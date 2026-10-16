"""Step 4: ratios to English, bootstrap intervals and the letter experiment -> results/summary.csv"""
import csv
import json
import random
from pathlib import Path

R = {**json.loads(Path("results/tokens_js.json").read_text()),
     **json.loads(Path("results/tokens_py.json").read_text())}
corpus = json.loads(Path("data/corpus.json").read_text(encoding="utf-8"))
chars = {k: len(v["full"]) for k, v in corpus.items()}
LANGS = ["az_latn", "tr", "ru", "kk", "uz_latn", "de", "az_cyrl"]


def bootstrap(a, b, n=5000, seed=1):
    """95% interval of sum(a)/sum(b), resampling articles."""
    rnd = random.Random(seed)
    k = min(len(a), len(b))
    vals = []
    for _ in range(n):
        idx = [rnd.randrange(k) for _ in range(k)]
        vals.append(sum(a[i] for i in idx) / sum(b[i] for i in idx))
    vals.sort()
    return vals[int(0.025 * n)], vals[int(0.975 * n)]


rows = []
for tok, r in R.items():
    en = r["en"]["total"]
    row = {"tokenizer": tok}
    for lang in LANGS:
        row[f"{lang}/en"] = round(r[lang]["total"] / en, 3)
    lo, hi = bootstrap(r["az_latn"]["articles"], r["en"]["articles"])
    a, e = r["az_latn"]["articles"], r["en"]["articles"]
    k = min(len(a), len(e))
    row["az/en articles only"] = round(sum(a[:k]) / sum(e[:k]), 3)
    row["az/en 95% low"], row["az/en 95% high"] = round(lo, 3), round(hi, 3)
    row["az chars/token"] = round(chars["az_latn"] / r["az_latn"]["total"], 2)
    row["en chars/token"] = round(chars["en"] / en, 2)
    az = r["az_latn"]["total"]
    row["schwa->e change %"] = round(100 * (r["az_schwa_e"]["total"] / az - 1), 1)
    row["no diacritics change %"] = round(100 * (r["az_ascii"]["total"] / az - 1), 1)
    row["cyrillic/latin"] = round(r["az_cyrl"]["total"] / az, 3)
    rows.append(row)

rows.sort(key=lambda x: x["az_latn/en"])
with open("results/summary.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

for x in rows:
    print(f"{x['tokenizer']:14} az/en={x['az_latn/en']:.2f} "
          f"(articles {x['az/en articles only']:.2f}, 95% {x['az/en 95% low']:.2f}-{x['az/en 95% high']:.2f})  tr/en={x['tr/en']:.2f}  "
          f"schwa->e {x['schwa->e change %']:+.1f}%")
print("Saved results/summary.csv")
