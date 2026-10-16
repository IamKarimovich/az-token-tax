// Step 2: count tokens with six tokenizers (all vocabularies ship inside the npm packages).
import fs from "fs";
import { fromPreTrained as qwen } from "@lenml/tokenizer-qwen2_5";
import { fromPreTrained as gemma } from "@lenml/tokenizer-gemma3";
import { fromPreTrained as deepseek } from "@lenml/tokenizer-deepseek_v3";
import * as o200k from "gpt-tokenizer/encoding/o200k_base";
import * as cl100k from "gpt-tokenizer/encoding/cl100k_base";
import llama3 from "llama3-tokenizer-js";

const corpus = JSON.parse(fs.readFileSync("data/corpus.json", "utf8"));
const q = qwen(), g = gemma(), d = deepseek();
const noSpecial = { add_special_tokens: false };

const tokenizers = {
  "GPT-4o": s => o200k.encode(s),
  "GPT-4": s => cl100k.encode(s),
  "Llama 3": s => llama3.encode(s, { bos: false, eos: false }),
  "Qwen 2.5": s => q.encode(s, noSpecial),
  "Gemma 3": s => g.encode(s, noSpecial),
  "DeepSeek-V3": s => d.encode(s, noSpecial),
};

const results = {};
for (const [name, encode] of Object.entries(tokenizers)) {
  results[name] = {};
  for (const [lang, text] of Object.entries(corpus)) {
    const row = { total: encode(text.full).length };
    if (text.articles) row.articles = text.articles.map(a => encode(a).length);
    results[name][lang] = row;
  }
  console.log(`${name.padEnd(12)} az=${results[name].az_latn.total}  en=${results[name].en.total}`);
}

// How a few words are split, for the write-up.
const words = ["Azərbaycan", "ləyaqət", "bərabərlik", "dövlət", "məsuliyyət", "proqramlaşdırma"];
const splits = {
  "GPT-4o": w => o200k.encode(" " + w).map(i => o200k.decode([i])),
  "Qwen 2.5": w => q.encode(" " + w, noSpecial).map(i => q.decode([i])),
  "Gemma 3": w => g.encode(" " + w, noSpecial).map(i => g.decode([i])),
};
const examples = {};
for (const [name, split] of Object.entries(splits))
  examples[name] = Object.fromEntries(words.map(w => [w, split(w).join("|")]));

fs.mkdirSync("results", { recursive: true });
fs.writeFileSync("results/tokens_js.json", JSON.stringify(results));
fs.writeFileSync("results/word_splits.json", JSON.stringify(examples, null, 1));
console.log("Saved results/tokens_js.json");
