from os import listdir, system, path as px, environ
from json import load, dumps
from re import sub
from datetime import datetime
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from tika import parser
from pdfkit import from_string as pdf_from_string
from PIL import Image
from pytesseract import image_to_string
from requests import get, post


with open(px.join(px.dirname(__file__), "config.json"), "r", encoding="utf-8") as jf:
    cfg = load(jf)


def create_first_page(item, itemId, cover_page_dir, f):
    f.write('\n            Inside create_first_page func.')

    options = {
        'page-size': 'A4',
        'encoding': 'utf-8',
        'footer-html': cover_page_dir + '/footer.html'
    }
    css = cover_page_dir + '/example.css'

    last_modified = str(datetime.strptime(item['o:modified']['@value'], '%Y-%m-%dT%H:%M:%S+00:00'))
    title = item['dcterms:title'][0]['@value']
    author = item['dcterms:creator'][0]['@value']
    cite_str = create_cite_str(item, f)
    try:
        doi = 'DOI: ' + item['bibo:doi'][0]['@value']
    except:
        doi = ' '
    uri = 'URI: dr.rgf.bg.ac.rs/s/repo/item/' + itemId.split(':')[1]

    with open(cover_page_dir + '/prva-strana.html', 'r', encoding='utf-8') as g:
        html_str = g.read()

    html_str = html_str % (last_modified, title, author, cite_str, doi, uri)

    pdf_from_string(html_str, cover_page_dir + '/out.pdf', options=options, css=css)
    system('chown www-data:www-data ' + cover_page_dir + '/out.pdf')
    f.write('\nFirst page created in' + cover_page_dir + '/out.pdf')


def create_cite_str(item, f):
    f.write('\nInside create_cite_str func.')
    cite_list = []
    fields = ['dcterms:creator', 'dcterms:title', 'dcterms:source', 'dcterms:issued',
              'rgf:bibliographicCitationVolume', 'rgf:bibliographicCitationIssue']

    for field in fields:
        try:
            x = item[field][0]['@value']
            cite_list.append(x)
        except:
            pass
    return ' | '.join(cite_list)



def file2txt(idx, filename, f):
    txt = 'failed'
    if px.exists(filename):
        f.write('\nmain(idx = %s, filename = %s, f)' % (idx, filename))
        try:
            ext = filename.split('.')[-1]
            f.write('\nFile type %s' % ext)
            if ext == 'jpg' or ext == 'png' or ext == 'tiff':
                f.write('\nOCR started [Image mode]')
                try:
                    txt = ocr_single(filename)
                except Exception as e:
                    f.write('\n[Error] ' + str(e))
                    txt = 'example'
            # Nije slika
            else:
                try:
                    f.write('\nText extraction started [Apache Tika]')
                    raw = parser.from_file(filename)
                    txt = raw['content']
                    txt = process_txt(txt)
                    if txt == ' ':
                        x = txt[10]
                    try:
                        # Tika procitala
                        if filename.endswith('.pdf'):
                            f.write('\n    Edit vec postojeceg itema')
                            r = get('http://10.100.0.81/' + omeka_instance + '/api/items/' + itemId.split(':')[1])
                            f.write('\n    Getting item metadata from Omeka Api: %s' % str(r))
                            item = r.json()
                            last_modified = str(datetime.strptime(item['o:modified']['@value'], '%Y-%m-%dT%H:%M:%S+00:00'))
                            f.write('\n        last_modified = %s' % last_modified)
                            check_str = 'Последња измена:'
                            if check_str in txt[:100]:
                                f.write('\ncheck_str in txt[:100]')
                                if last_modified not in txt[:100]:
                                    if omeka_instance in pdf_add:
                                        f.write('\nlast_modified not in txt[:100]')
                                        remove_first_page(filename, f)
                                        create_first_page(item, itemId, f)
                                        add_cover_page(filename, f)
                                    else:
                                        f.write('\nNot adding cover page\n')
                            else:
                                if omeka_instance in pdf_add:
                                    create_first_page(item, itemId, f)
                                    add_cover_page(filename,f)
                                else:
                                    f.write('\nNot adding cover page\n')
                    except Exception as e:
                        f.write('\n[ERROR] Tried to add page: ' + str(e))
                except Exception as e:
                    f.write('\nUnable to extract text, attempting OCR...' + str(e))
                    f.write('\nPdfsandwich started...')
                    system('pdfsandwich -quiet -lang=srp+srp_latn ' + filename + ' -o ' + filename)
                    system('chown www-data:www-data ' + filename)
                    f.write('\nPdfsandwich finished')
                    raw = parser.from_file(filename)
                    txt = raw['content']
                    txt = process_txt(txt)

                    try:
                        if filename.endswith('.pdf'):
                            f.write('\n    Editing first page')
                            r = get('http://10.100.0.81/' + omeka_instance + '/api/items/' + itemId.split(':')[1])
                            item = r.json()
                            last_modified = str(datetime.strptime(item['o:modified']['@value'], '%Y-%m-%dT%H:%M:%S+00:00'))
                            check_str = 'Последња измена:'
                            if check_str in txt[:100]:
                                f.write('\n        check_str in txt[:100]')
                                if last_modified not in txt[:100]:
                                    f.write('\n        last_modified not in txt[:100]')
                                    if omeka_instance in pdf_add:
                                        remove_first_page(filename, f)
                                        create_first_page(item, itemId, f)
                                        add_cover_page(filename, f)
                                    else:
                                        f.write('\nNot adding cover page\n')
                            else:
                                if omeka_instance in pdf_add:
                                    create_first_page(item, itemId, f)
                                    add_cover_page(filename, f)
                                    f.write('\n    Cover page created and merged')
                                else:
                                    f.write('\nNot adding cover page\n')
                    except Exception as e:
                        f.write('\n[ERROR] Error in editing first page: ' + str(e))
        except Exception as e:
            f.write('\nText extraction failed. [Error]: ' + str(e))
            txt = 'example'

    else:
        f.write('\nFile not found.')
        txt = 'example'

    filename = filename.split('.')[0]
    with open(filename + '_ocr' + '.txt', 'w') as f:
        f.write(txt)
    cleanup(temp_folders[idx])
    return txt


def rq_handler(data):
    print('RQ Handler started')
    environ['OMP_THREAD_LIMIT'] = '1'
    itemId = 'items:' + data.split('|')[0]
    filepaths = data.split('|')[1]
    filepaths = filepaths.split(',')
    f = open('log_long_run4.txt', 'a+')
    ###################################################
    #                   Settings                      #
    ###################################################
    pdf_add = ['repo_rgf']

    omeka_instance = filepaths[0].split('/')[4]
    solr_core = omeka_instance.split('_')[1]
    instance_dir = '/usr/custom/' + omeka_instance
    temp_dir = '/usr/custom/' + omeka_instance + '/temp'
    cover_page_dir = '/usr/custom/' + omeka_instance + '/cover_page'
    ###################################################
    f.write(' '.join(['\n####', str(datetime.now()), '####', '\n']))
    f.write('\n' + data + '\n')
    f.write('\n'.join(
        ['omeka_instance = ' + omeka_instance, 'solr_core = ' + solr_core, 'instance_dir = ' + instance_dir,
         'temp_dir = ' + temp_dir]))
    temp_folders = []
    for filepath in filepaths:
        temp_folders.append(temp_dir + '/' + filepath.split('.')[0].split('/')[-1] + '_temp')
    for temp_folder_path in temp_folders:
        system('mkdir ' + temp_folder_path)


    media_txt = ''
    for idx, filepath in enumerate(filepaths):
        media_txt = media_txt + '\n' + file2txt(idx, filepath, f)
    r = get('http://10.100.0.81:8983/solr/' + solr_core + '/get?id=' + itemId)
    item = r.json()
    item['doc']['media_txt'] = media_txt

    item['doc']['hasMedia'] = []
    for filepath in filepaths:
        path, ext = px.splitext(filepath)
        item['doc']['hasMedia'].append(ext[1:])

    item = item['doc']
    payload = dumps(item)
    url = 'http://localhost:8983/solr/' + solr_core + '/update/json/docs?commit=true'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF=8'}
    r = post(url, data=payload, headers=headers)
    f.write('\nSubmitted to Solr index: ' + itemId + ' ' + str(r))
    f.close()
    
    
def process_txt(txt):
    txt = sub(r'\t+', ' ', txt)
    txt = sub(r'(-)?\n+', '', txt)
    txt = sub(r'\n,', ' ', txt)
    txt = sub(r'\s+', ' ', txt)
    return txt


def cleanup(temp_folder):
    system('rm -rf ' + temp_folder)


def ocr(img_path):
    img = Image.open(temp_folders[idx] + '/' + img_path)
    txt = image_to_string(img, lang='srp+srp_latn')  # , config='--psm 6'
    return process_txt(txt)


def ocr_single(img_path):
    img = Image.open(img_path)
    new_size = tuple(2 * x for x in img.size)
    img = img.resize(new_size, Image.ANTIALIAS)
    txt = image_to_string(img, lang='srp+srp_latn')  # , config='--psm 6'
    return process_txt(txt)


def add_cover_page(filename, cover_page_dir, f):
    merger = PdfFileMerger()
    input1 = open(cover_page_dir + '/out.pdf', 'rb')
    input2 = open(filename, 'rb')
    merger.append(input1)
    merger.append(input2)
    system('rm ' + filename)
    output = open(filename, 'wb')
    merger.write(output)
    system('chown www-data:www-data ' + filename)
    f.write('\nFirst page and original file merged')


def remove_first_page(filename):
    old = PdfFileReader(filename, 'rb')
    new = PdfFileWriter()

    for i in range(old.getNumPages()):
        if i != 0:
            p = old.getPage(i)
            new.addPage(p)

    with open(filename, 'wb') as f:
        new.write(f)


def remove_all_first_pages(site):
    files_dir = f"""{cfg["sites_dir"]}/{site}/{cfg["files_relative_dir"]}"""
    pdfs = [file for file in listdir(files_dir) if file.endswith('.pdf')]

    check_str = 'Последња измена:'
    headers = {'X-Tika-PDFextractInlineImages': 'true'}
    for pdf in pdfs:
        try:
            raw = parser.from_file(files_dir + '/' + pdf)
            print(files_dir + '/' + pdf)
            txt = raw['content']
            txt = process_txt(txt)
            # print(txt)
            if txt == ' ':
                x = txt[10]
            try:
                if check_str in txt[:100]:
                    remove_first_page(files_dir + '/' + pdf)
                else:
                    print('Did nothing. ' + files_dir + '/' + pdf)
            except Exception as e:
                print('Failed!' + str(e))
        except Exception as e:
            print('File corrupted or empty ' + str(e) + ' ' + pdf)