from tika import parser
from io import BytesIO


def extract_text(file_bytes):
    bytesio = BytesIO(file_bytes)
    text = parser.from_buffer(bytesio)["content"]
    text = postprocess(text)
    return text


def postprocess(text):
    return text
