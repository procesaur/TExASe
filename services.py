from helper import cfg
from tika import parser
from ocrmypdf import ocr
from io import BytesIO
from postprocessing import postprocess


def extract(args):
    file, lang, renew, pdf = args

    if pdf:
        output_file = ocr_file(file, lang)
        if output_file and renew:
            with open(file, "wb") as out_file:
                out_file.write(output_file.getbuffer())
        file = output_file
    else:
        output_file = None

    text = parser.from_file(file)
    text = postprocess(text)

    return text, output_file


def ocr_file(bytes, lang):
    output = BytesIO()
    input = BytesIO(bytes)

    if lang is None and cfg["languages"]:
        lang = "+".join(cfg["languages"])
        ocr(input_file=input, output_file=output, skip_text=True, language=lang, deskew=True)
    else:
        ocr(input_file=input, output_file=output, skip_text=True)
    return output
