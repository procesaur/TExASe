from os import name, remove


def isWindows():
    return name == 'nt'


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