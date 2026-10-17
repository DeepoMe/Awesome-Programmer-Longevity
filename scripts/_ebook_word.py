# -*- coding: utf-8 -*-
"""电子书 Word 版：ebook_word.html（图片相对路径、details 展开为标题）→ Word COM 转 PDF"""
import pathlib, markdown, re

root = pathlib.Path(__file__).resolve().parent.parent
md_text = (root / "README.md").read_text(encoding="utf-8")

# 条目卡展开：details/summary 在 Word HTML 中不渲染内容——转为标题流
# 条目卡展开：details/summary 在 Word HTML 中不渲染内容——转为标题流
md_text = md_text.replace("<details>", "<details open>")
# 图片改 file:/// 绝对路径（Word HTML 渲染需要）
md_text = md_text.replace("](images/", f"](file:///{root.as_posix()}/images/")

html_body = markdown.markdown(md_text, extensions=["tables"])

# details -> 纯标题结构
html_body = re.sub(
    r'<details open>\s*<summary><b>(.*?)</b>(.*?)</summary>',
    lambda m: f"<h2>{m.group(1)}{m.group(2)}</h2>",
    html_body)
html_body = html_body.replace("</details>", "")

# "关于熊博士"折叠卡同样展开
html_body = html_body.replace(
    '<details open>\n<summary><b>展开：熊博士是谁</b>（姓名 · 机构 · 论文——按需查看）</summary>',
    "<h2>熊博士是谁（姓名 · 机构 · 论文）</h2>")

html = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>程序员续命与长寿指南</title>
<style>
body{{font-family:"Microsoft YaHei";font-size:10.5pt;line-height:1.6;color:#2D2A26;max-width:720px;margin:0 auto}}
h1{{color:#D97E36;font-size:18pt}}
h2{{color:#D97E36;font-size:13pt;border-bottom:1px solid #e5ddd0}}
h3{{color:#2C6E63;font-size:11.5pt}}
table{{border-collapse:collapse;font-size:8.5pt}}
th,td{{border:1px solid #e0d8ca;padding:3pt 5pt}}
th{{background:#FBF3E8}}
blockquote{{border-left:3pt solid #D97E36;background:#FBF3E8;margin:6pt 0;padding:5pt 10pt}}
img{{max-width:78%;display:block;margin:6pt auto}}
</style></head><body>
<h1 style="text-align:center;font-size:24pt">程序员续命与长寿指南</h1>
<p style="text-align:center;font-size:14pt"><b>命是可以科学地续的</b></p>
<p style="text-align:center">33 条 · 证据分级 · 真实文献（68 个 PubMed 验证 PMID）</p>
<p style="text-align:center">熊博士 · DeepoMe 深度甲基 · 2026-10 · v1.0</p>
<p style="text-align:center;font-size:8.5pt;color:#888">本指南是健康教育内容，不构成医疗建议；有疾病请就医。CC BY-NC-SA 4.0</p>
<hr>
{html_body}
</body></html>"""

out = root / "ebook_word.html"
out.write_text(html, encoding="utf-8")
print("OK", out.name, out.stat().st_size // 1024, "KB")
