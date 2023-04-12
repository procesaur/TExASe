from tika import parser
from io import BytesIO
from os import path as px, walk


def extract_text(file_bytes):
    bytesio = BytesIO(file_bytes)
    text = parser.from_buffer(bytesio)["content"]
    text = postprocess(text)
    return text


def extract_all_text(path):
    if not path.endswith("/"):
        path = path + "/"
    filelist = []
    output = {}
    if px.isdir(path):
        for root, dirs, files in walk(path):
            for file in files:
                filelist.append(px.join(root, file))
    for filepath in filelist:
        with open(filepath, "rb") as f:
            output[filepath] = extract_text(f.read())


def postprocess(text):
    return text
