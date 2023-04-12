from ocrworks import ocr_file, extract_text
from pdfworks import add_cover_page


def extract(args):
    file_bytes, filetype, params = args
    text = extract_text(file_bytes)
    return text, None


def ocr(args):
    file_bytes, filetype, params = args
    new_file = ocr_file(file_bytes, filetype, params["lang"])
    new_file = add_cover_page(new_file)
    return None, new_file
  

def renew(args):
    file_bytes, filetype, params = args
    new_file = ocr_file(file_bytes, filetype, params["lang"])
    new_file = add_cover_page(new_file)
    with open(params["file_path"], "wb") as out_file:
        out_file.write(new_file)
    
    
def ocr_and_extract(args):
    file_bytes, filetype, params = args
    new_file = ocr_file(file_bytes, filetype, params["lang"])
    text = extract_text(new_file)
    new_file = add_cover_page(new_file, metadata_id="752")
    return text, new_file


services = {
    "extract": extract,
    "ocr_file": ocr_file,
    "renew": renew,
    "ocr_and_extract": ocr_and_extract
}
