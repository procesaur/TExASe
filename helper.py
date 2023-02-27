from os import name, remove
from json import load
from os import path as px


def load_conf(path=None):
    if not path:
        path = px.join(px.dirname(__file__), "config.json")
    with open(path, "r", encoding="utf-8") as cf:
        return load(cf)


cfg = load_conf()


def tryDel(file):
    try:
        remove(file)
    except:
        pass


def limit(x, mini, maxi):
    if isinstance(x, str):
        if len(x) > maxi:
            x = x[:maxi]
    else:
        if x < mini:
            x = mini
        if x > maxi:
            x = maxi
    return x


def log_stuff(stuff):
    if "log" in cfg and cfg["log"]:
        try:
            with open(cfg["log"], "a+", encoding="utf-8") as lf:
                lf.write("\t".join([str(x) for x in stuff]) + "\n")
        except:
            pass
