from helper import log_stuff, cfg
from flask import request
from os import path as px


def process_req(req, service):
    query_parameters = params_from_req(req)

    file_bytes, filetype, filename = process_file_req(req, query_parameters)
    params = get_params(query_parameters, service)
    log_stuff([request.remote_addr, filename, ";".join(params)])
    args = (file_bytes, filetype, params)

    return filename, args


def params_from_req(req):
    query_parameters = req.args
    if len(query_parameters) == 0:
        query_parameters = req.form
    return query_parameters


def get_params(query_parameters, service):
    required = cfg["services"][service]["params"]
    params = {}
    for param in required:
        if required[param] == "bool":
            params[param] = get_bool(query_parameters, param)
        elif required[param] == "string":
            params[param] = get_string(query_parameters, param)
        else:
            pass
    return params


def process_file_req(req, query_parameters):
    if "file" in req.files:
        file_bytes = req.files["file"].read()
        filename = req.files["file"].filename
        if filename != "":
            filetype = file2filetype(req.files["file"])
            return file_bytes, filetype, filename

    filename = query_parameters.get('file')
    filetype = filename2filetype(filename)
    file_bytes = filepath2file(filename)

    return file_bytes, filetype, filename


def get_string(params, name, alternative=None):
    try:
        result = params.get(name)
        if result == "":
            result = alternative
    except:
        result = alternative

    return result


def get_bool(params, name, default=False):
    try:
        result = params.get(name)
        if result == 1 or result == "1":
            result = True
        else:
            result = False
    except:
        result = default

    return result


def file2filetype(file):
    ct = file.content_type
    if "pdf" in ct:
        return "pdf"
    if "image" in ct:
        return "image"
    return "doc"


def filename2filetype(filename):
    if ".pdf" in filename:
        return "pdf"
    for ext in cfg["tesseract"]["img_ext"]:
        if ext in filename:
            return "image"
    return "doc"


def filepath2file(filepath):
    if px.exists(filepath):
        with open(filepath, "rb") as f:
            file_bytes = f.read()
        return file_bytes
    else:
        return None
