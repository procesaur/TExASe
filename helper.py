from os import remove
from json import load
from os import path as px
from pdfkit import configuration


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


def get_wkhtmltopdf_path():
    for path in cfg["wkhtmltopdf_path"]:
        if px.isfile(path):
            return path

    return "wkhtmltopdf"


def get_pdfkit_config():
    return configuration(wkhtmltopdf=get_wkhtmltopdf_path())


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


def get_default_repo():
    if "default_repo" in cfg:
        return cfg["default_repo"]
    return "default"


def get_repo_cfg(repo):
    if not repo:
        repo = default_repo
    with open(px.join(px.dirname(__file__), "repos/" + repo + "/config.json"), "r", encoding="utf-8") as cf:
        cfg = load(cf)
    with open(px.join(px.dirname(__file__), "repos/" + repo + "/cover.html"), "r", encoding="utf-8") as hf:
        html = hf.read()

    logo_path = px.join(px.dirname(__file__), cfg["logo_path"])
    css_path = px.join(px.dirname(__file__), "repos/" + repo + "/css.css")

    return cfg, html, logo_path, css_path


def should_create_cover(repo):
    repo_cfg, cover_page, logo_path, css_path = get_repo_cfg(repo)
    if "create_first_page" in repo_cfg:
        if repo_cfg["create_first_page"]:
            return True
    return False


pdfkit_config = get_pdfkit_config()
default_repo = get_default_repo()
tesseract_path = get_tesseract_path()
