# -*- coding: utf-8 -*-
"""fitz.Story: ebook.html -> PDF（A4，系统字体）"""
import fitz, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "ebook.html").read_text(encoding="utf-8")

css = """
body {font-family: Microsoft YaHei; font-size: 9.8pt; color: #2D2A26; line-height: 1.55;}
h1 {color: #D97E36; font-size: 15pt;}
h2 {color: #D97E36; font-size: 12pt;}
h3 {color: #2C6E63; font-size: 10.5pt;}
table {font-size: 8pt;}
th {background-color: #FBF3E8;}
blockquote {background-color: #FBF3E8;}
img {width: 52%;}
"""

story = fitz.Story(html=html, user_css=css)
writer = fitz.DocumentWriter(str(root / "ebook_v1.pdf"))
mediabox = fitz.paper_rect("a4")
where = mediabox + (40, 40, -40, -40)
more = 1
pages = 0
while more:
    dev = writer.begin_page(mediabox)
    more, _ = story.place(where)
    story.draw(dev)
    writer.end_page()
    pages += 1
writer.close()
p = root / "ebook_v1.pdf"
print("OK pages:", pages, "size:", p.stat().st_size // 1024, "KB")
