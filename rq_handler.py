from services import extract
from helper import log_stuff
from flask import request
from os import path as px


def process_req(req):
    query_parameters = params_from_req(req)

    file, pdf = process_file_req(req, query_parameters)

    lang = get_string(query_parameters, "lang")
    renew = get_bool(query_parameters, "renew")

    log_stuff([request.remote_addr, file, lang, renew])

    function = extract
    args = (file, lang, renew, pdf)

    return function, args


def params_from_req(req):
    query_parameters = req.args
    if len(query_parameters) == 0:
        query_parameters = req.form
    return query_parameters


def process_file_req(req, query_parameters):
    if "file" in req.files:
        file = req.files["file"]
        name = file.filename
    else:
        name = query_parameters.get('file')
        if px.exists(name):
            with open(name, "rb") as f:
                file = f.read()
        else:
            file = None

    if name.endswith("pdf"):
        pdf = True
    else:
        pdf = False

    return file, pdf


def get_string(params, name, alternative=None):
    try:
        result = params.get(name)
        if result is "":
            result = alternative
    except:
        result = alternative

    return result


def get_bool(params, name, default=False):
    try:
        result = params.get(name)
        if result == 1:
            result = True
        else:
            result = False
    except:
        result = default

    return result
