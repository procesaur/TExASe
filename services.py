from helper import cfg
from textract import process
from ocrmypdf import ocr


def extract(args):
    file, lang, save_pdf = args

    if file.endswith(".pdf") and save_pdf:
        try:
            if lang is None and cfg["languages"]:
                lang = "+".join(cfg["languages"])
                ocr(input_file=file, output_file=file, skip_text=True, language=lang)
            else:
                ocr(input_file=file, output_file=file, skip_text=True)
        except:
            pass

    text = process(file)
    return text
