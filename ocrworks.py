from pytesseract import pytesseract, image_to_pdf_or_hocr
from PIL import Image
from ocrmypdf import ocr as pdf_ocr
from helper import cfg, tesseract_path, poppler_path, pngquant_path, unpaper_path
from helper import should_aggro_ocr, should_deskew, should_clean, should_optimize, should_force_ocr
from io import BytesIO
from pdfworks import has_cover, merge_pages
from pdf2image import convert_from_bytes
from cv2 import cvtColor, resize, threshold, THRESH_OTSU, THRESH_BINARY, erode
from cv2 import COLOR_BGR2RGB, COLOR_RGB2BGR, COLOR_BGR2GRAY
from numpy import array as nparray, ndarray


agro = should_aggro_ocr()


def ocr_file(file_bytes, filetype, lang):
    lang = ocr_lang(lang)

    if filetype == "pdf":
        if has_cover(file_bytes):
            return file_bytes
        else:
            if agro:
                return aggro_ocr(file_bytes, lang)
            bytesio = BytesIO(file_bytes)
            return ocr_pdf(bytesio, lang)

    elif filetype == "img":
        return ocr_img(file_bytes, lang)

    return file_bytes


def ocr_img(image, lang):
    pytesseract.tesseract_cmd = tesseract_path
    if agro:
        image = improve_image(image)
    return image_to_pdf_or_hocr(image, extension='pdf', lang=lang)


def aggro_ocr(file_bytes, lang):
    pdfs = [ocr_img(image, lang) for image in convert_from_bytes(file_bytes, poppler_path=poppler_path)]
    return merge_pages(pdfs)


def ocr_pdf(bytesio, lang):
    output = BytesIO()
    kwargs = {}

    if lang:
        kwargs["language"] = lang
    if should_clean():
        kwargs["clean"] = True
        kwargs["oversample"] = 300
    if should_deskew():
        kwargs["deskew"] = True
    if should_force_ocr():
        kwargs["force_ocr"] = True
    else:
        kwargs["skip_text"] = True

    pdf_ocr(input_file=bytesio, output_file=output, optimize=should_optimize(), **kwargs)
    return output.getbuffer().tobytes()


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
