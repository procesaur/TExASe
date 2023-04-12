from helper import get_repo_cfg
from requests import get


def generate_citation_string(cite_format, metadata):
    citation_string = ""
    for x in cite_format:
        if ":" in x:
            try:
                citation_string += ";".join([y["@value"] for y in metadata[x]])
            except:
                pass
        else:
            citation_string += x
    return citation_string


def get_citation_string(metadata_id, repo=""):
    repo_cfg, cover_page, logo_path, css_path = get_repo_cfg(repo)
    try:
        metadata_json = get(repo_cfg["api_url"] + metadata_id).json()
    except:
        metadata_json = {}
    return generate_citation_string(repo_cfg["citation_string"], metadata_json)


def get_metadata(metadata_id, repo=""):
    repo_cfg, cover_page, logo_path = get_repo_cfg(repo)
    return get_metadata_from_url(repo_cfg["api_url"], metadata_id)


def get_metadata_from_url(url, id):
    try:
        return get(url + id).json()
    except:
        return {}