# -*- coding: utf-8 -*-
"""网页版电子书：README.md -> ebook.html（手机友好：左右点击翻页/字号可调/目录跳转/夜间模式）
图片相对路径（repo 内/GitHub Pages 均可用）"""
import re, pathlib, markdown

root = pathlib.Path(__file__).resolve().parent.parent
md = (root / "README.md").read_text(encoding="utf-8")

def render(md_txt):
    return markdown.markdown(md_txt, extensions=["tables"])

pages = []  # (title, html)

# 封面
pages.append(("封面", """
<div class="cover">
<h1>程序员续命与长寿指南</h1>
<p class="tag">命是可以科学地续的</p>
<p>33 条 · 证据分级 · 真实文献</p>
<p class="dim">熊博士 · DeepoMe 深度甲基 · 2026-10 · v1.0</p>
<p class="tip">👉 点击屏幕右侧翻页｜中间呼出目录｜右上角调字号</p>
</div>"""))

# 抽取主要区块
def grab(start_pat, end_pat, title):
    global md
    m = re.search(start_pat, md, re.S)
    if not m:
        return
    seg = md[m.start():]
    m2 = re.search(end_pat, seg[len(m.group(0)):])
    chunk = m.group(0) + (seg[len(m.group(0)):m2.start() + len(m.group(0))] if m2 else "")
    pages.append((title, render(chunk)))

# 前言
m = re.search(r"## 前言[\s\S]*?(?=## 证据分级)", md)
if m: pages.append(("前言", render(m.group(0))))
# 分级
m = re.search(r"## 证据分级[\s\S]*?(?=## 连载说明)", md)
if m: pages.append(("证据分级", render(m.group(0))))
# 目录（转为可点击目录，原表保留）
m = re.search(r"## 目录[\s\S]*?(?=## 🌅 续命的一天 · 正文)", md)
if m: pages.append(("目录", render(m.group(0))))
# 十二柱
m = re.search(r"### 🏛️[\s\S]*?(?=## 🌅 续命的一天 · 正文)", md)
if m: pages.append(("十二柱", render(m.group(0))))

# 33 条（details 卡逐条拆页）
cards = re.findall(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>", md, re.S)
for summary, body in cards:
    title = re.sub(r"<[^>]+>", "", summary).split("｜")[0].strip()
    pages.append((title, f"<div class='card'><h2>{re.sub(chr(60)+'[^>]+'+chr(62),'',summary)}</h2>{render(body)}</div>"))

# 尾部
m = re.search(r"## 续命工具箱[\s\S]*$", md)
if m: pages.append(("附录", render(m.group(0))))

sections = []
toc = "".join(
    f"<div class='tocitem' onclick='go({i})'>{i+1}. {t}</div>"
    for i, (t, _) in enumerate(pages))
for i, (t, h) in enumerate(pages):
    sections.append(f"<section class='page' id='p{i}'><div class='pagebody'>{h}</div></section>")

HTML = """<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>程序员续命与长寿指南 · 网页版</title>
<style>
:root{--fs:17px;--bg:#FDFBF7;--ink:#2D2A26;--amber:#D97E36;--teal:#2C6E63;--dim:#6B655C;--card:#fff;--bd:#e5ddd0}
.night{--bg:#1E1B18;--ink:#E8E2D8;--amber:#E8A25E;--teal:#7BB8AC;--dim:#9B948A;--card:#292521;--bd:#3d3831}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--ink);font-family:"Microsoft YaHei",system-ui,sans-serif;
     font-size:var(--fs);line-height:1.9;height:100vh;overflow:hidden}
#book{height:100%;display:flex;flex-direction:column}
header{display:flex;justify-content:space-between;align-items:center;padding:8px 14px;
       border-bottom:1px solid var(--bd);flex-shrink:0}
header .t{color:var(--amber);font-weight:700;font-size:.9em}
header button{background:none;border:1px solid var(--bd);color:var(--ink);border-radius:8px;
       padding:4px 10px;font-size:15px;cursor:pointer;margin-left:6px}
#stage{flex:1;position:relative;overflow:hidden}
.page{position:absolute;inset:0;padding:18px 22px;overflow-y:auto;display:none;
      transform:translateX(0);transition:transform .18s ease}
.page.on{display:block}
.cover{text-align:center;padding-top:16vh}
.cover h1{color:var(--amber);font-size:1.8em}
.cover .tag{font-size:1.15em;margin:14px 0}
.cover .dim{color:var(--dim);margin-top:20px}
.cover .tip{margin-top:8vh;color:var(--teal);font-size:.85em}
h2{color:var(--amber);font-size:1.15em;margin:14px 0 8px;border-bottom:1px solid var(--bd);padding-bottom:4px}
h3{color:var(--teal);font-size:1em;margin:12px 0 6px}
table{border-collapse:collapse;width:100%;font-size:.78em;margin:8px 0;background:var(--card)}
th,td{border:1px solid var(--bd);padding:5px 7px;text-align:left}
th{background:rgba(217,126,54,.12)}
img{max-width:100%;border-radius:10px;margin:10px auto;display:block}
blockquote{border-left:4px solid var(--amber);background:rgba(217,126,54,.08);
           margin:8px 0;padding:8px 12px;border-radius:0 8px 8px 0;font-size:.92em}
a{color:var(--teal)}
.card h2{font-size:1.05em}
footer{display:flex;justify-content:center;align-items:center;gap:18px;padding:8px;
       border-top:1px solid var(--bd);color:var(--dim);font-size:.82em;flex-shrink:0}
footer b{color:var(--amber)}
#nav{position:absolute;top:0;bottom:0;width:33%;z-index:5}
#navL{left:0}#navM{left:33%;width:34%}#navR{right:0}
#toc{position:absolute;top:0;bottom:0;left:-84%;width:84%;max-width:360px;background:var(--card);
     z-index:20;overflow-y:auto;padding:16px;transition:left .2s;border-right:1px solid var(--bd)}
#toc.on{left:0}
.tocitem{padding:9px 10px;border-bottom:1px solid var(--bd);cursor:pointer;font-size:.9em}
.tocitem:active{background:rgba(217,126,54,.15)}
#mask{position:absolute;inset:0;background:rgba(0,0,0,.35);z-index:15;display:none}
#mask.on{display:block}

@media (max-width: 768px){
  :root{--fs:20px}
  .page{padding:14px 15px}
  table{font-size:.86em}
  th,td{padding:7px 9px}
  blockquote{font-size:.96em;padding:10px 12px}
  header button{padding:8px 14px;font-size:17px;margin-left:8px}
  header .t{font-size:.95em}
  footer{font-size:.88em;padding-bottom:calc(10px + env(safe-area-inset-bottom))}
  .tocitem{font-size:1em;padding:13px 12px}
  img{border-radius:8px}
}
</style></head><body>
<div id="book">
<header><span class="t" id="ht">程序员续命与长寿指南</span>
<span><button onclick="fs(-1)">A-</button><button onclick="fs(1)">A+</button>
<button onclick="night()">🌙</button></span></header>
<div id="stage">
__SECTIONS__
<div id="navL" class="" onclick="flip(-1)"></div><div id="navM" onclick="toc()"></div><div id="navR" onclick="flip(1)"></div>
<div id="mask" onclick="toc()"></div>
<div id="toc"><h2>目录</h2>__TOC__</div>
</div>
<footer><span onclick="flip(-1)">‹ 上一页</span><b id="pg">1 / N</b><span onclick="flip(1)">下一页 ›</span></footer>
</div>
<script>
let cur=0,N=__N__;
function show(){document.querySelectorAll('.page').forEach((p,i)=>p.classList.toggle('on',i===cur));
document.getElementById('pg').textContent=(cur+1)+' / '+N;
document.getElementById('ht').textContent=document.querySelectorAll('.page')[cur].dataset.t||'程序员续命与长寿指南';}
function flip(d){cur=Math.max(0,Math.min(N-1,cur+d));show();}
function go(i){cur=i;show();toc();}
function toc(){document.getElementById('toc').classList.toggle('on');document.getElementById('mask').classList.toggle('on');}
function fs(d){let v=parseInt(localStorage.xm_fs3||17)+d*2;v=Math.max(13,Math.min(26,v));
localStorage.xm_fs3=v;document.documentElement.style.setProperty('--fs',v+'px');}
if(localStorage.xm_fs3)document.documentElement.style.setProperty('--fs',localStorage.xm_fs3+'px');
if(localStorage.xm_night==='1')document.body.classList.add('night');
function night(){document.body.classList.toggle('night');
localStorage.xm_night=document.body.classList.contains('night')?'1':'0';}
let sx=0;document.addEventListener('touchstart',e=>sx=e.touches[0].clientX);
document.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-sx;
if(Math.abs(dx)>60)flip(dx<0?1:-1);});
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')flip(1);if(e.key==='ArrowLeft')flip(-1);});
show();
</script></body></html>"""

# 每页 data-t 标题
secs = []
for i, s in enumerate(sections):
    t = pages[i][0]
    secs.append(s.replace("<section ", f"<section data-t='{t}' ", 1))

html = HTML.replace("__SECTIONS__", "\n".join(secs)).replace("__TOC__", toc).replace("__N__", str(len(pages)))
out = root / "ebook.html"
out.write_text(html, encoding="utf-8")
print(f"OK {out.name}: {len(pages)} 页, {out.stat().st_size//1024}KB")
