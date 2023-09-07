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


def get_poppler_path():
    for path in cfg["poppler_path"]:
        if px.isdir(path):
            return path
    return None


def get_unpaper_path():
    for path in cfg["unpaper_path"]:
        if px.isdir(path):
            return path
    return None


def get_pngquant_path():
    for path in cfg["pngquant_path"]:
        if px.isdir(path):
            return path
    return None


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

    cfg["options"]["footer-html"] = px.join(px.dirname(__file__), cfg["options"]["footer-html"])

    return cfg, html, logo_path, css_path


def should_create_cover(repo=None):
    repo_cfg, cover_page, logo_path, css_path = get_repo_cfg(repo)
    if "create_first_page" in repo_cfg:
        if repo_cfg["create_first_page"]:
            return True
    return False


def should_aggro_ocr(repo=None):
    if not repo:
        repo = get_default_repo()
    repo_cfg, cover_page, logo_path, css_path = get_repo_cfg(repo)
    if "aggressive_ocr" in repo_cfg:
        if repo_cfg["aggressive_ocr"]:
            return True
    return False


def should_clean(repo=None):
    if not repo:
        repo = get_default_repo()
    repo_cfg, cover_page, logo_path, css_path = get_repo_cfg(repo)
    if "fast_ocr" in repo_cfg:
        if repo_cfg["fast_ocr"] and unpaper_path:
            return True
    return False


def should_deskew(repo=None):
    if not repo:
        repo = get_default_repo()
    repo_cfg, cover_page, logo_path, css_path = get_repo_cfg(repo)
    if "fast_ocr" in repo_cfg:
        if repo_cfg["fast_ocr"]:
            return True
    return False


def should_optimize(repo=None):
    if not repo:
        repo = get_default_repo()
    repo_cfg, cover_page, logo_path, css_path = get_repo_cfg(repo)
    if "pdf_optimization" in repo_cfg:
        if pngquant_path:
            return repo_cfg["pdf_optimization"]
    return 0


def should_force_ocr(repo=None):
    if not repo:
        repo = get_default_repo()
    repo_cfg, cover_page, logo_path, css_path = get_repo_cfg(repo)
    if "force_ocr" in repo_cfg:
        return repo_cfg["force_ocr"]
    return False


pdfkit_config = get_pdfkit_config()
default_repo = get_default_repo()
tesseract_path = get_tesseract_path()
poppler_path = get_poppler_path()
pngquant_path = get_pngquant_path()
unpaper_path = get_unpaper_path()
