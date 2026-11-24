"""Course home: the six parts, the Explorers with their Python code, progress export/import."""
from sitelib import *
import sitelib
sitelib.AV_BASE = "shared/avatar/"

MAN = code_manifest()


def card(n, slug, topic, part, desc, built):
    tag = "a" if built else "div"; href = f' href="{slug}/index.html"' if built else ""
    return (f'<{tag} class="partcard{"" if built else " soon"}"{href} data-part="{n}"><span class="k">{topic} · {part}</span><b>{topic} — {part.split(" of ")[0].split(" ·")[0]}</b><span class="d">{B(*desc)}</span>'
            + (f'<div class="pb"><i style="width:0"></i></div><span class="pp"><span class="pct">0 %</span> · <span class="last"></span></span><span class="go">{B("Open", "Buka")} →</span>' if built
               else f'<span class="pp">{B("coming", "akan datang")}</span>') + f'</{tag}>')


def excard(k, name, desc, where, pack):
    p = MAN[pack]
    return (f'<div class="partcard excard"><span class="k">Explorer · {B(*where)}</span><b>{name}</b><span class="d">{B(*desc)}</span>'
            f'<div class="cardacts"><a class="btn" href="labs/{k}.html">{B("Open", "Buka")}</a>'
            f'{zip_btn(pack, "code/", "Python code", "Kod Python", "btn ghost")}<span class="savemsg" aria-live="polite"></span></div>'
            f'<span class="pp">{", ".join(p["files"])} · .zip · {kb(p["bytes"])}</span></div>')


groups = {}
for p in COURSE_PARTS: groups.setdefault(p[2], []).append(p)
cards = "".join(f'<div class="topic">{t}</div><div class="parts">' + "".join(card(*p) for p in ps) + '</div>' for t, ps in groups.items())
labs = "".join(excard(*e) for e in EXPLORERS)
allp = MAN["all"]

body = f'''
<div class="wrap">
<header class="top">
  <div>
    <nav class="crumbs" aria-label="Breadcrumb"><a class="homelink" href="https://people.utm.my/arazin/for-my-students/">For My Students</a><span class="sep" aria-hidden="true">›</span><a class="homelink" href="../" data-pages-only hidden>My Lectures</a><span class="sep" aria-hidden="true" data-pages-only hidden>›</span><span class="cur" aria-current="page">SEAA 4243</span></nav>
    <div class="eyebrow">SEAA 4243 · {B("Faculty of Civil Engineering, UTM", "Fakulti Kejuruteraan Awam, UTM")}</div>
    <h1>SEAA 4243 Finite Element Method</h1>
    <p class="sub">{B("Two-dimensional problems: heat transfer and plane stress in five sessions, then one session with ANSYS. Each part has notes, slides, worked examples in answer-scheme form, exercises and an interactive Explorer.", "Masalah dua dimensi: heat transfer dan plane stress dalam lima sesi, kemudian satu sesi dengan ANSYS. Setiap bahagian ada nota, slides, contoh bekerja dalam bentuk skema jawapan, latihan dan Explorer interaktif.")}</p>
  </div>
  <div class="tools">
    <div class="seg" role="group" aria-label="Language / Bahasa"><button type="button" data-setlang="ms" aria-pressed="false">BM</button><button type="button" data-setlang="en" aria-pressed="true">EN</button></div>
    <div class="seg tsz" role="group" aria-label="Text size"><button type="button" data-ts="-1" aria-label="Smaller text">A−</button><button type="button" data-ts="1" aria-label="Larger text">A+</button></div>
    <button class="iconbtn" id="themebtn" type="button" aria-label="Theme" title="Theme"></button>
  </div>
</header>
<main>
  <div class="vhead" style="margin-top:12px">{sitelib.avatar("wave")}<div class="vtxt"><h2>{B("Course home", "Laman kursus")}</h2>
    <p class="todo"><b>{B("What to do", "Apa perlu dibuat")}</b> {B("Open a part and start from its Start tab; every part page has a ⌂ button that brings you back here. Continue opens the part you used last.", "Buka satu bahagian dan mula dari tab Mula; setiap halaman bahagian ada butang ⌂ untuk kembali ke sini. Sambung membuka bahagian yang terakhir anda gunakan.")}</p>
    <p class="counts"><span class="cl">{B("Progress:", "Kemajuan:")}</span> <b id="overall">0 %</b> {B("overall: the mean over the parts that are available.", "keseluruhan: purata bahagian yang tersedia.")}</p></div>
    <a class="btn" id="contbtn" href="01-heat-transfer-1/index.html">{B("Continue", "Sambung")} →</a></div>
  {cards}
  <div class="topic">{B("Explorers and Python code", "Explorer dan kod Python")}</div>
  <p class="lead" style="margin:0 0 10px">{B("Each Explorer runs in the browser, on a phone too. The Python code solves the same problems in the same notation: use it to check hand calculations, and for assignments and projects.", "Setiap Explorer berjalan dalam pelayar, termasuk telefon. Kod Python menyelesaikan masalah yang sama dengan notasi yang sama: guna untuk menyemak pengiraan tangan, dan untuk assignment serta projek.")}</p>
  <div class="parts">{labs}</div>
  <div class="recbar" style="margin-top:12px">{zip_btn("all", "code/", "All Python code in one zip (" + kb(allp["bytes"]) + ")", "Semua kod Python dalam satu zip (" + kb(allp["bytes"]) + ")", "btn ghost")}<span class="savemsg" aria-live="polite"></span></div>
  <div class="topic">{B("Your progress", "Kemajuan anda")}</div>
  <div class="card">
    <p class="lead">{B("Progress is kept in this browser only. Export it to a file to move it to another device or to keep a copy; import that file on the other device. It is your own record, not a gradebook.", "Kemajuan disimpan dalam pelayar ini sahaja. Export ke fail untuk memindahkannya ke peranti lain atau menyimpan salinan; import fail itu pada peranti lain. Ia rekod anda sendiri, bukan buku gred.")}</p>
    <div class="recbar"><button class="btn ghost" id="expbtn" type="button"><span class="dl" aria-hidden="true">⤓</span> {B("Export progress (JSON)", "Export kemajuan (JSON)")}</button><label class="btn ghost" for="impfile">{B("Import progress…", "Import kemajuan…")}</label><input id="impfile" type="file" accept="application/json,.json" hidden><span class="savemsg" id="impmsg" aria-live="polite"></span></div>
    <p class="lead" style="margin:10px 0 0"><button class="linkbtn" id="resetall" type="button">{B("Erase all progress", "Padam semua kemajuan")}</button></p>
  </div>
  <div class="topic">{B("Text and sources", "Teks dan sumber")}</div>
  <div class="card"><p class="lead" style="margin:0">{B("Text: Mohd Yassin et al., <i>Two-Dimensional Finite Element Formulations for Heat, Solids and Fluids (with Matlab)</i>, MSNM 2020. Third-party images are credited where they appear (MIT, BSD, LGPL and CC BY licences). Python code: MIT licence.", "Teks: Mohd Yassin et al., <i>Two-Dimensional Finite Element Formulations for Heat, Solids and Fluids (with Matlab)</i>, MSNM 2020. Imej pihak ketiga dikreditkan di tempat ia muncul (lesen MIT, BSD, LGPL dan CC BY). Kod Python: lesen MIT.")}</p></div>
</main>
<footer class="foot"><p class="lect">{sitelib.avatar("head", "fava")}{B("Lecturer: Assoc. Prof. Ts. Dr. Ahmad Razin Zainal Abidin · arazin@utm.my", "Pensyarah: Prof. Madya Ts. Dr. Ahmad Razin Zainal Abidin · arazin@utm.my")}</p>
{copyright_line()}</footer>
</div>
'''
script = r'''
<script>
(function(){
  var $=function(s){return document.querySelector(s);}, $$=function(s){return Array.prototype.slice.call(document.querySelectorAll(s));};
  var API=window.COURSE_API||{}, bi=API.bi||function(e){return e;};
  /* the link to the other courses exists only on the GitHub Pages copy (My_Lectures/) */
  if(/github\.io$/.test(location.hostname))$$("[data-pages-only]").forEach(function(e){e.hidden=false;});
  function ld(k){try{var v=localStorage.getItem(k);return v?JSON.parse(v):null;}catch(e){return null;}}
  var lang=function(){return document.documentElement.getAttribute("data-lang")==="ms";};
  function paint(){
    var sum=0,n=0,latest=null;
    $$(".partcard[data-part] .pb").forEach(function(pb){var card=pb.closest(".partcard"),p=card.getAttribute("data-part"),st=ld("seaa4243-p"+p+"-v1");
      var pct=st&&st.pct?st.pct:0; pb.firstElementChild.style.width=pct+"%"; card.querySelector(".pct").textContent=pct+" %";
      card.querySelector(".last").textContent=st&&st.last?(lang()?"dibuka ":"opened ")+new Date(st.last).toLocaleDateString(undefined,{day:"numeric",month:"short"}):(lang()?"belum dibuka":"not opened yet");
      sum+=pct;n++; if(st&&st.last&&(!latest||st.last>latest.t))latest={t:st.last,href:card.getAttribute("href")};});
    $("#overall").textContent=(n?Math.round(sum/n):0)+" %"; if(latest)$("#contbtn").setAttribute("href",latest.href);
  }
  paint(); window.addEventListener("focus",paint); $$("[data-setlang]").forEach(function(b){b.addEventListener("click",function(){setTimeout(paint,0);});});
  $("#expbtn").addEventListener("click",function(){var o={};try{for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k&&k.indexOf("seaa4243-")===0){try{o[k]=JSON.parse(localStorage.getItem(k));}catch(e){}}}}catch(e){}
    var blob=new Blob([JSON.stringify({exported:new Date().toISOString(),course:"SEAA4243",data:o},null,1)],{type:"application/json"});
    API.saveFile(blob,"seaa4243-progress-"+new Date().toISOString().slice(0,10)+".json",$("#impmsg"),this);});
  $("#impfile").addEventListener("change",function(){var f=this.files[0];if(!f)return;var r=new FileReader();r.onload=function(){try{var j=JSON.parse(r.result),d=j.data||j,n=0;Object.keys(d).forEach(function(k){if(k.indexOf("seaa4243-")===0){localStorage.setItem(k,JSON.stringify(d[k]));n++;}});$("#impmsg").innerHTML=bi("Imported: "+n+" records.","Diimport: "+n+" rekod.");paint();}catch(e){$("#impmsg").innerHTML=bi("Not a valid progress file.","Bukan fail kemajuan yang sah.");}};r.readAsText(f);});
  var armed=false,rb=$("#resetall"),RB=rb.innerHTML;rb.addEventListener("click",function(){if(!armed){armed=true;rb.innerHTML=bi("Tap again to erase all progress","Tekan sekali lagi untuk memadam semua kemajuan");setTimeout(function(){armed=false;rb.innerHTML=RB;},4000);return;}
    var ks=[];try{for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k&&k.indexOf("seaa4243-")===0&&k!=="seaa4243-prefs")ks.push(k);}ks.forEach(function(k){localStorage.removeItem(k);});}catch(e){}armed=false;rb.innerHTML=RB;paint();});
})();
</script>'''
cfg = {"title": "SEAA 4243 Finite Element Method", "description": "Course home: heat transfer and plane stress by finite elements, with notes, slides, exercises, Explorers and Python code.",
       "course": {"part": 0, "key": "seaa4243-home-v1", "prefs": "seaa4243-prefs"}}
(SITE / "index.html").write_text(page(cfg, body, script_extra=script))
print("home written")
