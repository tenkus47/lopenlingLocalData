from pathlib import Path

import requests

DATA_PATH = Path(__file__).resolve().parent
OUTPUT = DATA_PATH / "chonjuk"

config = {
    "text_title": "བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ་བཞུགས་སོ།",
    "url_template": "https://raw.githubusercontent.com/OpenPecha-Data/{pecha_id}/{view}/{file_name}.txt",
    "versions": {
        "Dominant": {
            "pecha": "O2FCA4A99",
            "branch": "export-lopenling",
            "has_layout": False,
        },
        "སྡེ་དགེ": {
            "pecha": "DF8F32338",
            "branch": "export-lopenling",
            "has_layout": True,
        },
        "སྣར་ཐང": {
            "pecha": "D9755B799",
            "branch": "export-lopenling",
            "has_layout": True,
        },
        "པེ་ཅིན": {
            "pecha": "D0A20E299",
            "branch": "export-lopenling",
            "has_layout": True,
        },
        "ཅོ་ནེ": {},
    },
}


def download_file(url, output_path):
    print(url)
    r = requests.get(url)

    if r.status_code != requests.codes.OK:
        raise f"Failed to download, {url}"

    output_path.write_text(r.text)


def get_text_file_url(version, file_name):
    text_file_url = config["url_template"].format(
        pecha_id=config["versions"][version]["pecha"],
        view=config["versions"][version]["branch"],
        file_name=file_name,
    )
    return text_file_url


def download_version(version):
    if not config["versions"][version]:
        return

    version_output_path = OUTPUT / version
    version_output_path.mkdir(exist_ok=True, parents=True)

    text_file_name = config["text_title"]
    text_file_path = version_output_path / f"{text_file_name}.txt"

    text_file_url = get_text_file_url(version, text_file_name)
    download_file(text_file_url, text_file_path)

    if not config["versions"][version]["has_layout"]:
        return

    text_file_name = f"{config['text_title']}_layout"
    text_file_path = version_output_path / f"{text_file_name}.txt"
    text_file_url = get_text_file_url(version, text_file_name)
    download_file(text_file_url, text_file_path)


def main():
    for version in config["versions"]:
        download_version(version)


if __name__ == "__main__":
    main()
