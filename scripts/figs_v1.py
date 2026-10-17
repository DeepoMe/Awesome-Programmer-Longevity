# -*- coding: utf-8 -*-
"""续命指南首批配图 3 张（视觉系统 v1）
规范：暖白底/墨色主字/琥珀+深青双色/图内文字关键词级/无图例框/无参考文献进图
输出 images/ 目录，宽 1800px（公众号 2x）
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

# ── 视觉系统 ──
BG = "#FDFBF7"; INK = "#2D2A26"; AMBER = "#D97E36"; TEAL = "#2C6E63"
GRAY = "#B8B2A7"; SUB = "#6B655C"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei"], "font.family": "sans-serif",
    "axes.unicode_minus": False, "figure.facecolor": BG, "axes.facecolor": BG,
    "text.color": INK, "axes.edgecolor": GRAY, "xtick.color": SUB, "ytick.color": SUB,
})
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
os.makedirs(OUT, exist_ok=True)

# ── 图 1：续命十二柱全景 ──
def fig_pillars():
    fig, ax = plt.subplots(figsize=(12, 5.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6.9); ax.axis("off")
    pillars = [
        ("H1", "基因组不稳定", True), ("H2", "端粒损耗", True), ("H3", "表观遗传改变", True),
        ("H4", "蛋白稳态丧失", True), ("H5", "自噬失能", True), ("H6", "营养感知失调", True),
        ("H7", "线粒体功能障碍", True), ("H8", "细胞衰老", True), ("H9", "干细胞耗竭", False),
        ("H10", "细胞间通讯改变", True), ("H11", "慢性炎症", True), ("H12", "菌群失调", True),
    ]
    for i, (h, name, has) in enumerate(pillars):
        col, row = i % 6, i // 6
        x = 0.35 + col * 1.95; base = 1.15 if row == 0 else 0.0
        # 柱体
        body = FancyBboxPatch((x, 0.55 + row * 3.0), 1.35, 1.75,
                              boxstyle="round,pad=0.02,rounding_size=0.10",
                              linewidth=1.6 if has else 1.2,
                              edgecolor=AMBER if has else GRAY,
                              facecolor="#FBF3E8" if has else BG,
                              linestyle="-" if has else (0, (4, 3)))
        ax.add_patch(body)
        # 状态球
        ax.add_patch(Circle((x + 0.675, 2.62 + row * 3.0), 0.115,
                            facecolor=AMBER if has else "none",
                            edgecolor=AMBER if has else GRAY,
                            linewidth=1.4, linestyle="-" if has else (0, (3, 2))))
        ax.text(x + 0.675, 1.72 + row * 3.0, h, ha="center", va="center",
                fontsize=17, fontweight="bold", color=INK if has else SUB)
        ax.text(x + 0.675, 1.12 + row * 3.0, name, ha="center", va="center",
                fontsize=8.6, color=INK if has else SUB)
    ax.text(0.35, 6.52, "续命十二柱", fontsize=21, fontweight="bold", color=INK)
    ax.text(2.62, 6.52, "衰老标志全景", fontsize=11, color=SUB, va="center")
    # 状态图例（一行，仅两种 key）
    ax.plot([0.38], [0.185], marker="o", ms=7.5, color=AMBER)
    ax.text(0.55, 0.185, "有抓手", fontsize=9.5, color=SUB, va="center")
    ax.plot([1.55], [0.185], marker="o", ms=7.5, mfc="none", mec=GRAY, mew=1.3, ls=(0, (3, 2)))
    ax.text(1.72, 0.185, "诚实留白", fontsize=9.5, color=SUB, va="center")
    fig.savefig(os.path.join(OUT, "pillars12.png"), dpi=150, bbox_inches="tight",
                facecolor=BG, pad_inches=0.28)
    plt.close(fig)

# ── 图 2：睡眠债剪刀差（示意） ──
def fig_sleep_debt():
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    d = np.linspace(0, 14, 200)
    obj = 100 - 4.6 * d                      # 客观表现：近线性下滑（示意）
    sub = 62 - 6.5 * (1 - np.exp(-d / 1.6))  # 主观困倦感：平台化（示意）
    ax.plot(d, obj, color=AMBER, lw=3.2, solid_capstyle="round")
    ax.plot(d, sub, color=TEAL, lw=3.2, ls=(0, (5, 2.2)), dash_capstyle="round")
    # 端点关键标注（关键词级）
    ax.annotate("实际表现", xy=(13.2, obj[-25]), xytext=(9.4, 62), fontsize=14,
                fontweight="bold", color=AMBER,
                arrowprops=dict(arrowstyle="-", color=AMBER, lw=1.1))
    ax.annotate("自我感觉", xy=(13.15, sub[-25]), xytext=(9.4, 44), fontsize=14,
                fontweight="bold", color=TEAL,
                arrowprops=dict(arrowstyle="-", color=TEAL, lw=1.1))
    ax.annotate("", xy=(14.1, 36), xytext=(14.1, 57),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    ax.text(14.32, 46.5, "错觉 gap", fontsize=10.5, color=SUB, va="center", rotation=90)
    ax.set_xlim(0, 15.4); ax.set_ylim(0, 105)
    ax.set_xticks([0, 7, 14]); ax.set_xticklabels(["第1天", "第7天", "第14天"], fontsize=11)
    ax.set_yticks([])
    ax.set_xlabel("每晚只睡 6 小时", fontsize=12, color=SUB, labelpad=8)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="x", length=0)
    ax.set_title("睡眠债：越欠越多，感觉越平", fontsize=19, fontweight="bold",
                 color=INK, pad=14, loc="left")
    fig.savefig(os.path.join(OUT, "sleep_debt.png"), dpi=190, bbox_inches="tight",
                facecolor=BG, pad_inches=0.25)
    plt.close(fig)

# ── 图 3：咖啡因半衰期 ──
def fig_caffeine():
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    t = np.linspace(0, 11, 240)  # 14:00 后的小时数
    hours = t + 14
    fast = 100 * 0.5 ** (t / 3.5)   # 快代谢 t1/2≈3.5h（示意偏快）
    mid = 100 * 0.5 ** (t / 5.0)    # 典型 t1/2=5h
    slow = 100 * 0.5 ** (t / 7.0)   # 慢代谢 t1/2=7h
    ax.plot(hours, mid, color=AMBER, lw=3.4, solid_capstyle="round")
    ax.fill_between(hours, fast, slow, color=AMBER, alpha=0.13, lw=0)
    ax.text(20.6, 46, "典型 5h", fontsize=13, fontweight="bold", color=AMBER)
    ax.text(21.8, 22, "个体带", fontsize=10, color=SUB)
    # 关键锚点：19:00 剩一半
    ax.plot([19], [50], marker="o", ms=9, color=INK, zorder=5)
    ax.plot([19, 19], [0, 50], color=GRAY, lw=1.0, ls=(0, (2, 2)))
    ax.plot([14, 19], [50, 50], color=GRAY, lw=1.0, ls=(0, (2, 2)))
    ax.text(18.55, 54, "还剩一半", fontsize=12.5, color=INK, ha="right")
    # 就寝区
    ax.axvspan(22.5, 25, color=TEAL, alpha=0.10, lw=0)
    ax.text(23.75, 90, "就寝", fontsize=12, color=TEAL, ha="center")
    ax.text(23.75, 20, "深睡眠\n被削", fontsize=10.5, color=TEAL, ha="center")
    ax.set_xlim(14, 25.2); ax.set_ylim(0, 102)
    ax.set_xticks([14, 17, 19, 21, 23])
    ax.set_xticklabels(["14:00\n喝下", "17:00", "19:00", "21:00", "23:00"], fontsize=10.5)
    ax.set_yticks([0, 50, 100]); ax.set_yticklabels(["0", "50%", "100%"], fontsize=10.5)
    ax.set_ylabel("血中咖啡因", fontsize=11, color=SUB)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.set_title("下午 2 点那杯咖啡的下半场", fontsize=19, fontweight="bold",
                 color=INK, pad=14, loc="left")
    fig.savefig(os.path.join(OUT, "caffeine.png"), dpi=190, bbox_inches="tight",
                facecolor=BG, pad_inches=0.25)
    plt.close(fig)

if __name__ == "__main__":
    fig_pillars(); fig_sleep_debt(); fig_caffeine()
    for f in sorted(os.listdir(OUT)):
        print("OK", f)
