# -*- coding: utf-8 -*-
"""GitHub Social preview 卡片 1280x640"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

BG, INK, AMBER, TEAL, DIM = '#FDFBF7', '#2D2A26', '#D97E36', '#2C6E63', '#6B655C'

fig, ax = plt.subplots(figsize=(12.8, 6.4), dpi=200)
fig.patch.set_facecolor(BG)
ax.set_xlim(0, 12.8); ax.set_ylim(0, 6.4)
ax.axis('off')

# 左侧文字区
ax.text(0.9, 5.35, '程序员续命指南', fontsize=54, fontweight='bold', color=AMBER,
        fontfamily='Microsoft YaHei')
ax.text(0.95, 4.62, 'Awesome Programmer Longevity · Extend your runtime',
        fontsize=17, color=TEAL)
ax.text(0.95, 4.18, '命是可以科学地续的', fontsize=15, color=DIM,
        fontfamily='Microsoft YaHei')

# 三卖点胶囊
feats = ['11 章', '双尺子证据分级', '105 篇 PubMed 验证文献']
x = 0.95
for f in feats:
    w = 0.35 + len(f) * 0.235
    ax.add_patch(FancyBboxPatch((x, 3.05), w, 0.62, boxstyle='round,pad=0.06',
                 fc='white', ec=AMBER, lw=1.6))
    ax.text(x + w/2, 3.36, f, fontsize=15, color=INK, ha='center', va='center',
            fontfamily='Microsoft YaHei')
    x += w + 0.35

# 落款
ax.text(0.95, 1.05, '熊博士 · DeepoMe 深度甲基', fontsize=14, color=DIM,
        fontfamily='Microsoft YaHei')
ax.text(0.95, 0.62, 'github.com/DeepoMe/Awesome-Programmer-Longevity', fontsize=11.5, color=TEAL)

# 右侧十二柱简化装饰（琥珀实心+1灰虚=诚实留白）
rng = np.random.default_rng(7)
xs = np.linspace(9.35, 12.15, 6)
for r, ybase in [(0, 1.15), (1, 3.75)]:
    for i, xx in enumerate(xs):
        h = 0.85 + rng.uniform(0, 0.75)
        leave = (r == 0 and i == 2)
        if leave:
            ax.plot([xx, xx], [ybase, ybase + h], color='#C9C2B6', lw=9,
                    ls=(0, (2, 2)), solid_capstyle='round', alpha=0.9)
        else:
            ax.plot([xx, xx], [ybase, ybase + h], color=AMBER, lw=9,
                    solid_capstyle='round', alpha=0.35 + 0.65 * (h - 0.85) / 0.75)
        ax.plot(xx, ybase, 'o', ms=4.5, color=TEAL)

fig.savefig(r'd:\00000___Coding\113--CapoVime\续命指南\awesome-programmer-longevity\images\social_preview.png',
            dpi=200, facecolor=BG, bbox_inches='tight', pad_inches=0.25)
print('OK social_preview.png')
