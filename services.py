from helper import cfg


def extract(args):
    file, lang, save_pdf = args

    with open("E:aaaa.txt", "w+") as tf:
        tf.write("asdasdasdad")
    return "asdasdasd"


def remove_first_page(filename):
    old = PdfFileReader(filename, 'rb')
    new = PdfFileWriter()

    for i in range(old.getNumPages()):
        if i != 0:
            p = old.getPage(i)
            new.addPage(p)

    with open(filename, 'wb') as f:
        new.write(f)


def remove_first_pages(filenames):
    return 0


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