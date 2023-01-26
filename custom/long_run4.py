import pytesseract
import os
from PIL import Image
import re
from tika import parser
import requests
import json
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import pdfkit
import contextlib
from datetime import datetime
# from settings import settings


def rq_handler(data):
    print('RQ Handler started')
    os.environ['OMP_THREAD_LIMIT'] = '1'
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
    f.write('\n'+data+'\n')
    f.write('\n'.join(['omeka_instance = ' + omeka_instance, 'solr_core = ' + solr_core, 'instance_dir = ' + instance_dir, 'temp_dir = ' + temp_dir]))
    temp_folders = []
    for filepath in filepaths:
        temp_folders.append(temp_dir + '/' + filepath.split('.')[0].split('/')[-1] + '_temp')
    for temp_folder_path in temp_folders:
        os.system('mkdir ' + temp_folder_path)

    def create_first_page(item, itemId, f):
        f.write('\n            Inside create_first_page func.')
        def create_cite_str(item, f):
            f.write('\n                Inside create_cite_str func.')
            cite_list = []
            try:
                author = item['dcterms:creator'][0]['@value']
                cite_list.append(author)
            except:
                pass
            try:
                title = item['dcterms:title'][0]['@value']
                cite_list.append(title)
            except:
                pass
            try:
                source = item['dcterms:source'][0]['@value']
                cite_list.append(source)
            except:
                pass
            try:
                year = item['dcterms:issued'][0]['@value']
                cite_list.append(year)
            except:
                pass
            try:
                volume = item['rgf:bibliographicCitationVolume'][0]['@value']
                cite_list.append(volume)
            except:
                pass
            try:
                number = item['rgf:bibliographicCitationIssue'][0]['@value']
                cite_list.append(number)
            except:
                pass
            return ' | '.join(cite_list)

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

        pdfkit.from_string(html_str, cover_page_dir + '/out.pdf', options=options, css=css)
        os.system('chown www-data:www-data ' + cover_page_dir + '/out.pdf')
        f.write('\nFirst page created in' + cover_page_dir + '/out.pdf')

    def add_cover_page(filename, f):
        merger = PdfFileMerger()
        input1 = open(cover_page_dir + '/out.pdf', 'rb')
        input2 = open(filename, 'rb')
        merger.append(input1)
        merger.append(input2)
        os.system('rm ' + filename)
        output = open(filename, 'wb')
        merger.write(output)
        os.system('chown www-data:www-data ' + filename)
        f.write('\nFirst page and original file merged')

    def remove_first_page(filename, f):
        old = PdfFileReader(filename, 'rb')
        new = PdfFileWriter()

        for i in range(old.getNumPages()):
            if i != 0:
                p = old.getPage(i)
                new.addPage(p)

        with open(filename, 'wb') as f:
            new.write(f)
        f.write('\nRemoved first page')

    def cleanup(temp_folder):
        os.system('rm -rf ' + temp_folder)
        f.write('\nTemp folder cleaned')

    def process_txt(txt):
        txt = re.sub(r'\t+', ' ', txt)
        txt = re.sub(r'(-)?\n+', '', txt)
        txt = re.sub(r'\n+', ' ', txt)
        txt = re.sub(r'\s+', ' ', txt)
        return txt

    def ocr(img_path):
        img = Image.open(temp_folders[idx] + '/' + img_path)
        txt = pytesseract.image_to_string(img, lang='srp+srp_latn')  # , config='--psm 6'
        return process_txt(txt)

    def ocr_single(img_path):
        img = Image.open(img_path)
        new_size = tuple(2 * x for x in img.size)
        img = img.resize(new_size, Image.ANTIALIAS)
        txt = pytesseract.image_to_string(img, lang='srp+srp_latn')  # , config='--psm 6'
        return process_txt(txt)

    def main(idx, filename, f):
        txt = 'failed'
        if os.path.exists(filename):
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
                                r = requests.get('http://10.100.0.81/' + omeka_instance + '/api/items/' + itemId.split(':')[1])
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
                        os.system('pdfsandwich -quiet -lang=srp+srp_latn ' + filename + ' -o ' + filename)
                        os.system('chown www-data:www-data ' + filename)
                        f.write('\nPdfsandwich finished')
                        raw = parser.from_file(filename)
                        txt = raw['content']
                        txt = process_txt(txt)

                        try:
                            if filename.endswith('.pdf'):
                                f.write('\n    Editing first page')
                                r = requests.get('http://10.100.0.81/' + omeka_instance + '/api/items/' + itemId.split(':')[1])
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

    media_txt = ''
    for idx, filepath in enumerate(filepaths):
        media_txt = media_txt + '\n' + main(idx, filepath, f)
    r = requests.get('http://10.100.0.81:8983/solr/' + solr_core + '/get?id=' + itemId)
    item = r.json()
    item['doc']['media_txt'] = media_txt

    item['doc']['hasMedia'] = []
    for filepath in filepaths:
        path, ext = os.path.splitext(filepath)
        item['doc']['hasMedia'].append(ext[1:])

    item = item['doc']
    payload = json.dumps(item)
    url = 'http://localhost:8983/solr/' + solr_core + '/update/json/docs?commit=true'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF=8'}
    r = requests.post(url, data=payload, headers=headers)
    f.write('\nSubmitted to Solr index: ' + itemId + ' ' + str(r))
    f.close()