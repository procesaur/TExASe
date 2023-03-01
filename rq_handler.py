from services import remove_first_pages, extract, remove_all_first_pages
from helper import log_stuff
from flask import request
from os import path as px


def process_req(req):
    # get query parameters
    query_parameters = req.args
    if len(query_parameters) == 0:
        query_parameters = req.form

    if request.path == "remove_first_pages":
        fnames = query_parameters.get('filenames')

        log_stuff([request.remote_addr, "remove_first_pages", fnames])

        if px.isdir(fnames):
            function = remove_all_first_pages
            args = fnames
        else:
            function = remove_first_pages
            args = fnames.split("|")

    else:
        file = query_parameters.get('file')
        lang = query_parameters.get('lang')
        save_pdf = query_parameters.get('save_pdf')

        log_stuff([request.remote_addr, file, lang, save_pdf])

        if save_pdf == 1:
            save_pdf = True

        function = extract
        args = (file, lang, save_pdf)

    return function, args