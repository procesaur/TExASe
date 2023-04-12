from pytesseract import pytesseract, image_to_pdf_or_hocr
from PIL import Image
from ocrmypdf import ocr as pdf_ocr
from helper import cfg, tesseract_path
from io import BytesIO


def ocr_file(file_bytes, filetype, lang):
    bytesio = BytesIO(file_bytes)
    lang = ocr_lang(lang)
    if filetype == "pdf":
        return ocr_pdf(bytesio, lang)

    elif filetype == "image":
        pytesseract.tesseract_cmd = tesseract_path
        return image_to_pdf_or_hocr(Image.open(bytesio), extension='pdf')

    return file_bytes


def ocr_image(bytesio, lang):
    pytesseract.tesseract_cmd = tesseract_path
    return image_to_pdf_or_hocr(Image.open(bytesio), extension='pdf', lang=lang)


def ocr_pdf(bytesio, lang):
    output = BytesIO()
    if lang:
        pdf_ocr(input_file=bytesio, output_file=output, skip_text=True, deskew=True, language=lang)
    else:
        pdf_ocr(input_file=bytesio, output_file=output, skip_text=True, deskew=True)

    return output.getbuffer().tobytes()


def ocr_lang(lang):
    available_langs = get_available_langs()
    if lang in available_langs or not available_langs:
        return lang

    return "+".join(available_langs)


def get_available_langs():
    if not cfg["tesseract"]:
        return None

    if not cfg["tesseract"]["languages"]:
        return None

    return cfg["tesseract"]["languages"]
