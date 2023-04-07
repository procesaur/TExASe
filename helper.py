from os import remove
from json import load
from os import path as px


def load_conf(path=None):
    if not path:
        path = px.join(px.dirname(__file__), "config.json")
    with open(path, "r", encoding="utf-8") as cf:
        return load(cf)


cfg = load_conf()


def get_tesseract_path():
    for path in cfg["tesseract"]["path"]:
        if px.isfile(path):
            return path

    return "tesseract"


def tryDel(file):
    try:
        remove(file)
    except:
        pass


def log_stuff(stuff):
    if "log" in cfg and cfg["log"]:
        try:
            with open(cfg["log"], "a+", encoding="utf-8") as lf:
                lf.write("\t".join([str(x) for x in stuff]) + "\n")
        except:
            pass


def get_return_type(service):
     if "return" not in cfg["services"][service]:
         return None
     return cfg["services"][service]["return"]


tesseract_path = get_tesseract_path()