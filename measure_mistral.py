"""Step 3: count tokens with the two Mistral tokenizers (files ship with mistral-common)."""
import json
from pathlib import Path

import mistral_common
import sentencepiece as spm
from mistral_common.tokens.tokenizers.tekken import Tekkenizer

files = Path(mistral_common.__file__).parent / "data"
corpus = json.loads(Path("data/corpus.json").read_text(encoding="utf-8"))

tekken = Tekkenizer.from_file(str(files / "tekken_240911.json"))
sp = spm.SentencePieceProcessor(model_file=str(files / "tokenizer.model.v1"))

tokenizers = {
    "Mistral Tekken": lambda s: tekken.encode(s, bos=False, eos=False),
    "Mistral 7B": lambda s: sp.encode(s),
}

results = {}
for name, encode in tokenizers.items():
    results[name] = {}
    for lang, text in corpus.items():
        row = {"total": len(encode(text["full"]))}
        if "articles" in text:
            row["articles"] = [len(encode(a)) for a in text["articles"]]
        results[name][lang] = row
    print(f"{name:14} az={results[name]['az_latn']['total']}  en={results[name]['en']['total']}")

Path("results").mkdir(exist_ok=True)
Path("results/tokens_py.json").write_text(json.dumps(results))
print("Saved results/tokens_py.json")
