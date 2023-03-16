from services import extract
from helper import log_stuff
from flask import request


def process_req(req):
    # get query parameters
    query_parameters = req.args
    if len(query_parameters) == 0:
        query_parameters = req.form

    file = query_parameters.get('file')
    lang = query_parameters.get('lang')
    save_pdf = query_parameters.get('save_pdf')

    log_stuff([request.remote_addr, file, lang, save_pdf])

    if save_pdf == 1:
        save_pdf = True

    function = extract
    args = (file, lang, save_pdf)

    return function, args
