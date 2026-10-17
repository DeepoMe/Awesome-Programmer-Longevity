# -*- coding: utf-8 -*-
"""v4：22 条新条目卡图（012-033）——一图两用：README 卡内配图 + 公众号封面
模板：左侧编号大字+等级徽章+柱锚；右侧标题+机制钩子一句
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle

BG = "#FDFBF7"; INK = "#2D2A26"; AMBER = "#D97E36"; TEAL = "#2C6E63"
GRAY = "#B8B2A7"; SUB = "#6B655C"; LIGHT = "#FBF3E8"
plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei"], "font.family": "sans-serif",
    "axes.unicode_minus": False, "figure.facecolor": BG,
})
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "heads")
os.makedirs(OUT, exist_ok=True)

ITEMS = [
    ("012", "冥想十分钟", "🟢", "H1·端粒酶↑", "压力轴最硬干预：meta 级证据"),
    ("013", "意想与免疫", "🟡", "H10·神经免疫", "注意力投向患处，炎症走向改变"),
    ("014", "甘麦大枣汤与小麦胚芽", "🟡", "H11/H5", "1800 年前的经方×当代自噬研究"),
    ("015", "写代码与心流", "🟡", "认知·跨界", "中断成本与心流保护"),
    ("016", "脑内内存管理", "🟡", "工作记忆", "写下来就是扩容；练脑软件无效"),
    ("017", "情绪与基因组稳定", "🟢", "H1/H2", "生活压力→端粒加速缩短"),
    ("018", "记忆与基因组断裂重连", "🟡", "H1·基因组", "大脑为写记忆主动折断 DNA 再修复"),
    ("019", "40Hz 声光节拍", "🟡", "神经节律", "MIT gamma 刺激的健脑外推"),
    ("020", "麦角硫因与蘑菇", "🟡", "H7/H11", "长寿维生素的队列证据"),
    ("021", "Omega-3 与干眼", "🟡", "眼表/H11", "证据分裂：可试，别期待奇迹"),
    ("022", "坚果一把", "🟢", "H6·营养感知", "腰果编号的自我救赎"),
    ("023", "APOE4 与长链脂肪酸", "🟡", "H1×H7", "鱼油护脑，因基因而异"),
    ("024", "亚精胺与小麦胚芽", "🟡", "H5·自噬", "延寿胺，人体 RCT 已起步"),
    ("025", "PQQ", "🟡", "H7·线粒体", "线粒体新生的小 RCT 群"),
    ("026", "GlyNAC", "🟡", "H5/H7", "老年补剂组合的 Baylor 系列"),
    ("027", "甲基化时钟", "🟢", "H3·表观遗传", "你的身体年龄谁说了算"),
    ("028", "醋与乙酸", "🟢", "H12·菌群", "同一分子，两条路径"),
    ("029", "八段锦与筋", "🟢🟡🔴", "H4·蛋白稳态", "拉伸、筋膜与'肝主筋'四层递进"),
    ("030", "NAC 与化痰", "🟢", "H11·炎症", "药典老药的 Cochrane 证据"),
    ("031", "颂钵", "🟡🔴", "松弛反应", "初步证据，宣称从严"),
    ("032", "面相与生物年龄", "🟡", "表型时钟", "北大热像时钟+AI 多组学"),
    ("033", "阳气与线粒体", "🔴🟡", "H7·线粒体", "概念映射，认真对待"),
]

GRADE_COLOR = {"🟢": "#3E8E5A", "🟡": "#D9A036", "🔴": "#C05B4D"}

for num, title, grade, pillar, hook in ITEMS:
    fig, ax = plt.subplots(figsize=(9.6, 3.6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 4.5); ax.axis("off")
    # 左侧编号块
    ax.add_patch(FancyBboxPatch((0.30, 0.55), 3.0, 3.4,
                 boxstyle="round,pad=0.03,rounding_size=0.16",
                 fc=LIGHT, ec=AMBER, lw=1.8))
    ax.text(1.80, 2.45, num, ha="center", va="center", fontsize=44,
            fontweight="bold", color=AMBER)
    # 等级徽章（纯色圆+白字，避免 emoji 字形缺失）
    badge = {"🟢": ("实证", "#3E8E5A"), "🟡": ("机制", "#D9A036"),
             "🔴": ("待证", "#C05B4D")}
    bc, bcol = badge.get(grade[0], ("?", GRAY))
    ax.add_patch(Circle((0.74, 3.42), 0.30, fc=bcol, ec="none"))
    ax.text(0.74, 3.42, bc, ha="center", va="center", fontsize=8.5,
            color="white", fontweight="bold")
    # 右侧
    ax.text(3.75, 3.28, title, fontsize=23, fontweight="bold", color=INK,
            va="center")
    ax.text(3.78, 2.55, hook, fontsize=13.5, color=SUB, va="center")
    ax.plot([3.78, 11.55], [1.95, 1.95], color=GRAY, lw=0.9, ls=(0, (3, 3)))
    ax.text(11.55, 1.45, pillar, fontsize=12, color=TEAL, ha="right",
            va="center", fontweight="bold")
    ax.text(3.78, 1.45, "证据走到哪，说到哪", fontsize=10, color=GRAY,
            va="center")
    fig.savefig(os.path.join(OUT, f"head_{num}.png"), dpi=170,
                bbox_inches="tight", facecolor=BG, pad_inches=0.22)
    plt.close(fig)

print("heads done:", len(ITEMS))
