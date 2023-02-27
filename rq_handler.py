from services import remove_first_pages, extract, remove_all_first_pages
from helper import log_stuff, cfg
from flask import request
from os import path as px
import time


def task_in_background(t):
    delay = 1

    print("Running Task")
    print("Simulates the {delay} seconds")

    time.sleep(delay)

    print(len(t))
    print("Completed Task")

    return len(t)


def process_req(req, target="api"):
    # get query parameters
    query_parameters = req.args
    if len(query_parameters) == 0:
        query_parameters = req.form

    if target == "remove_first_pages":
        fnames = query_parameters.get('filenames')

        log_stuff([request.remote_addr, "remove_first_pages", fnames])

        if px.isdir(fnames):
            remove_all_first_pages(fnames)
        else:
            filenames = fnames.split("|")
            remove_first_pages(filenames)

    else:
        file = query_parameters.get('file')
        lang = query_parameters.get('lang')
        save_pdf = query_parameters.get('save_pdf')

        log_stuff([request.remote_addr, file, lang, save_pdf])

        if save_pdf == 1:
            save_pdf = True

        return extract(file, lang, save_pdf)


def process_req2():
    with open("E:/new", "w") as f:
        f.write("asdasdasdasda")