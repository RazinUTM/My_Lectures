#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmad Razin Zainal Abidin and Universiti Teknologi Malaysia
"""Build the SEAA 4333 course home, index.html in the course folder.

What: joins shared/home_src.html (the page body) with shared/course.css, shared/course.js and the small home
script below (progress of each Unit, Continue, progress export and import), all inline, and writes
../index.html. The preferences script runs before first paint, as on the Unit pages.

How to call it, from the course folder:
  python3 shared/build_home.py

Why it is like this: the home page shares the Unit pages' engine and look, so a change to course.css or
course.js reaches every page at the next build and nothing is copied by hand.
"""
import json
from pathlib import Path

shared = Path(__file__).resolve().parent
course = shared.parent

REGIONS = [
    [".crumbs", "Where you are", "Di mana anda berada", "The way back to For My Students and My Lectures.", "Jalan kembali ke For My Students dan My Lectures."],
    ["#hcontact", "Your lecturer", "Pensyarah anda", "Questions about the course go to this email.", "Soalan tentang kursus dihantar ke e-mel ini."],
    [".prefs", "Settings", "Tetapan", "Language (BM/EN), light or dark theme, text size (AA), and this guide. The choice is kept for every page of the course.", "Bahasa (BM/EN), tema cerah atau gelap, saiz teks (AA), dan panduan ini. Pilihan disimpan untuk setiap halaman kursus."],
    ["#homehead", "Continue", "Sambung", "Your overall progress, and a button to the Unit you used last.", "Kemajuan keseluruhan anda, dan butang ke Unit yang terakhir anda gunakan."],
    ["#units", "Units", "Unit", "One card per Unit, with its progress. Units not yet released are marked coming.", "Satu kad bagi setiap Unit, dengan kemajuannya. Unit yang belum dikeluarkan ditanda akan datang."],
    ["#explorers", "Explorers", "Explorer", "The interactive labs used in class; each opens on its own too.", "Makmal interaktif yang digunakan dalam kelas; setiap satu boleh dibuka sendiri juga."],
    ["#progress", "Your progress", "Kemajuan anda", "Export your progress to a file, import it on another device, or erase it.", "Export kemajuan anda ke fail, import pada peranti lain, atau padamkannya."],
    ["footer.foot", "Credits and licence", "Kredit dan lesen", "Who made the pages and what you may reuse.", "Siapa yang menghasilkan halaman ini dan apa yang boleh digunakan semula."],
]
COURSE = {"prefix": "seaa4333", "key": "seaa4333-home-v1", "prefs": "seaa4333-prefs", "lang": "en", "avatarBase": "shared/avatar/", "regions": REGIONS}
PREFS = ('<script>(function(){try{var r=document.documentElement,p=JSON.parse(localStorage.getItem("seaa4333-prefs")||"null")||{};'
         'if(p.lang==="ms"){r.setAttribute("data-lang","ms");r.lang="ms"}'
         'if(p.theme==="light"||p.theme==="dark")r.setAttribute("data-theme",p.theme);'
         'var f=+p.font||1;r.style.setProperty("--font-scale",String(f));r.style.setProperty("--ts",String(f));'
         'if(p.fold)r.classList.add("subfold")}catch(e){}})();</script>')
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400'
         '&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;500;600&display=swap">')
HOME_JS = r"""
(function(){
  var $=function(s){return document.querySelector(s);}, $$=function(s){return Array.prototype.slice.call(document.querySelectorAll(s));};
  var API=window.COURSE_API||{}, bi=API.bi||function(e){return e;};
  function ld(k){try{var v=localStorage.getItem(k);return v?JSON.parse(v):null;}catch(e){return null;}}
  var ms=function(){return document.documentElement.getAttribute("data-lang")==="ms";};
  function paint(){
    var sum=0,n=0,latest=null;
    $$(".partcard[data-part] .pb").forEach(function(pb){var card=pb.closest(".partcard"),p=card.getAttribute("data-part"),st=ld("seaa4333-u"+p+"-v1");
      var pct=st&&st.pct?st.pct:0; pb.firstElementChild.style.width=pct+"%"; card.querySelector(".pct").textContent=pct+" %";
      card.querySelector(".last").textContent=st&&st.last?(ms()?"dibuka ":"opened ")+new Date(st.last).toLocaleDateString(ms()?"ms-MY":"en-GB",{day:"numeric",month:"short"}):(ms()?"belum dibuka":"not opened yet");
      sum+=pct;n++; if(st&&st.last&&(!latest||st.last>latest.t))latest={t:st.last,href:card.getAttribute("href")};});
    $("#overall").textContent=(n?Math.round(sum/n):0)+" %"; if(latest)$("#contbtn").setAttribute("href",latest.href);
  }
  paint(); window.addEventListener("focus",paint); var lb=$("#btn-lang"); if(lb)lb.addEventListener("click",function(){setTimeout(paint,0);});
  $("#expbtn").addEventListener("click",function(){var o={};try{for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k&&k.indexOf("seaa4333-")===0){try{o[k]=JSON.parse(localStorage.getItem(k));}catch(e){}}}}catch(e){}
    var blob=new Blob([JSON.stringify({exported:new Date().toISOString(),course:"SEAA4333",data:o},null,1)],{type:"application/json"});
    API.saveFile(blob,"seaa4333-progress-"+new Date().toISOString().slice(0,10)+".json",$("#impmsg"),this);});
  $("#impfile").addEventListener("change",function(){var f=this.files[0];if(!f)return;var r=new FileReader();r.onload=function(){try{var j=JSON.parse(r.result),d=j.data||j,n=0;Object.keys(d).forEach(function(k){if(k.indexOf("seaa4333-")===0){localStorage.setItem(k,JSON.stringify(d[k]));n++;}});$("#impmsg").innerHTML=bi("Imported: "+n+" records.","Diimport: "+n+" rekod.");paint();}catch(e){$("#impmsg").innerHTML=bi("Not a valid progress file.","Bukan fail kemajuan yang sah.");}};r.readAsText(f);});
  var armed=false,rb=$("#resetall"),RB=rb.innerHTML;rb.addEventListener("click",function(){if(!armed){armed=true;rb.innerHTML=bi("Tap again to erase all progress","Tekan sekali lagi untuk memadam semua kemajuan");setTimeout(function(){armed=false;rb.innerHTML=RB;},4000);return;}
    var ks=[];try{for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k&&k.indexOf("seaa4333-")===0&&k!=="seaa4333-prefs")ks.push(k);}ks.forEach(function(k){localStorage.removeItem(k);});}catch(e){}armed=false;rb.innerHTML=RB;paint();});
})();
"""


def main() -> int:
    body = (shared / "home_src.html").read_text(encoding="utf-8")
    css = (shared / "course.css").read_text(encoding="utf-8")
    js = (shared / "course.js").read_text(encoding="utf-8")
    conf = json.dumps(COURSE, ensure_ascii=False).replace("</", "<\\/")
    doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
           "<title>SEAA 4333 Reinforced Concrete Design II</title>\n"
           '<meta name="claude:viewport-fit-sides" content="cover">\n'
           '<meta name="description" content="Course home of SEAA 4333 Reinforced Concrete Design II, Faculty of Civil Engineering, UTM: '
           'the Units with their progress, the Explorers, assessment, and progress export.">\n'
           + PREFS + "\n" + FONTS + "\n<style>\n" + css + "</style>\n</head>\n<body>\n" + body
           + f"\n<script>window.COURSE = {conf};</script>\n<script>\n{js}</script>\n<script>{HOME_JS}</script>\n</body>\n</html>\n")
    (course / "index.html").write_text(doc, encoding="utf-8")
    print(f"index.html: {len(doc):,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
