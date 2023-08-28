from pytesseract import pytesseract, image_to_pdf_or_hocr
from PIL import Image
from helper import cfg, tesseract_path, poppler_path, image_improve
from io import BytesIO
from pdfworks import has_cover, merge_pages
from pdf2image import convert_from_bytes
from cv2 import cvtColor, resize, threshold, THRESH_OTSU, THRESH_BINARY, erode
from cv2 import COLOR_BGR2RGB, COLOR_RGB2BGR, COLOR_BGR2GRAY
from numpy import array as nparray, ndarray


def ocr_file(file_bytes, filetype, lang):
    bytesio = BytesIO(file_bytes)
    lang = ocr_lang(lang)
    if filetype == "pdf":
        if has_cover(file_bytes):
            return file_bytes
        return ocr_pdf(file_bytes, lang)

    elif filetype == "image":
        return ocr_image(Image.open(bytesio), lang)

    return file_bytes


def ocr_image(image, lang):
    if image_improve:
        image = improve_image(image)
    pytesseract.tesseract_cmd = tesseract_path
    return image_to_pdf_or_hocr(image, extension='pdf', lang=lang)


def ocr_pdf(bytesio, lang):
    images = convert_from_bytes(bytesio, poppler_path=poppler_path)
    pdfs = [ocr_image(image, lang) for image in images]
    return merge_pages(pdfs)


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


def convert_from_cv2_to_image(img: ndarray) -> Image:
    return Image.fromarray(cvtColor(img, COLOR_BGR2RGB))


def convert_from_image_to_cv2(img: Image) -> ndarray:
    return cvtColor(nparray(img), COLOR_RGB2BGR)


def improve_image(image):
    img = convert_from_image_to_cv2(image)
    img = resize(img, (0, 0), fx=2, fy=2)
    gry = cvtColor(img, COLOR_BGR2GRAY)
    erd = erode(gry, None, iterations=1)
    thr = threshold(erd, 0, 255, THRESH_BINARY + THRESH_OTSU)[1]
    return convert_from_cv2_to_image(thr)
