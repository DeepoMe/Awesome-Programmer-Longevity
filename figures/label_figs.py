# 给正文配图叠加英文关键词（原图在 figures/_raw/，重跑本脚本即可再生成）
from PIL import Image, ImageDraw, ImageFont
F='/usr/share/fonts/google-noto-vf/NotoSans[wght].ttf'
INK=(46,58,70)
# 每项：(文字, 标签中心x, y, 指向x, 指向y) —— 坐标为图宽/高的比例；无指向填 None
L={
'fig-20-20-20.jpg':[('20 ft',.12,.12,.07,.38),('tear film',.62,.94,.69,.6)],
'fig-40hz-gamma.jpg':[('40 Hz',.07,.12,.09,.4),('gamma',.33,.92,.33,.45),('amyloid',.62,.95,.6,.64)],
'fig-apoe4.jpg':[('non-carrier',.27,.96,None,None),('APOE4',.73,.96,None,None),('faster use',.92,.28,.85,.42)],
'fig-attention-inflammation.jpg':[('vagus',.8,.3,.58,.36),('distracted',.3,.97,.39,.83),('attending',.68,.97,.62,.82)],
'fig-baduanjin-fascia.jpg':[('fascia',.93,.12,.84,.3),('muscle',.93,.9,.8,.62)],
'fig-big-rocks.jpg':[('big rocks',.3,.5,.6,.55),('sand',.3,.25,.69,.2)],
'fig-caffeine.jpg':[('2 PM',.12,.12,None,None),('bedtime',.72,.12,None,None)],
'fig-emotion-telomere.jpg':[('telomere',.13,.06,.09,.2),('stress',.48,.08,.56,.13),('shorter',.86,.93,.86,.72)],
'fig-ergonomics.jpg':[('neck load',.1,.15,.3,.24),('laptop stand',.47,.94,.58,.72)],
'fig-ergothioneine.jpg':[('ergothioneine',.6,.08,.55,.2),('OCTN1',.82,.9,.8,.62)],
'fig-face-age.jpg':[('visible',.19,.96,None,None),('thermal',.5,.96,None,None),('AI + omics',.81,.96,None,None)],
'fig-face-neck-lymph.jpg':[('cervical lymphatics',.2,.6,.48,.6),('lymph nodes',.25,.78,.53,.64),('stroke down',.88,.25,.62,.55)],
'fig-flow.jpg':[('interruption',.9,.25,.75,.47),('flow',.55,.94,.58,.72)],
'fig-ganmai-wheatgerm.jpg':[('wheat germ',.6,.92,.62,.72),('spermidine',.52,.2,.72,.52),('autophagy',.62,.06,.8,.3)],
'fig-glynac.jpg':[('glycine',.86,.14,.73,.39),('NAC',.5,.93,.6,.6)],
'fig-hallmarks.jpg':[(f'H{i+1}',x,.04,None,None) for i,x in enumerate([.133,.194,.25,.306,.364,.417,.578,.633,.694,.75,.806,.867])],
'fig-meditation.jpg':[('telomerase',.66,.1,.53,.12),('less stress',.17,.25,.27,.35)],
'fig-memory-dna-break.jpg':[('DNA break',.17,.93,.17,.55),('repair',.47,.93,.5,.6),('memory circuit',.84,.93,.83,.75)],
'fig-methylation-clock.jpg':[('young',.1,.6,.19,.66),('old',.93,.45,.76,.35),('methyl marks',.86,.92,.66,.85)],
'fig-morning-light.jpg':[('morning light',.15,.1,None,None),('night screen',.65,.1,.66,.47)],
'fig-nac-mucus.jpg':[('NAC',.46,.2,.38,.3),('S–S bonds',.1,.85,.153,.365),('cilia',.66,.95,.87,.78)],
'fig-new-warming-menu.jpg':[('traditional',.4,.94,None,None),('new',.6,.94,None,None)],
'fig-nuts.jpg':[('~28 g',.86,.4,.62,.55)],
'fig-offload.jpg':[('overload',.1,.95,None,None),('offload',.47,.12,.38,.3)],
'fig-omega3.jpg':[('fish oil',.6,.25,.65,.5),('olive oil',.92,.3,.83,.47)],
'fig-pomodoro.jpg':[('focus',.17,.18,.06,.32),('break',.16,.67,.16,.56)],
'fig-pqq-evidence.png':[('cells',.17,.94,None,None),('mice',.39,.77,None,None),('small RCTs',.61,.6,None,None),('large RCTs?',.83,.5,None,None)],
'fig-screen-curfew.jpg':[('blue light',.2,.06,.3,.33)],
'fig-singing-bowl.jpg':[('relaxation',.14,.12,None,None)],
'fig-sleep-debt.jpg':[('"I\'m fine"',.12,.92,.06,.45),('sleep debt',.85,.92,.95,.72)],
'fig-spermidine.jpg':[('spermidine',.3,.08,.3,.25),('autophagy',.93,.18,.79,.33)],
'fig-standup.jpg':[('idle',.38,.97,.42,.7),('active',.88,.97,.84,.66)],
'fig-vinegar-acetate.jpg':[('vinegar',.26,.07,.15,.14),('gut bacteria',.55,.94,.45,.8),('acetate',.76,.75,.75,.6)],
'fig-vitamin-c.jpg':[('vitamin C',.76,.12,.62,.35),('sleep loss',.17,.15,.31,.15)],
'fig-yangqi-mitochondria.jpg':[('heat',.5,.25,None,None),('ATP',.5,.5,None,None),('mitophagy',.5,.8,None,None)],
'fig-zone2.jpg':[('can talk',.51,.15,None,None),('more mitochondria',.66,.95,.88,.72)],
}
def draw(name,items):
    im=Image.open('figures/_raw/'+name).convert('RGBA'); W,H=im.size
    s=W/1376; f=ImageFont.truetype(F,int(26*s)); f.set_variation_by_axes([600])
    ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    for t,x,y,tx,ty in items:
        cx,cy=x*W,y*H; b=d.textbbox((0,0),t,font=f); w,h=b[2]-b[0],b[3]-b[1]
        px,py=14*s,8*s; box=[cx-w/2-px,cy-h/2-py,cx+w/2+px,cy+h/2+py]
        box=[max(4,box[0]),max(4,box[1]),min(W-4,box[2]),min(H-4,box[3])] if False else box
        dx=max(0,4-box[0])+min(0,W-4-box[2]); dy=max(0,4-box[1])+min(0,H-4-box[3])
        box=[box[0]+dx,box[1]+dy,box[2]+dx,box[3]+dy]; cx+=dx; cy+=dy
        if tx is not None:
            X,Y=tx*W,ty*H; d.line([(cx,cy),(X,Y)],fill=INK+(200,),width=max(2,int(2*s)))
            r=5*s; d.ellipse([X-r,Y-r,X+r,Y+r],fill=INK+(230,))
        d.rounded_rectangle(box,radius=(box[3]-box[1])/2,fill=(255,255,255,225),outline=INK+(90,),width=1)
        d.text((cx-w/2-b[0],cy-h/2-b[1]),t,font=f,fill=INK+(255,))
    out=Image.alpha_composite(im,ov).convert('RGB')
    out.save('figures/'+name,quality=92) if name.endswith('.jpg') else out.save('figures/'+name)
for k,v in L.items(): draw(k,v)
print(len(L))
