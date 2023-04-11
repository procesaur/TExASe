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
from requests import get


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


def extract_text(file_bytes):
    bytesio = BytesIO(file_bytes)
    text = parser.from_buffer(bytesio)["content"]
    text = postprocess(text)
    return text


def add_cover_page(file_bytes, repo="", metadata_id=""):
    if create_cover:
        page = create_cover_page(repo, metadata_id)

        output = BytesIO()
        merger = PdfMerger()
        merger.append(BytesIO(page))
        merger.append(BytesIO(file_bytes))
        merger.write(output)

        return output.getbuffer().tobytes()
    return file_bytes


def create_cover_page(repo="", metadata_id=""):

    if not repo:
        repo = default_repo

    repo_cfg, cover_page, logo_path = get_repo_cfg(repo)

    uri = repo_cfg["uri_url"]+metadata_id
    metadata, cite_str = get_metadata(metadata_id, repo)
    if not metadata["timestamp"]:
        metadata["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cover_page = cover_page % (repo_cfg["repo_name_short"], repo_cfg["timestamp_label"], metadata["timestamp"],
                               metadata["title"], metadata["creator"], logo_path,
                               repo_cfg["img_width"], repo_cfg["img_height"], repo_cfg["repo_name"],
                               repo_cfg["repo_name_short"], cite_str, metadata["doi"], uri)

    output = pdf_from_string(cover_page, css="repos/" + repo + "/css.css",
                             options=repo_cfg["options"], configuration=pdfkit_config)
    return output


def get_metadata(metadata_id, repo=""):
    if not repo:
        repo = default_repo
    repo_cfg, cover_page, logo_path = get_repo_cfg(repo)

    metadata_json = get(repo_cfg["api_url"] + metadata_id).json()

    citation_string = ""
    for x in repo_cfg["citation_string"]:
        if ":" in x:
            try:
                citation_string += ";".join([y["@value"] for y in metadata_json[x]])
            except:
                pass
        else:
            citation_string += x

    metadata = {}
    for x in repo_cfg["basic_metadata_fields"]:
        try:
            metadata[x] = ";".join([y["@value"] for y in metadata_json[repo_cfg["basic_metadata_fields"][x]]])
        except:
            metadata[x] = ""

    return metadata, citation_string

