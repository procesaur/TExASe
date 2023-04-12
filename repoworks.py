from helper import default_repo, get_repo_cfg
from requests import get


def get_metadata(metadata_id, repo=""):
    if not repo:
        repo = default_repo
    repo_cfg, cover_page, logo_path = get_repo_cfg(repo)

    try:
        metadata_json = get(repo_cfg["api_url"] + metadata_id).json()
    except:
        metadata_json = {}

    citation_string = get_citation_string(repo_cfg["citation_string"], metadata_json)

    metadata = {}
    for x in repo_cfg["basic_metadata_fields"]:
        try:
            metadata[x] = ";".join([y["@value"] for y in metadata_json[repo_cfg["basic_metadata_fields"][x]]])
        except:
            metadata[x] = ""

    return metadata, citation_string


def get_citation_string(format, metadata):
    citation_string = ""
    for x in format:
        if ":" in x:
            try:
                citation_string += ";".join([y["@value"] for y in metadata[x]])
            except:
                pass
        else:
            citation_string += x
    return citation_string
