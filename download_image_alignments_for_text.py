from pathlib import Path

import requests

DATA_PATH = Path(__file__).resolve().parent
ALIGNMENTS_PATH = DATA_PATH / "alignments"

config = {
    "text_title": "བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ་བཞུགས་སོ།",
    "url_template": "https://raw.githubusercontent.com/OpenPecha-Data/{repo}/{branch}/{repo}.json",
    "versions": {
        "Dominant": {
        },
        "སྡེ་དགེ": {
            "pecha": "DF8F32338",
            "branch": "alignment-image",
        },
        "སྣར་ཐང": {
            "pecha": "D9755B799",
            "branch": "alignment-image",
        },
        "པེ་ཅིན": {
            "pecha": "D0A20E299",
            "branch": "alignment-image",
        },
        "ཅོ་ནེ": {},
    }
}

TEXT_PATH = ALIGNMENTS_PATH / config["text_title"]
TEXT_PATH.mkdir(exist_ok=True, parents=True)

def download_file(url, output_path):
    print(url)
    r = requests.get(url)

    if r.status_code != requests.codes.OK:
        raise f"Failed to download, {url}"

    output_path.write_text(r.text)

def get_text_file_url(version, file_name):
    text_file_url = config["url_template"].format(
        repo=config["versions"][version]["pecha"],
        branch=config["versions"][version]["branch"],
        file_name=file_name
    )
    return text_file_url


def download_version_image_alignment(version):
    if not config["versions"][version]:
        return

    text_file_name = f"{version}.json"
    text_file_path = TEXT_PATH / text_file_name

    text_file_url = get_text_file_url(version, text_file_name)
    download_file(text_file_url, text_file_path)

def main():
    for version in config["versions"]:
        download_version_image_alignment(version)

if __name__ == "__main__":
    main()
