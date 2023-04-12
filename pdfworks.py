from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from helper import create_cover, pdfkit_config
from datetime import datetime
from pdfkit import from_string as pdf_from_string
from repoworks import get_metadata, default_repo, get_repo_cfg


def has_cover(file_bytes):
    try:
        reader = PdfReader(BytesIO(file_bytes))
        if reader.metadata["/has_texase_cover"] == "yes":
            return True
        else:
            return False
    except:
        return False


def remove_cover(file_bytes):
    try:
        input = PdfReader(BytesIO(file_bytes))
        output = BytesIO()
        writer = PdfWriter()
        for i, page in enumerate(input.pages):
            if i > 0:
                writer.add_page(page)
        writer.write(output)
        return output.getbuffer().tobytes()
    except:
        return file_bytes


def add_cover_page(file_bytes, repo="", metadata_id=""):
    if create_cover:

        if has_cover(file_bytes):
            remove_cover(file_bytes)

        page = create_cover_page(repo, metadata_id)

        output = BytesIO()
        merger = PdfMerger()
        merger.append(BytesIO(page))
        merger.append(BytesIO(file_bytes))
        merger.add_metadata({
            '/has_texase_cover': 'yes'
        })
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