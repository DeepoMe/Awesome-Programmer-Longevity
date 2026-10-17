# -*- coding: utf-8 -*-
"""续命指南配图 v2：剩余 8 条目（视觉系统同 v1）
图内文字关键词级、无参考文献、示意数据方向均与正文一致
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

BG = "#FDFBF7"; INK = "#2D2A26"; AMBER = "#D97E36"; TEAL = "#2C6E63"
GRAY = "#B8B2A7"; SUB = "#6B655C"; LIGHT = "#FBF3E8"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei"], "font.family": "sans-serif",
    "axes.unicode_minus": False, "figure.facecolor": BG, "axes.facecolor": BG,
    "text.color": INK, "axes.edgecolor": GRAY, "xtick.color": SUB, "ytick.color": SUB,
})
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
os.makedirs(OUT, exist_ok=True)

def clean(ax, keep_left=False):
    for s in ["top", "right"] + ([] if keep_left else ["left"]):
        ax.spines[s].set_visible(False)

# ── 005 晨光：节律锚定 vs 漂移（示意） ──
def fig_morning():
    fig, ax = plt.subplots(figsize=(9.5, 5.0))
    t = np.linspace(5, 29, 400)  # 5:00 -> 次日5:00
    def mela(peak, width):
        return np.exp(-0.5 * ((t - peak) / width) ** 2)
    anchored = mela(23.2, 2.0)      # 锚定：23 点左右升起
    drifted = mela(26.3, 2.3)       # 漂移：凌晨 2 点后才升
    ax.plot(t, anchored, color=AMBER, lw=3.2, solid_capstyle="round")
    ax.plot(t, drifted, color=TEAL, lw=3.0, ls=(0, (5, 2.2)))
    ax.text(21.0, 1.06, "晨光锚定", fontsize=13.5, fontweight="bold", color=AMBER)
    ax.text(25.6, 0.62, "晚睡漂移", fontsize=13.5, fontweight="bold", color=TEAL)
    # 晨光箭头：把漂移拉回
    ax.add_patch(FancyArrowPatch((7.2, 0.86), (7.2, 0.13), arrowstyle="-|>",
                                 mutation_scale=17, color=AMBER, lw=2.4))
    ax.text(7.2, 1.02, "晨光 10 分钟", fontsize=11.5, color=AMBER, ha="center")
    ax.set_xlim(5, 29); ax.set_ylim(0, 1.22)
    ticks = [6, 12, 18, 24, 28]
    ax.set_xticks(ticks); ax.set_xticklabels(["6:00", "12:00", "18:00", "0:00", "4:00"], fontsize=10)
    ax.set_yticks([])
    ax.axvspan(24, 28, color=INK, alpha=0.045, lw=0)
    clean(ax); ax.tick_params(length=0)
    ax.set_title("困意信号：被早晨拉住，还是被夜晚拖走", fontsize=18.5,
                 fontweight="bold", pad=14, loc="left")
    fig.savefig(os.path.join(OUT, "morning_light.png"), dpi=190,
                bbox_inches="tight", facecolor=BG, pad_inches=0.25)
    plt.close(fig)

# ── 002 起身闹钟：锯齿 vs 单调下滑（示意） ──
def fig_sit():
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    t = np.linspace(0, 180, 600)
    no_break = 100 * np.exp(-t / 62)
    ax.plot(t, no_break, color=TEAL, lw=3.0)
    # 每 30 分钟起身：锯齿恢复
    tb, yb = [0], [100]
    seg_t = np.linspace(0, 30, 40)
    for k in range(6):
        decay = yb[-1] * np.exp(-(seg_t) / 62)
        tb += list(seg_t + k * 30); yb += list(decay)
        tb.append((k + 1) * 30); yb.append(min(100, yb[-1] * 1.16 + 6))
    ax.plot(tb, yb, color=AMBER, lw=3.0)
    for xm in range(30, 181, 30):
        ax.plot([xm], [2], marker="|", ms=12, color=GRAY)
        ax.plot([xm], [26], marker="^", ms=7, color=AMBER, clip_on=False)
    ax.text(150, 74, "每 30 分钟起身", fontsize=13, fontweight="bold", color=AMBER)
    ax.text(122, 24, "一直坐着", fontsize=13, fontweight="bold", color=TEAL)
    ax.set_xlim(0, 185); ax.set_ylim(0, 108)
    ax.set_xticks([0, 60, 120, 180])
    ax.set_xticklabels(["0 分", "60 分", "120 分", "180 分"], fontsize=10)
    ax.set_yticks([])
    clean(ax); ax.tick_params(length=0)
    ax.set_title("久坐是过程性伤害，起身是分钟级恢复（示意）", fontsize=18,
                 fontweight="bold", pad=14, loc="left")
    fig.savefig(os.path.join(OUT, "sit_break.png"), dpi=190,
                bbox_inches="tight", facecolor=BG, pad_inches=0.25)
    plt.close(fig)

# ── 003 用眼：眨眼频率对比（相对示意，无绝对数字） ──
def fig_blink():
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    bars = [("谈话", 1.0, TEAL), ("盯屏专注", 0.45, AMBER)]
    for i, (lab, h, c) in enumerate(bars):
        ax.bar(i, h, width=0.44, color=c, alpha=0.92, zorder=3)
        ax.text(i, h + 0.035, lab, ha="center", fontsize=13.5,
                fontweight="bold", color=INK)
    ax.annotate("", xy=(1, 0.45), xytext=(1, 1.0),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.8))
    ax.text(1.09, 0.70, "掉一半以上", fontsize=12, color=SUB, rotation=90, va="center")
    ax.text(0.5, 0.50, "眨眼频率", fontsize=15, fontweight="bold",
            color=INK, ha="center", bbox=dict(boxstyle="round,pad=0.32",
            fc=LIGHT, ec=AMBER, lw=1.4))
    ax.set_xlim(-0.55, 1.75); ax.set_ylim(0, 1.16)
    ax.set_xticks([]); ax.set_yticks([])
    clean(ax, keep_left=False)
    ax.set_title("泪膜的定时器，被屏幕按了暂停", fontsize=18.5,
                 fontweight="bold", pad=14, loc="left")
    fig.savefig(os.path.join(OUT, "blink.png"), dpi=190,
                bbox_inches="tight", facecolor=BG, pad_inches=0.25)
    plt.close(fig)

# ── 011 熬夜VC：缓冲一角（示意） ──
def fig_vc():
    fig, ax = plt.subplots(figsize=(9.2, 4.9))
    t = np.linspace(0, 10, 200)
    plain = 100 * (1 + 0.09 * t ** 1.35)
    withvc = 100 * (1 + 0.052 * t ** 1.35)
    ax.plot(t, plain, color=TEAL, lw=3.0)
    ax.plot(t, withvc, color=AMBER, lw=3.0)
    ax.fill_between(t, withvc, plain, color=AMBER, alpha=0.16, lw=0)
    ax.text(6.6, plain[-30] + 5, "熬夜 · 无 VC", fontsize=13, fontweight="bold", color=TEAL)
    ax.text(6.6, withvc[-30] - 16, "熬夜 · 补 VC", fontsize=13, fontweight="bold", color=AMBER)
    ax.text(4.9, 137, "挡住一角", fontsize=12, color=SUB, ha="center")
    ax.set_xlim(0, 10.6); ax.set_ylim(85, 235)
    ax.set_xticks([0, 10]); ax.set_xticklabels(["熬夜开始", "天亮"], fontsize=10.5)
    ax.set_yticks([])
    clean(ax); ax.tick_params(length=0)
    ax.set_ylabel("氧化应激", fontsize=11, color=SUB)
    ax.set_title("VC 是止损垫，不是免死金牌（示意）", fontsize=18.5,
                 fontweight="bold", pad=14, loc="left")
    fig.savefig(os.path.join(OUT, "vc_rescue.png"), dpi=190,
                bbox_inches="tight", facecolor=BG, pad_inches=0.25)
    plt.close(fig)

# ── 008 工学：颈椎负荷阶梯（力学模型方向） ──
def fig_neck():
    fig, ax = plt.subplots(figsize=(9.2, 4.9))
    data = [("0°", 1.0), ("15°", 2.3), ("30°", 3.6), ("45°", 5.2)]
    for i, (lab, v) in enumerate(data):
        c = AMBER if i <= 1 else TEAL
        ax.bar(i, v, width=0.56, color=c, alpha=0.92, zorder=3)
        ax.text(i, v + 0.12, f"{v:.0f}×" if i else "1×", ha="center",
                fontsize=13.5, fontweight="bold", color=INK)
        ax.text(i, -0.42, f"低头 {lab}" if i else "正直", ha="center", fontsize=11.5, color=SUB)
    ax.plot([0.35, 3.35], [1.0, 1.0], color=GRAY, lw=1.1, ls=(0, (3, 2)))
    ax.set_xlim(-0.6, 3.6); ax.set_ylim(0, 6.0)
    ax.set_xticks([]); ax.set_yticks([])
    clean(ax)
    ax.set_title("头每低一寸，脖子多扛几斤（力学模型）", fontsize=18.5,
                 fontweight="bold", pad=14, loc="left")
    fig.savefig(os.path.join(OUT, "neck_load.png"), dpi=190,
                bbox_inches="tight", facecolor=BG, pad_inches=0.25)
    plt.close(fig)

# ── 001 下颌淋巴：引流方向示意（抽象线稿） ──
def fig_lymph():
    fig, ax = plt.subplots(figsize=(7.6, 5.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 11); ax.axis("off")
    # 头颈轮廓（极简）
    theta = np.linspace(-0.15 * np.pi, 1.15 * np.pi, 100)
    ax.plot(5 + 1.9 * np.cos(theta), 8.6 + 2.15 * np.sin(theta), color=INK, lw=2.2)
    ax.plot([4.2, 3.9], [6.6, 4.2], color=INK, lw=2.2)   # 颈左
    ax.plot([5.8, 6.1], [6.6, 4.2], color=INK, lw=2.2)   # 颈右
    ax.plot([3.9, 6.1], [4.2, 4.2], color=INK, lw=2.2)   # 肩线
    # 下颌缘箭头（下巴→耳垂）
    ax.add_patch(FancyArrowPatch((4.55, 6.9), (5.9, 7.35), arrowstyle="-|>",
                 mutation_scale=16, color=AMBER, lw=2.6,
                 connectionstyle="arc3,rad=-0.25"))
    ax.add_patch(FancyArrowPatch((5.45, 6.9), (4.15, 7.35), arrowstyle="-|>",
                 mutation_scale=16, color=AMBER, lw=2.6,
                 connectionstyle="arc3,rad=0.25"))
    # 颈链淋巴结
    for y in (6.15, 5.45, 4.75):
        ax.add_patch(Circle((3.55, y), 0.15, fc=LIGHT, ec=AMBER, lw=1.6))
        ax.add_patch(Circle((6.45, y), 0.15, fc=LIGHT, ec=AMBER, lw=1.6))
    ax.add_patch(FancyArrowPatch((5.75, 7.15), (6.42, 6.4), arrowstyle="-|>",
                 mutation_scale=14, color=TEAL, lw=1.9, connectionstyle="arc3,rad=0.18"))
    ax.add_patch(FancyArrowPatch((4.25, 7.15), (3.58, 6.4), arrowstyle="-|>",
                 mutation_scale=14, color=TEAL, lw=1.9, connectionstyle="arc3,rad=-0.18"))
    ax.text(5.0, 10.35, "轻 1-2 分钟", fontsize=15, fontweight="bold", ha="center")
    ax.text(5.0, 3.35, "下颌缘 → 颈深链", fontsize=12, color=SUB, ha="center")
    ax.text(1.15, 9.4, "大脑代谢废物", fontsize=10.5, color=SUB)
    ax.add_patch(FancyArrowPatch((1.05, 9.0), (2.9, 8.2), arrowstyle="-|>",
                 mutation_scale=13, color=GRAY, lw=1.5))
    ax.set_title("方向对，力度轻", fontsize=18.5, fontweight="bold", pad=10, loc="left")
    fig.savefig(os.path.join(OUT, "lymph_drain.png"), dpi=190,
                bbox_inches="tight", facecolor=BG, pad_inches=0.25)
    plt.close(fig)

# ── 009 番茄钟：强制暂停协议 ──
def fig_pomodoro():
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    # 方波：25 专注 / 5 休息 ×3
    seg = [(0, 25, 1), (25, 30, 0.15), (30, 55, 1), (55, 60, 0.15), (60, 85, 1), (85, 90, 0.15)]
    for a, b, v in seg:
        ax.fill_between([a, b], 0, v, color=AMBER if v > 0.5 else TEAL,
                        alpha=0.88 if v > 0.5 else 0.55, lw=0, step="mid")
    # BRAC 慢波
    t = np.linspace(0, 90, 300)
    brac = 0.55 + 0.16 * np.sin(2 * np.pi * t / 90 - np.pi / 2)
    ax.plot(t, brac, color=INK, lw=1.8, ls=(0, (4, 2.4)), alpha=0.75)
    ax.text(37, 1.10, "专注 25", fontsize=12.5, fontweight="bold", color=AMBER)
    ax.text(27.5, -0.14, "休 5", fontsize=11, color=TEAL, ha="center")
    ax.text(88, 0.83, "90 分钟慢波", fontsize=10.5, color=SUB, ha="right")
    ax.set_xlim(-2, 92); ax.set_ylim(-0.3, 1.28)
    ax.set_xticks([0, 30, 60, 90]); ax.set_yticks([])
    clean(ax); ax.tick_params(length=0)
    ax.set_title("强制暂停协议：节律本身就是价值", fontsize=18.5,
                 fontweight="bold", pad=14, loc="left")
    fig.savefig(os.path.join(OUT, "pomodoro.png"), dpi=190,
                bbox_inches="tight", facecolor=BG, pad_inches=0.25)
    plt.close(fig)

# ── 006 Zone2：三区一带 ──
def fig_zone2():
    fig, ax = plt.subplots(figsize=(9.6, 4.3))
    zones = [("热身", 0, 2.6, "#EDE6D6", SUB), ("Zone 2", 2.6, 5.2, AMBER, INK), ("无氧", 5.2, 8, "#D8E2DF", SUB)]
    for name, a, b, c, tc in zones:
        ax.axvspan(a, b, color=c, alpha=0.95 if name == "Zone 2" else 0.55, lw=0)
        ax.text((a + b) / 2, 0.62, name, ha="center", fontsize=15,
                fontweight="bold" if name == "Zone 2" else "normal",
                color="white" if name == "Zone 2" else tc)
    ax.text(3.9, 0.30, "能说话 · 唱不了歌", ha="center", fontsize=14,
            color="white", fontweight="bold")
    ax.annotate("每周 3-5 次 · 30-45 分钟", xy=(3.9, 0.86), ha="center",
                fontsize=11.5, color=INK,
                xytext=(3.9, 0.90))
    ax.set_xlim(0, 8); ax.set_ylim(0, 1.05)
    ax.set_xticks([]); ax.set_yticks([])
    ax.axis("off")
    ax.set_title("线粒体的训练课，在最便宜的那一档", fontsize=18.5,
                 fontweight="bold", pad=8, loc="left")
    fig.savefig(os.path.join(OUT, "zone2.png"), dpi=190,
                bbox_inches="tight", facecolor=BG, pad_inches=0.25)
    plt.close(fig)

if __name__ == "__main__":
    fig_morning(); fig_sit(); fig_blink(); fig_vc()
    fig_neck(); fig_lymph(); fig_pomodoro(); fig_zone2()
    print("v2 done:", sorted(os.listdir(OUT)))
