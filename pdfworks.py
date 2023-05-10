from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from helper import should_create_cover, pdfkit_config
from datetime import datetime
from pdfkit import from_string as pdf_from_string
from repoworks import get_repo_cfg, get_metadata_from_url, generate_citation_string
from os import listdir, path as px


def has_cover(file_bytes):
    try:
        reader = PdfReader(BytesIO(file_bytes))
        if reader.metadata["/has_texase_cover"] == "yes":
            return True
        return False

    except:
        return False


def remove_cover_page(file_bytes):
    try:
        input = PdfReader(BytesIO(file_bytes))
        output = BytesIO()
        writer = PdfWriter()
        for i, page in enumerate(input.pages):
            if i > 0:
                writer.add_page(page)
        writer.addMetadata({
            '/has_texase_cover': 'no'
        })
        writer.write(output)
        return output.getbuffer().tobytes()
    except:
        return file_bytes


def add_cover_page(file_bytes, item_id="", repo="", nocover=False):
    if should_create_cover(repo) and not nocover:

        if has_cover(file_bytes):
            file_bytes = remove_cover_page(file_bytes)

        page = create_cover_page(repo, item_id)

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
    repo_cfg, cover_page, logo_path, css_path = get_repo_cfg(repo)

    uri = repo_cfg["uri_url"] + metadata_id
    metadata = get_metadata_from_url(repo_cfg["uri_url"], metadata_id)

    for field in repo_cfg["basic_metadata_fields"]:
        if field not in metadata.keys():
            metadata[field] = ""

    cite_str = generate_citation_string(repo_cfg["citation_string"], metadata)
    if "timestamp" not in metadata.keys():
        metadata["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif not metadata["timestamp"]:
        metadata["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cover_page = cover_page % (repo_cfg["repo_name_short"], repo_cfg["timestamp_label"], metadata["timestamp"],
                               metadata["title"], metadata["creator"], logo_path,
                               repo_cfg["img_width"], repo_cfg["img_height"], repo_cfg["repo_name"],
                               repo_cfg["repo_name_short"], cite_str, metadata["doi"], uri)

    output = pdf_from_string(cover_page, css=css_path, options=repo_cfg["options"], configuration=pdfkit_config)
    return output


def remove_all_filecovers(path):
    if not path.endswith("/"):
        path = path + "/"
    if px.isdir(path):
        files = listdir(path)
        for file in files:
            try:
                with open(path + file, "rb") as fb:
                    new_file = remove_cover_page(fb.read())
                    fb.write(new_file)
            except:
                pass