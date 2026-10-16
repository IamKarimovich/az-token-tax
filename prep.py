"""Step 1: download the UDHR parallel corpus and build data/corpus.json.

The Universal Declaration of Human Rights is taken from the NLTK `udhr2`
corpus. Each language is stored as the full text and as a list of articles
(used later for bootstrap intervals).
"""
import json
import re
import urllib.request
import zipfile
from pathlib import Path

URL = "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/udhr2.zip"
DATA = Path("data")
ZIP = DATA / "udhr2.zip"

LANGS = {
    "az_latn": "azj_latn",
    "az_cyrl": "azj_cyrl",
    "en": "eng",
    "tr": "tur",
    "ru": "rus",
    "kk": "kaz",
    "uz_latn": "uzn_latn",
    "de": "deu",
}

# Lines like "Article 5" / "Maddə 5" separate the articles.
HEADING = re.compile(r"\b([1-9]|[12][0-9]|30)\b")


def split_articles(lines):
    articles, current = [], []
    for line in lines:
        if len(line) < 40 and HEADING.search(line):
            if current:
                articles.append(current)
            current = []
        else:
            current.append(line)
    articles.append(current)
    return ["\n".join(a) for a in articles]


def main():
    DATA.mkdir(exist_ok=True)
    if not ZIP.exists():
        print("Downloading UDHR corpus...")
        urllib.request.urlretrieve(URL, ZIP)

    corpus = {}
    with zipfile.ZipFile(ZIP) as z:
        for key, name in LANGS.items():
            raw = z.read(f"udhr2/{name}.txt").decode("utf-8")
            lines = [l.strip() for l in raw.splitlines() if l.strip()]
            corpus[key] = {"full": "\n".join(lines), "articles": split_articles(lines)}
            print(f"{key:8} {len(corpus[key]['full']):6} chars  "
                  f"{len(corpus[key]['full'].split()):5} words  "
                  f"{len(corpus[key]['articles'])} blocks")

    # Control variants of the Azerbaijani text. They are not valid Azerbaijani;
    # they only test how much the special letters cost.
    az = corpus["az_latn"]["full"]
    ascii_map = str.maketrans("əƏışçğöüİŞÇĞÖÜ", "eEiscgouISCGOU")
    corpus["az_schwa_e"] = {"full": az.replace("ə", "e").replace("Ə", "E")}
    corpus["az_schwa_ae"] = {"full": az.replace("ə", "ä").replace("Ə", "Ä")}
    corpus["az_ascii"] = {"full": az.translate(ascii_map)}

    (DATA / "corpus.json").write_text(json.dumps(corpus, ensure_ascii=False), encoding="utf-8")
    print("Saved data/corpus.json")


if __name__ == "__main__":
    main()
