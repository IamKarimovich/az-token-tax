# Azerbaijani in LLM tokenizers

How many tokens does the same text need in Azerbaijani compared with English, Turkish and Russian?

## Data and method

- **Text:** the Universal Declaration of Human Rights (UDHR) in eight versions: Azerbaijani (Latin and Cyrillic), English, Turkish, Russian, Kazakh, Uzbek (Latin) and German. Source: the NLTK `udhr2` corpus, downloaded automatically by `prep.py`.
- **Tokenizers:** GPT-4o (`o200k_base`), GPT-4 (`cl100k_base`), Llama 3, Qwen 2.5, Gemma 3, DeepSeek-V3, Mistral Tekken, Mistral 7B (SentencePiece v1).
- **Metric:** number of tokens for the text in a language divided by the number of tokens for the English text.
- **Uncertainty:** bootstrap over the 30 articles (5,000 resamples, 95% interval).
- **Control experiment:** the Azerbaijani text with every `ə` replaced by `e`, and with all diacritics removed. These variants are not valid Azerbaijani; they only show how much of the overhead comes from the special letters.

## Requirements

- Python 3.10+
- Node.js 18+

## Run

```bash
pip install -r requirements.txt
npm install
```

Then on Windows:

```
run_all.bat
```

or on Linux/macOS:

```bash
./run_all.sh
```

Results are written to `results/`: `summary.csv` and two figures.

## Limitations

- One corpus and one genre (legal text). News, chat or code-mixed text may give different numbers.
- The translations are not perfectly parallel; the Turkish UDHR uses older and more compact wording.
- Token count reflects API cost and context usage, not model quality.
