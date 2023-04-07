from pytesseract import pytesseract, image_to_pdf_or_hocr
from PIL import Image
from ocrmypdf import ocr as pdf_ocr
from helper import cfg, tesseract_path
from tika import parser
from io import BytesIO
from postprocessing import postprocess
from datetime import datetime
from helper import default_repo, get_repo_cfg, create_cover, pdfkit_config
from pdfkit import from_string as pdf_from_string
from PyPDF2 import PdfMerger


def ocr_file(file_bytes, filetype, lang):
    bytesio = BytesIO(file_bytes)
    lang = ocr_lang(lang)
    if filetype == "pdf":
        if create_cover:
            return add_cover_page(ocr_pdf(bytesio, lang))
        else:
            return ocr_pdf(bytesio, lang)

    elif filetype == "image":
        pytesseract.tesseract_cmd = tesseract_path
        if create_cover:
            return add_cover_page(image_to_pdf_or_hocr(Image.open(bytesio), extension='pdf'))
        else:
            return image_to_pdf_or_hocr(Image.open(bytesio), extension='pdf')
    else:
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


def extract_text(file_bytes):
    bytesio = BytesIO(file_bytes)
    text = parser.from_buffer(bytesio)["content"]
    text = postprocess(text)
    return text


def add_cover_page(file_bytes, timestamp=None, repo="", metadata_url=""):

    page = create_cover_page(timestamp, repo, metadata_url)

    output = BytesIO()
    merger = PdfMerger()
    merger.append(BytesIO(page))
    merger.append(BytesIO(file_bytes))
    merger.write(output)

    return output.getbuffer().tobytes()


def create_cover_page(timestamp=None, repo="", metadata_url=""):

    if not repo:
        repo = default_repo

    repo_cfg, cover_page, logo_path = get_repo_cfg(repo)

    if not timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    title, authors, source, issued, volume, issue, doi, uri = get_metadata(metadata_url)

    cite_str = create_cite_str(title, authors, source, issued, volume, issue)

    cover_page = cover_page % (repo_cfg["repo_name_short"], repo_cfg["timestamp_label"], timestamp, title, authors,
                               logo_path, repo_cfg["img_width"], repo_cfg["img_height"], repo_cfg["repo_name"],
                               repo_cfg["repo_name_short"], cite_str, doi, uri)

    output = pdf_from_string(cover_page, css="repos/" + repo + "/css.css",
                             options=repo_cfg["options"], configuration=pdfkit_config)
    return output


def get_metadata(metadata_url):
    try:
        return title, authors, source, issued, volume, issue, doi, uri
    except:
        return "", "", "", "", "", "", "", ""


def create_cite_str(title, authors, source, issued, volume, issue):
    cite_list = []
    fields = [title, authors, source, issued, volume, issue]

    for x in fields:
        try:
            cite_list.append(x)
        except:
            pass
    return ' | '.join(cite_list)
