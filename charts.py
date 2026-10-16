"""Step 5: figures -> results/fig1_ratio_to_english.png, results/fig2_schwa_experiment.png"""
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

with open("results/summary.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

names = [r["tokenizer"] for r in rows]
x = np.arange(len(rows))
num = lambda key: np.array([float(r[key]) for r in rows])

plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})

# Figure 1: tokens relative to English
az, tr, ru = num("az_latn/en"), num("tr/en"), num("ru/en")
w = 0.26

fig, ax = plt.subplots(figsize=(10, 5.6), dpi=150)
ax.bar(x - w, az, w, label="Azərbaycan")
ax.bar(x, tr, w, label="Türk")
ax.bar(x + w, ru, w, label="Rus")
ax.axhline(1, color="black", lw=1, ls="--", label="İngilis (=1)")
for xi, v in zip(x, az):
    ax.text(xi - w, v + 0.08, f"{v:.2f}", ha="center", fontsize=8.5)
ax.set_xticks(x, names, rotation=20, ha="right")
ax.set_ylabel("Token sayı / ingilis dilində token sayı")
ax.set_title("Eyni mətnin token sayı, ingilis dilinə nisbətən (UDHR, 8 tokenizer)")
ax.set_ylim(0, 3.4)
ax.grid(axis="y", alpha=0.3)
ax.legend(frameon=False, ncol=4, loc="upper left")
fig.tight_layout()
fig.savefig("results/fig1_ratio_to_english.png")
plt.close(fig)

# Figure 2: effect of replacing "ə" with "e"
change = num("schwa->e change %")
fig, ax = plt.subplots(figsize=(10, 5.2), dpi=150)
ax.bar(x, change, 0.6, color="tab:gray")
for xi, v in zip(x, change):
    ax.text(xi, v - 0.8, f"{v:.1f}%", ha="center", va="top", fontsize=9)
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(x, names, rotation=20, ha="right")
ax.set_ylabel("Token sayının dəyişməsi, %")
ax.set_title("Azərbaycan mətnində “ə” hərfi “e” ilə əvəz edildikdə token sayının dəyişməsi")
ax.set_ylim(min(change) - 5, 3)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig("results/fig2_schwa_experiment.png")
plt.close(fig)
print("Saved results/fig1_ratio_to_english.png and results/fig2_schwa_experiment.png")
