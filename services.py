from helper import cfg
from tika import parser
from ocrmypdf import ocr
from io import BytesIO
from postprocessing import postprocess
from pytesseract import image_to_string, pytesseract, image_to_pdf_or_hocr
from PIL import Image


def extract(args):
    file, lang, renew, pdf = args
    bytesio = BytesIO(file)
    lang = OCRlang(lang)

    image = True
    if pdf:
        output_file = ocr_file(bytesio, lang)
        if output_file and renew:
            with open(file, "wb") as out_file:
                out_file.write(output_file)
        bytesio = BytesIO(output_file)
    else:
        output_file = None

    if image and lang:

        pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        text = image_to_string(Image.open(bytesio), lang)
        if text and renew:
            image_to_pdf_or_hocr(Image.open(bytesio))
    else:
        parsed = parser.from_buffer(bytesio)
        text = parsed["content"]

    text = postprocess(text)
    print(text)
    return text, output_file


def ocr_file(file, lang):
    output = BytesIO()
    if lang:
        ocr(input_file=file, output_file=output, skip_text=True, deskew=True, language=lang)
    else:
        ocr(input_file=file, output_file=output, skip_text=True, deskew=True)

    return output.getbuffer().tobytes()


def OCRlang(lang):
    if lang is None and cfg["languages"]:
        lang = "+".join(cfg["languages"])
        return lang
    else:
        return None
