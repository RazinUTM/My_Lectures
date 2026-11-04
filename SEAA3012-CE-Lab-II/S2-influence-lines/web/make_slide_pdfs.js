/* Print the 21 slides of index.html to vector PDFs (EN and BM), one 16:9 page per slide.
   Usage: node make_slide_pdfs.js <dir with node_modules containing mathjax and @ibm/plex-*>
   Needs Playwright (Chromium) and poppler's pdfunite. Output: ../pdf/s2_slides_online_EN.pdf, _BM.pdf */
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {execFileSync}=require('child_process');
const NM=path.resolve(process.argv[2]||'.','node_modules');
const MJ=fs.readFileSync(path.join(NM,'mathjax/es5/tex-svg.js'),'utf8');
const F=(pkg,file)=>'file://'+path.join(NM,'@ibm',pkg,'fonts/complete/woff2',file);
const face=(fam,pkg,file,w,st)=>`@font-face{font-family:"${fam}";src:url(${F(pkg,file)}) format("woff2");font-weight:${w};font-style:${st||'normal'}}`;
const FONTS=[face('IBM Plex Sans','plex-sans','IBMPlexSans-Regular.woff2',400),face('IBM Plex Sans','plex-sans','IBMPlexSans-Medium.woff2',500),
 face('IBM Plex Sans','plex-sans','IBMPlexSans-SemiBold.woff2',600),face('IBM Plex Sans','plex-sans','IBMPlexSans-Bold.woff2',700),
 face('IBM Plex Serif','plex-serif','IBMPlexSerif-Regular.woff2',400),face('IBM Plex Serif','plex-serif','IBMPlexSerif-SemiBold.woff2',600),
 face('IBM Plex Serif','plex-serif','IBMPlexSerif-Italic.woff2',400,'italic'),
 face('IBM Plex Mono','plex-mono','IBMPlexMono-Regular.woff2',400),face('IBM Plex Mono','plex-mono','IBMPlexMono-Medium.woff2',500)].join('\n');
const PRINT=`@page{size:1280px 720px;margin:0}
html,body{margin:0!important;padding:0!important;background:#fff!important}
body>*:not(.wrap),header.top,.navwrap,footer,.slidebar,input.scrub,.view:not(#v-slides){display:none!important}
.wrap,main,#v-slides,.stage{margin:0!important;padding:0!important;max-width:none!important}
.frame{width:1280px!important;height:720px!important;border:0!important;border-radius:0!important}`;
const OUT=path.resolve(__dirname,'..','pdf');const TMP=fs.mkdtempSync(path.join(require('os').tmpdir(),'slides-'));
(async()=>{const b=await chromium.launch();
for(const lang of ['en','ms']){
  const ctx=await b.newContext({viewport:{width:1280,height:720},deviceScaleFactor:1});
  await ctx.addInitScript(l=>{try{localStorage.setItem('s2-il-v3',JSON.stringify({lang:l,theme:'light'}))}catch(e){}},lang);
  const p=await ctx.newPage();
  await p.route('**/*',r=>{const u=r.request().url();if(u.includes('mathjax'))return r.fulfill({body:MJ,contentType:'application/javascript'});
    if(u.includes('fonts.googleapis.com'))return r.fulfill({body:FONTS,contentType:'text/css'});if(u.startsWith('file:'))return r.continue();return r.abort()});
  await p.goto('file://'+path.resolve(__dirname,'..','index.html')+'#slides');await p.addStyleTag({content:PRINT});
  await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1500);
  const n=await p.evaluate(()=>document.querySelectorAll('#deck .slide').length);const files=[];
  for(let i=0;i<n;i++){
    await p.evaluate(i=>{document.getElementById('sfirst').click();for(let k=0;k<i;k++)document.getElementById('snext').click()},i);
    await p.evaluate(()=>window.MathJax&&MathJax.startup&&MathJax.startup.promise);await p.waitForTimeout(250);
    const f=path.join(TMP,`${lang}_${String(i+1).padStart(2,'0')}.pdf`);await p.pdf({path:f,width:'1280px',height:'720px',printBackground:true,pageRanges:'1'});files.push(f)}
  const out=path.join(OUT,`s2_slides_online_${lang==='ms'?'BM':'EN'}.pdf`);execFileSync('pdfunite',[...files,out]);console.log('wrote',out,n,'slides');await ctx.close()}
await b.close()})();
