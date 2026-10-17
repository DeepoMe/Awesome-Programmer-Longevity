# -*- coding: utf-8 -*-
"""生成电子书 HTML（ebook.html）：封面+目录+33 条全展开，供 Edge headless 转 PDF"""
import base64, pathlib, markdown, re, io
from PIL import Image

root = pathlib.Path(__file__).resolve().parent.parent
md_text = (root / "README.md").read_text(encoding="utf-8")

def embed(m):
    alt, rel = m.group(1), m.group(2)
    p = root / rel
    if not p.exists():
        return f"![{alt}](missing:{rel})"
    img = Image.open(p)
    if img.width > 680:  # 电子书降采样
        h = int(img.height * 680 / img.width)
        img = img.resize((680, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=72)
    return f"![{alt}](data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()})"

md_text = re.sub(r"!\[([^\]]*)\]\((images/[^)]+)\)", embed, md_text)

# 电子书：所有 details 展开（details 标签保留 open 属性）
md_text = md_text.replace("<details>", '<details open="open">')

css = """
<style>
@page{size:A4;margin:18mm 16mm}
body{font-family:"Microsoft YaHei",sans-serif;color:#2D2A26;line-height:1.8;font-size:10.5pt}
.cover{page-break-after:always;text-align:center;padding-top:120px}
.cover h1{font-size:26pt;color:#D97E36;border:none}
.cover p{font-size:12pt;color:#6B655C}
h1{font-size:20pt;border-bottom:2.5pt solid #D97E36;padding-bottom:6pt}
h2{font-size:14.5pt;color:#D97E36;page-break-before:auto;margin-top:18pt;border-bottom:.8pt solid #e5ddd0;padding-bottom:4pt}
h3{font-size:12pt;color:#2C6E63}
table{border-collapse:collapse;width:100%;font-size:8.8pt;margin:8pt 0;background:#fff}
th,td{border:.6pt solid #e0d8ca;padding:4pt 6pt;text-align:left}
th{background:#FBF3E8}
img{max-width:86%;display:block;margin:8pt auto;border-radius:6pt}
details{background:#fff;border:.6pt solid #e5ddd0;border-radius:6pt;margin:10pt 0;padding:8pt 12pt;page-break-inside:avoid}
summary{font-size:11.5pt;font-weight:bold;color:#2D2A26}
blockquote{border-left:3pt solid #D97E36;background:#FBF3E8;margin:8pt 0;padding:6pt 12pt;border-radius:0 6pt 6pt 0;font-size:9.8pt}
code{background:#f0ebe0;padding:1pt 4pt;border-radius:3pt;font-size:9.3pt}
a{color:#2C6E63;text-decoration:none}
.toc{page-break-after:always}
</style>
"""

cover = """<div class="cover">
<h1>程序员续命与长寿指南</h1>
<p style="font-size:15pt;margin-top:18px"><b>命是可以科学地续的</b></p>
<p>33 条 · 证据分级 · 真实文献（68 个 PubMed 验证 PMID）</p>
<p style="margin-top:60px">熊博士 · DeepoMe 深度甲基</p>
<p>2026-10 · v1.0 电子书版（内容与 GitHub README 同步）</p>
<p style="margin-top:80px;font-size:9pt;color:#999">本指南是健康教育内容，不构成医疗建议；有疾病请就医。<br>CC BY-NC-SA 4.0</p>
</div>"""

body = markdown.markdown(md_text, extensions=["tables"])

html = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>程序员续命与长寿指南 · 电子书</title>{css}</head><body>
{cover}
{body}
</body></html>"""

out = root / "ebook.html"
out.write_text(html, encoding="utf-8")
print("OK", out, f"{out.stat().st_size//1024} KB")
