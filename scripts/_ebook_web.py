# -*- coding: utf-8 -*-
"""网页版电子书：README_ZH.md -> ebook.html（手机友好：左右点击翻页/字号可调/目录跳转/夜间模式）
图片相对路径（repo 内/GitHub Pages 均可用）"""
import re, pathlib, markdown

root = pathlib.Path(__file__).resolve().parent.parent
LANG = __import__('sys').argv[1] if len(__import__('sys').argv) > 1 else 'zh'
if LANG == 'en':
    SRC_NAME, OUT_NAME, LANG_LINK = 'README.md', 'ebook.html', 'ebook-zh.html'
else:
    SRC_NAME, OUT_NAME, LANG_LINK = 'README_ZH.md', 'ebook-zh.html', 'ebook.html'
md = (root / SRC_NAME).read_text(encoding="utf-8")

def render(md_txt):
    return markdown.markdown(md_txt, extensions=["tables"])

pages = []  # (title, html)

# 封面
pages.append(("封面", """
<div class="cover">
<h1>程序员长寿指南</h1>
<p class="tag">命是可以科学地续的</p>
<p>11 章 · 双尺子证据分级 · 105 篇验证文献</p>
<p class="dim">熊博士 · DeepoMe 深度甲基 · 2026-10 · v2.0</p>
<p class="tip">👉 点击左右侧翻页｜滑动也可以｜顶部 A/文 切换语言｜参考文献在节末折叠条</p>
</div>"""))

APPENDIX = ('术语表', '编程比喻对照表', '配图规范', '续命工具箱', '关注与更新', '贡献指南', '关于熊博士', '声明', 'License', '利益冲突')

# 全文按行首 ## 分段(统一处理 CRLF/连载态/手动编辑)
# 目录折叠区(完整目录 details 块)内的段跳过
toc_zone = (0, 0)
mz = re.search(r'<summary><b>&#128214;?📖 完整目录[\s\S]*?</details>', md)
if not mz:
    mz = re.search(r'完整目录[\s\S]*?</details>', md)
if mz:
    toc_zone = (mz.start(), mz.end())

parts = re.split(r'(?m)(?=^## )', md)
pos = 0
for piece in parts:
    pstart = md.find(piece[:60], pos) if piece[:60] else -1
    if pstart < 0:
        pstart = pos
    pos = pstart + len(piece)
    piece = piece.strip()
    if not piece.startswith('## '):
        continue
    if toc_zone[0] <= pstart < toc_zone[1]:
        continue  # 目录区内的章标题段跳过
    m2 = re.match(r'## (.+)', piece)
    name = m2.group(1).strip()
    # 目录页跳过(阅读器自带目录抽屉); 其余照单全收
    if name == '目录':
        continue
    pages.append((name[:18], render(piece)))

# 相邻同名段合并(章头小节表 + 章正文)
merged = []
for title, html in pages:
    if merged and merged[-1][0] == title:
        merged[-1] = (title, merged[-1][1] + html)
    else:
        merged.append((title, html))
pages = merged

sections = []
toc = "".join(
    f"<div class='tocitem' onclick='go({i})'>{i+1}. {t}</div>"
    for i, (t, _) in enumerate(pages))
for i, (t, h) in enumerate(pages):
    sections.append(f"<section class='page' id='p{i}'><div class='pagebody'>{h}</div></section>")

HTML = """<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>程序员长寿指南 · 网页版</title>
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

.page{word-break:break-word;overflow-wrap:break-word}
.page table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}
footer button{padding:10px 16px}
.clickzone{position:absolute;top:56px;bottom:44px;width:30%;z-index:5}
.cz-l{left:0}.cz-r{right:0}
@media (max-width: 768px){.clickzone{top:48px;bottom:52px}}
</style></head><body>
<div id="book">
<header><span class="t" id="ht">程序员长寿指南</span>
<span><button onclick="fs(-1)">A-</button><button onclick="fs(1)">A+</button>
<button onclick="night()">🌙</button>
<button onclick="location.href='__LANG__'">A/文</button></span></header>
<div id="stage">
__SECTIONS__
<div id="navL" class="" onclick="flip(-1)"></div><div id="navM" onclick="toc()"></div><div id="navR" onclick="flip(1)"></div>
<div id="mask" onclick="toc()"></div>
<div id="toc"><h2>目录</h2>__TOC__</div>
</div>
<footer><span onclick="flip(-1)">‹ 上一页</span><b id="pg">1 / N</b><span onclick="flip(1)">下一页 ›</span><div class="clickzone cz-l" onclick="flip(-1)"></div><div class="clickzone cz-r" onclick="flip(1)"></div></footer>
</div>
<script>
let cur=0,N=__N__;
function show(){document.querySelectorAll('.page').forEach((p,i)=>p.classList.toggle('on',i===cur));
document.getElementById('pg').textContent=(cur+1)+' / '+N;
document.getElementById('ht').textContent=document.querySelectorAll('.page')[cur].dataset.t||'程序员长寿指南';}
function flip(d){cur=Math.max(0,Math.min(N-1,cur+d));show();}
function go(i){cur=i;show();toc();}
function toc(){document.getElementById('toc').classList.toggle('on');document.getElementById('mask').classList.toggle('on');}
function fs(d){let v=parseInt(localStorage.xm_fs3||17)+d*2;v=Math.max(13,Math.min(26,v));
localStorage.xm_fs3=v;document.documentElement.style.setProperty('--fs',v+'px');}
if(localStorage.xm_fs3)document.documentElement.style.setProperty('--fs',localStorage.xm_fs3+'px');
if(localStorage.xm_night==='1')document.body.classList.add('night');
function night(){document.body.classList.toggle('night');
localStorage.xm_night=document.body.classList.contains('night')?'1':'0';}
let sx=0,moved=0;
document.addEventListener('touchstart',e=>{sx=e.touches[0].clientX;moved=0;});
document.addEventListener('touchmove',e=>{if(Math.abs(e.touches[0].clientX-sx)>12)moved=1;});
document.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-sx;
if(Math.abs(dx)>60)flip(dx<0?1:-1);});
document.addEventListener('click',e=>{
if(moved)return; if(e.target.closest('button,a,summary,details,#toc,#toc *,header,footer'))return;
const x=e.clientX,w=window.innerWidth;
if(x<w*0.3)flip(-1); else if(x>w*0.7)flip(1);});
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')flip(1);if(e.key==='ArrowLeft')flip(-1);});
show();
</script></body></html>"""

# 每页 data-t 标题
secs = []
for i, s in enumerate(sections):
    t = pages[i][0]
    secs.append(s.replace("<section ", f"<section data-t='{t}' ", 1))

html = HTML.replace("__LANG__", LANG_LINK).replace("__SECTIONS__", "\n".join(secs)).replace("__TOC__", toc).replace("__N__", str(len(pages)))
out = root / OUT_NAME
out.write_text(html, encoding="utf-8")
print(f"OK {out.name}: {len(pages)} 页, {out.stat().st_size//1024}KB")
