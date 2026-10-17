# -*- coding: utf-8 -*-
"""电子书 v2（论文同款管线）：README.md → python-docx 构建 docx → WPS COM 导 PDF
图片全部本地路径直插（不走 HTML/base64）"""
import os, re, sys
from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

BASE = Path(__file__).resolve().parent.parent
MD = BASE / "README.md"
DOCX = BASE / "ebook_v2.docx"
PDF = BASE / "ebook_v1.pdf"

INK = RGBColor(0x2D, 0x2A, 0x26)
AMBER = RGBColor(0xD9, 0x7E, 0x36)
TEAL = RGBColor(0x2C, 0x6E, 0x63)
GRAY = RGBColor(0x6B, 0x65, 0x5C)

def set_font(run, size=10.5, color=INK, bold=False, name="Microsoft YaHei"):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)

INLINE_A = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BOLD = re.compile(r"\*\*([^*]+)\*\*")

def add_rich(par, text, size=10.5, color=INK):
    text = BOLD.sub(r"\1", text)
    text = INLINE_A.sub(lambda m: f"{m.group(1)}（{m.group(2)}）" if m.group(2).startswith("http") else m.group(1), text)
    text = text.replace("`", "")
    r = par.add_run(text)
    set_font(r, size=size, color=color)

doc = Document()
for s in doc.sections:
    s.page_width, s.page_height = Inches(8.27), Inches(11.69)  # A4
    s.left_margin = s.right_margin = Inches(0.7)
    s.top_margin = s.bottom_margin = Inches(0.65)

# 封面
for txt, sz, col, bold, center in [
    ("程序员续命与长寿指南", 26, AMBER, True, True),
    ("命是可以科学地续的", 15, INK, True, True),
    ("33 条 · 证据分级 · 真实文献（68 个 PubMed 验证 PMID）", 11, GRAY, False, True),
    ("熊博士 · DeepoMe 深度甲基", 11, INK, False, True),
    ("2026-10 · v1.0 电子书版（与 GitHub 同步）", 10, GRAY, False, True),
    ("本指南是健康教育内容，不构成医疗建议；有疾病请就医。CC BY-NC-SA 4.0", 8, GRAY, False, True),
]:
    p = doc.add_paragraph()
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(txt)
    set_font(r, size=sz, color=col, bold=bold)
doc.add_page_break()

lines = MD.read_text(encoding="utf-8").splitlines()
i, n = 0, len(lines)
while i < n:
    ln = lines[i]

    if ln.strip() in ("---", "<!-- MORE22 -->"):
        i += 1; continue
    if ln.startswith("<details"):
        i += 1; continue
    if ln.startswith("</details>"):
        i += 1; continue
    m = re.match(r"<summary><b>(.*?)</b>(.*?)</summary>", ln.strip())
    if m:
        p = doc.add_paragraph()
        r = p.add_run(f"{m.group(1)} {m.group(2)}")
        set_font(r, size=12.5, color=AMBER, bold=True)
        p.paragraph_format.space_before = Pt(14)
        i += 1; continue
    if ln.strip().startswith("<"):
        i += 1; continue

    if ln.startswith("### "):
        p = doc.add_paragraph(); add_rich(p, ln[4:], size=11.5, color=TEAL); i += 1; continue
    if ln.startswith("## "):
        p = doc.add_paragraph(); add_rich(p, ln[3:], size=14, color=AMBER)
        p.paragraph_format.space_before = Pt(18); i += 1; continue
    if ln.startswith("# "):
        p = doc.add_paragraph(); add_rich(p, ln[2:], size=17, color=AMBER); i += 1; continue

    im = re.match(r"!\[([^\]]*)\]\((images/[^)]+)\)", ln.strip())
    if im:
        img = BASE / im.group(2)
        if img.exists():
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.add_run().add_picture(str(img), width=Inches(4.9))
        i += 1; continue

    if ln.startswith("|") and i + 1 < n and set(lines[i + 1].replace("|", "").strip()) <= set("-: "):
        rows = []
        while i < n and lines[i].startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            if not set("".join(cells)) <= set("-: "):
                rows.append(cells)
            i += 1
        if rows:
            t = doc.add_table(rows=len(rows), cols=len(rows[0]))
            t.style = "Table Grid"
            for ri, row in enumerate(rows):
                for ci, cell in enumerate(row):
                    if ci < len(t.rows[ri].cells):
                        c = t.rows[ri].cells[ci]
                        c.text = ""
                        add_rich(c.paragraphs[0], re.sub(r"\*\*", "", cell), size=8.2, color=INK)
            doc.add_paragraph()
        continue

    if ln.startswith("> "):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        add_rich(p, ln[2:], size=9.8, color=GRAY)
        i += 1; continue

    if re.match(r"^\d+\. ", ln) or ln.startswith("- "):
        p = doc.add_paragraph(style="List Bullet" if ln.startswith("- ") else "List Number")
        add_rich(p, re.sub(r"^(\d+\.|-)\s*", "", ln), size=10.5)
        i += 1; continue

    if ln.strip():
        p = doc.add_paragraph()
        add_rich(p, ln, size=10.5)
        p.paragraph_format.space_after = Pt(5)
    i += 1

doc.save(DOCX)
print(f"[DOCX OK] {DOCX.name} {DOCX.stat().st_size//1024}KB")

# ---------- WPS COM 转 PDF（论文18 同款） ----------
import comtypes.client
import comtypes.gen
gen_dir = BASE / "_comtypes_gen"
gen_dir.mkdir(exist_ok=True)
comtypes.client.gen_dir = str(gen_dir)
comtypes.gen.__path__ = [str(gen_dir)]

wps = comtypes.client.CreateObject("KWps.Application")
try:
    d = wps.Documents.Open(str(DOCX), ReadOnly=True)
    d.ExportAsFixedFormat(str(PDF), 17)
    d.Close(False)
finally:
    wps.Quit()
print(f"[PDF OK] {PDF.stat().st_size//1024}KB")
