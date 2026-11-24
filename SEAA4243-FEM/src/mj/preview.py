import pathlib, json, re, sys
from playwright.sync_api import sync_playwright
from PIL import Image
root=pathlib.Path(sys.argv[1])
deck=json.loads((root/'project/deck.json').read_text())
secs=[]
# show uploaded images from their local copies (matched by sha256), so the preview is complete
import hashlib
bs = json.loads((root/'_blobsha.json').read_text()) if (root/'_blobsha.json').exists() else {}
loc = {hashlib.sha256(f.read_bytes()).hexdigest(): f for f in list((pathlib.Path(__file__).parent/'web_img').glob('*.png'))}
for sid in deck['order']:
    s=(root/f'project/slides/{sid}.html').read_text()
    s=re.sub(r'<aside>.*?</aside>','',s,flags=re.S)
    s=re.sub(r'<section id="([^"]+)" data-transition="[^"]+" style="', r'<section id="\1" style="position:relative;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden;', s, count=1)
    s=re.sub(r'/_blob/([0-9a-f]{32})', lambda m: ('file://'+str(loc[bs[m.group(1)]].resolve())) if m.group(1) in bs and bs[m.group(1)] in loc else m.group(0), s)
    secs.append(s)
css='''body{margin:0;background:#888;font-family:"IBM Plex Sans",Arial,sans-serif} section{margin:0 0 8px 0} h1,h2,h3,p,ul{margin:0} ul{padding-left:1.1em} h1,h2,h3{font-weight:600}
table{border-collapse:collapse;width:100%} td,th{border:1px solid #ddd;padding:0.35em 0.6em;text-align:left;vertical-align:top} th{font-weight:600}
x-shape[kind=arrow-right]{display:block;clip-path:polygon(0 25%,60% 25%,60% 0,100% 50%,60% 100%,60% 75%,0 75%)} img{display:block} svg{display:block}'''
sys.path.insert(0, str(pathlib.Path(__file__).parent)); from fontcss import font_css; css=font_css()+css
html=f'<html><head><style>{css}</style></head><body>'+''.join(secs)+'</body></html>'
(root/'_preview.html').write_text(html)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080}); pg.goto('file://'+str(root/'_preview.html')); pg.wait_for_timeout(500); pg.evaluate('document.fonts.ready')
    pg.screenshot(path=str(root/'_full.png'), full_page=True); b.close()
im=Image.open(root/'_full.png'); n=len(deck['order'])
for i in range(n):
    im.crop((0,i*1088,1920,i*1088+1080)).save(root/f'_s{i+1:02d}.png')
# contact sheets of 6 (2x3) at 1/3 scale
k=0; sheet=0
while k<n:
    sh=Image.new('RGB',(2*640+30,3*360+40),'#666')
    for j in range(6):
        if k+j>=n: break
        t=Image.open(root/f'_s{k+j+1:02d}.png').resize((640,360))
        sh.paste(t,((j%2)*650+10,(j//2)*370+10))
    sh.save(root/f'_sheet{sheet}.png'); sheet+=1; k+=6
print('sheets',sheet)
