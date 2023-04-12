from extractworks import extract_text, extract_all_text
from ocrworks import ocr_file
from pdfworks import add_cover_page, remove_cover_page, remove_all_filecovers
from repoworks import get_citation_string, get_metadata


def extract(args):
    file_bytes, filetype, params = args
    text = extract_text(file_bytes)
    return text, None


def ocr(args):
    file_bytes, filetype, params = args
    new_file = ocr_file(file_bytes, filetype, params["lang"])
    new_file = add_cover_page(new_file, item_id=params["id"], repo=params["repo"], nocover=params["nocover"])
    return None, new_file
  

def renew(args):
    file_bytes, filetype, params = args
    new_file = ocr_file(file_bytes, filetype, params["lang"])
    new_file = add_cover_page(new_file, item_id=params["id"], repo=params["repo"], nocover=params["nocover"])
    with open(params["file_path"], "wb") as out_file:
        out_file.write(new_file)
    
    
def ocr_and_extract(args):
    file_bytes, filetype, params = args
    new_file = ocr_file(file_bytes, filetype, params["lang"])
    text = extract_text(new_file)
    new_file = add_cover_page(new_file, item_id=params["id"], repo=params["repo"], nocover=params["nocover"])
    return text, new_file


def add_cover(args):
    file_bytes, filetype, params = args
    new_file = add_cover_page(file_bytes, item_id=params["id"], repo=params["repo"])
    return new_file


def remove_cover(args):
    file_bytes, filetype, params = args
    new_file = remove_cover_page(file_bytes)
    return new_file


def remove_all_covers(args):
    file_bytes, filetype, params = args
    remove_all_filecovers(params["path"])


def citation(args):
    file_bytes, filetype, params = args
    return get_citation_string(params["id"], params["repo"])


def metadata(args):
    file_bytes, filetype, params = args
    return str(get_metadata(params["id"], params["repo"]))


def extract_all(args):
    file_bytes, filetype, params = args
    return extract_all_text(params["path"])


services = {
    "extract": extract,
    "ocr_file": ocr_file,
    "renew": renew,
    "ocr_and_extract": ocr_and_extract,
    "add_cover": add_cover,
    "remove_cover": remove_cover,
    "remove_all_covers": remove_all_covers,
    "citation": citation,
    "metadata": metadata,
    "extract_all": extract_all
}
