# -*- coding: utf-8 -*-
"""生成审查视图 _review.html：README + 内嵌图片 + 折叠卡可展开"""
import base64, pathlib, markdown

root = pathlib.Path(__file__).resolve().parent.parent
md_text = (root / "README.md").read_text(encoding="utf-8")

# 图片内嵌为 base64（自包含单文件，双击即看）
import re
def embed(m):
    alt, rel = m.group(1), m.group(2)
    p = root / rel
    if not p.exists():
        return f"![{alt}](缺失:{rel})"
    ext = "png"
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"![{alt}](data:image/{ext};base64,{b64})"

md_text = re.sub(r"!\[([^\]]*)\]\((images/[^)]+)\)", embed, md_text)

css = """
<style>
body{font-family:"Microsoft YaHei",-apple-system,sans-serif;max-width:880px;margin:24px auto;
     padding:0 20px;color:#2D2A26;background:#FDFBF7;line-height:1.75}
h1{font-size:1.9em;border-bottom:3px solid #D97E36;padding-bottom:.3em}
h2{font-size:1.45em;color:#D97E36;margin-top:1.8em;border-bottom:1px solid #e5ddd0;padding-bottom:.25em}
h3{font-size:1.15em;color:#2C6E63;margin-top:1.4em}
table{border-collapse:collapse;width:100%;font-size:.92em;margin:1em 0;background:#fff}
th,td{border:1px solid #e0d8ca;padding:7px 10px;text-align:left}
th{background:#FBF3E8}
tr:nth-child(even) td{background:#FCFAF5}
img{max-width:100%;border-radius:8px;margin:10px 0;box-shadow:0 1px 4px rgba(45,42,38,.08)}
details{background:#fff;border:1px solid #e5ddd0;border-radius:10px;margin:12px 0;padding:10px 16px}
details[open]{border-color:#D97E36}
summary{cursor:pointer;font-size:1.04em;font-weight:600;color:#2D2A36}
summary::marker{color:#D97E36}
blockquote{border-left:4px solid #D97E36;background:#FBF3E8;margin:12px 0;padding:10px 16px;border-radius:0 8px 8px 0}
code{background:#f0ebe0;padding:2px 6px;border-radius:4px;font-size:.92em}
a{color:#2C6E63}
.banner{background:#2C6E63;color:#fff;padding:10px 18px;border-radius:10px;margin-bottom:20px;font-size:.95em}
</style>
"""

html = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>程序员续命与长寿指南 · 全文审查视图</title>{css}</head><body>
<div class="banner">📋 审查视图（本地生成，图片已内嵌）——33 条全部可展开审查 | 双击折叠条目标题展开</div>
{markdown.markdown(md_text, extensions=["tables"])}
</body></html>"""

out = root / "_review.html"
out.write_text(html, encoding="utf-8")
print("OK", out, f"{out.stat().st_size//1024} KB")
