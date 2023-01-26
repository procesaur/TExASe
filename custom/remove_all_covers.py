import os
import re
from long_run4 import parser
from PyPDF2 import PdfFileReader, PdfFileWriter


def process_txt(txt):
    txt = re.sub(r'\t+', ' ', txt)
    txt = re.sub(r'(-)?\n+', '', txt)
    txt = re.sub(r'\n,', ' ', txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt


def remove_first_page(filename):
    old = PdfFileReader(filename, 'rb')
    new = PdfFileWriter()

    for i in range(old.getNumPages()):
        if i != 0:
            p = old.getPage(i)
            new.addPage(p)

    with open(filename, 'wb') as f:
        new.write(f)


files_dir = '/var/www/html/repo_rgf/files/original'
pdfs = [file for file in os.listdir(files_dir) if file.endswith('.pdf')]

check_str = 'Последња измена:'
headers = {'X-Tika-PDFextractInlineImages':'true'}
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