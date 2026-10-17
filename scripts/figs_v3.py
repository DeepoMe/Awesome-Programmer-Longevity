# -*- coding: utf-8 -*-
"""v3：屏幕宵禁图（褪黑素 vs 屏幕光）"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

BG = "#FDFBF7"; INK = "#2D2A26"; AMBER = "#D97E36"; TEAL = "#2C6E63"
GRAY = "#B8B2A7"; SUB = "#6B655C"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei"], "font.family": "sans-serif",
    "axes.unicode_minus": False, "figure.facecolor": BG, "axes.facecolor": BG,
    "text.color": INK, "axes.edgecolor": GRAY, "xtick.color": SUB, "ytick.color": SUB,
})
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")

fig, ax = plt.subplots(figsize=(9.5, 5.0))
t = np.linspace(19, 27, 400)  # 19:00 -> 次日3:00
def mela(peak, width, amp):
    return amp * np.exp(-0.5 * ((t - peak) / width) ** 2)
normal = mela(23.6, 1.55, 1.0)
screen = mela(24.55, 1.5, 0.80)   # 延迟约 1 小时 + 压低
ax.plot(t, normal, color=AMBER, lw=3.2, solid_capstyle="round")
ax.plot(t, screen, color=TEAL, lw=3.0, ls=(0, (5, 2.2)))
ax.text(21.6, 1.045, "纸书夜", fontsize=13.5, fontweight="bold", color=AMBER)
ax.text(25.4, 0.66, "刷屏夜", fontsize=13.5, fontweight="bold", color=TEAL)
# 屏幕时段
ax.axvspan(22.0, 23.0, color=TEAL, alpha=0.13, lw=0)
ax.text(22.5, 1.10, "屏幕 1 小时", fontsize=11, color=TEAL, ha="center")
# 入睡延迟箭头
ax.annotate("", xy=(24.55, 0.06), xytext=(23.6, 0.06),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.7))
ax.text(24.07, 0.135, "入睡延迟", fontsize=11.5, color=INK, ha="center")
ax.set_xlim(19, 27); ax.set_ylim(0, 1.22)
ax.set_xticks([20, 22, 24, 26])
ax.set_xticklabels(["20:00", "22:00", "0:00", "2:00"], fontsize=10)
ax.set_yticks([])
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.tick_params(length=0)
ax.set_title("最后那小时屏幕，偷走的不止一小时", fontsize=18.5,
             fontweight="bold", pad=14, loc="left")
fig.savefig(os.path.join(OUT, "screen_curfew.png"), dpi=190,
            bbox_inches="tight", facecolor=BG, pad_inches=0.25)
print("OK screen_curfew.png")
