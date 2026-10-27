(function(){
"use strict";
/* =====================================================================
   State: one object, kept in localStorage under one key. Every read and
   write is wrapped, so the page works where storage is unavailable.
   ===================================================================== */
var KEY="s2-il-v3";
function ld(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function fresh(){return {lang:"en",theme:"auto",nmode:"full",read:{},qc:{},seen:{},slide:0,
  exp:{x:0,mode:"unit",keys:["R_A","R_B","R_C"],area:false,P:[5,2.5,1],a:[100,150]},
  pred:{ans:{},t0:0,t1:0},
  ex:{v:{},sel:{},chk:{},first:{},att:{},hint:{},conf:{},confAt:{},timer:{el:0,run:false,t0:0},done:0},
  lab:{ck:{},t1:{g:"R_A",k:"0.05",m:"2.5",v:[]},t2:{g:"R_A",k:"0.05",v:[]},eq:{},done1:false,done2:false,big:null},
  time:{}}}
var ST=(function(){var d=fresh(),s=ld(KEY,null);if(!s||typeof s!=="object")return d;
  Object.keys(d).forEach(function(k){if(s[k]===undefined)s[k]=d[k];else if(d[k]&&typeof d[k]==="object"&&!Array.isArray(d[k])){Object.keys(d[k]).forEach(function(j){if(s[k][j]===undefined)s[k][j]=d[k][j]})}});return s})();
var saveT=null;function save(){clearTimeout(saveT);saveT=setTimeout(function(){sv(KEY,ST)},120)}
function saveNow(){clearTimeout(saveT);sv(KEY,ST)}
window.addEventListener("pagehide",saveNow);

/* ---------- language and theme ---------- */
function L2(en,ms){return ST.lang==="ms"?ms:en}
var root=document.documentElement;
function tx(el,en,ms){el.setAttribute("data-en",en);el.setAttribute("data-ms",ms);el.textContent=L2(en,ms)}
var langHooks=[];
function applyLang(){root.setAttribute("data-lang",ST.lang);root.setAttribute("lang",ST.lang==="ms"?"ms":"en");
  document.querySelectorAll("[data-setlang]").forEach(function(b){b.setAttribute("aria-pressed",String(b.getAttribute("data-setlang")===ST.lang))});
  document.querySelectorAll("[data-en][data-ms]").forEach(function(el){el.textContent=L2(el.getAttribute("data-en"),el.getAttribute("data-ms"))});
  document.querySelectorAll("[data-ph-en]").forEach(function(el){el.placeholder=L2(el.getAttribute("data-ph-en"),el.getAttribute("data-ph-ms"))});
  langHooks.forEach(function(f){try{f()}catch(e){}})}
document.querySelectorAll("[data-setlang]").forEach(function(b){b.addEventListener("click",function(){ST.lang=b.getAttribute("data-setlang");save();applyLang()})});
var THEMES=["auto","light","dark"],SVGI='<svg viewBox="0 0 24 24" width="19" height="19" aria-hidden="true" style="display:block;margin:auto">',TSYM={
  auto:SVGI+'<circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 4a8 8 0 0 0 0 16z" fill="currentColor"/></svg>',
  light:SVGI+'<circle cx="12" cy="12" r="4.2" fill="currentColor"/><g stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 2.5v2.6M12 18.9v2.6M2.5 12h2.6M18.9 12h2.6M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8"/></g></svg>',
  dark:SVGI+'<path d="M20 14.6A8.2 8.2 0 1 1 9.4 4a6.6 6.6 0 0 0 10.6 10.6z" fill="currentColor"/></svg>'};
function applyTheme(){if(ST.theme==="auto")root.removeAttribute("data-theme");else root.setAttribute("data-theme",ST.theme);
  var b=document.getElementById("themebtn");b.innerHTML=TSYM[ST.theme];
  var lab=L2({auto:"Theme: automatic",light:"Theme: light",dark:"Theme: dark"}[ST.theme],{auto:"Tema: automatik",light:"Tema: cerah",dark:"Tema: gelap"}[ST.theme]);
  b.setAttribute("aria-label",lab);b.setAttribute("title",lab)}
document.getElementById("themebtn").addEventListener("click",function(){ST.theme=THEMES[(THEMES.indexOf(ST.theme)+1)%3];save();applyTheme();rerenderFigs()});
langHooks.push(applyTheme);

/* ---------- model ---------- */
var xB=250,xC=440,xD=690,xE=880,xF=1130,L=250;
var HALTS=[["A",0],["1",100],["2",200],["B",250],["3",300],["4",400],["C",440],["5",500],["6",600],["D",690],["7",700],["8",800],["E",880],["9",900],["10",1000],["11",1100],["F",1130]];
function RC(x){return (x>=xC&&x<=xD)?(xD-x)/L:0}
function RD(x){return (x>=xC&&x<=xD)?(x-xC)/L:0}
function RA(x){if(x<=xC)return (xB-x)/L;if(x<=xD)return -(xC-xB)/L*RC(x);return 0}
function RB(x){if(x<=xC)return x/L;if(x<=xD)return (xC/L)*RC(x);return 0}
function RE(x){if(x>=xD)return (xF-x)/L;if(x>=xC)return ((xF-xD)/L)*RD(x);return 0}
function RF(x){if(x>=xD)return (x-xE)/L;if(x>=xC)return -((xE-xD)/L)*RD(x);return 0}
var IL={R_A:RA,R_B:RB,R_C:RC,R_D:RD,R_E:RE,R_F:RF};
var KEYS=["R_A","R_B","R_C","R_D","R_E","R_F"];
var CV={R_A:"var(--rA)",R_B:"var(--rB)",R_C:"var(--rC)",R_D:"var(--rD)",R_E:"var(--rE)",R_F:"var(--rF)"};
var XJ=[0,250,439.999,440,690,690.001,880,1130];
var VERT=[0,250,440,690,880,1130];
var PRACTICE=[51,29,10,1,-11,-28,-39,-29,-13,-1,0,0,1,-1,0,1,0];
function haltName(x){for(var i=0;i<HALTS.length;i++)if(HALTS[i][1]===x)return HALTS[i][0];return null}
function f1(v){var s=(Math.abs(v)<0.05?0:v).toFixed(1).replace(/\.0$/,"");return s.replace("-","−")}
function f2(v){var s=(Math.abs(v)<5e-3?0:v).toFixed(2);return s.replace("-","−")}
function f3(v){var s=(Math.abs(v)<5e-4?0:v).toFixed(3);return s.replace("-","−")}
function mmss(ms){var s=Math.max(0,Math.round(ms/1000)),m=Math.floor(s/60);return (m<10?"0":"")+m+":"+((s%60)<10?"0":"")+(s%60)}
/* loads on the bridge as [position, value, index]; the leading load P1 stands at x, the others follow to its right */
function groupOf(mode){if(mode==="cmp")return {P:[5,2.5,0],a:[100,0]};return {P:ST.exp.P,a:ST.exp.a}}
function allLoads(x,mode){if(mode==="unit")return [[x,1,0]];if(mode==="m25")return [[x,2.5,0]];var g=groupOf(mode),pos=[x,x+g.a[0],x+g.a[0]+g.a[1]],l=[];
  for(var i=0;i<3;i++)if(g.P[i]>0)l.push([pos[i],g.P[i],i]);return l}
function loadsFor(x,mode){return allLoads(x,mode).filter(function(l){return l[0]<=xF+1e-9})}
function offLoads(x,mode){return allLoads(x,mode).filter(function(l){return l[0]>xF+1e-9})}
function kg(v){return String(+(+v).toFixed(2))}
function valueOf(key,x,mode){var s=0;loadsFor(x,mode).forEach(function(l){s+=l[1]*IL[key](l[0])});return s}
function comp(key,x){return valueOf(key,x,"cmp")}

/* ---------- MathJax ---------- */
var mjq=[];
function typeset(el){var MJ=window.MathJax;if(MJ&&MJ.typesetPromise&&MJ.startup&&MJ.startup.promise){MJ.startup.promise.then(function(){return MJ.typesetPromise([el])}).catch(function(){})}else{mjq.push(el)}}
window.__mjReady=function(){var q=mjq;mjq=[];q.forEach(typeset)};

/* =====================================================================
   SVG figures. x-scale fixed (1 unit = 1 mm, viewBox width 1240); text (fs),
   symbols (G) and the vertical scale K grow on narrow screens.
   ===================================================================== */
var W=1240,X0=55,G=1,INSLIDE=false;
function setG(fs){G=1+(fs-1)*0.8}
function px(x){return X0+x}
function T(x,y,s,o){o=o||{};return '<text x="'+x.toFixed(1)+'" y="'+y.toFixed(1)+'" font-size="'+(o.size||16).toFixed(1)+'" text-anchor="'+(o.anchor||"start")+'"'+(o.weight?' font-weight="'+o.weight+'"':'')+' class="svgtext" style="fill:'+(o.fill||"var(--fg)")+'">'+s+'</text>'}
function Rl(k){return 'R<tspan style="font-size:72%" dy="0.3em">'+k.slice(2)+'</tspan><tspan dy="-0.3em"></tspan>'}
function Eta(k){return 'η<tspan style="font-size:72%" dy="0.3em">'+k+'</tspan><tspan dy="-0.3em"></tspan>'}
function Ln(x1,y1,x2,y2,col,w,extra){return '<line x1="'+x1.toFixed(1)+'" y1="'+y1.toFixed(1)+'" x2="'+x2.toFixed(1)+'" y2="'+y2.toFixed(1)+'" style="stroke:'+col+'" stroke-width="'+w.toFixed(2)+'"'+(extra||'')+'/>'}
function vArrow(x,y1,y2,col,w){var up=y2<y1,h=Math.min(14*G,Math.abs(y2-y1)*0.6),hw=8*G;w=(w||3)*G;var yb=up?y2+h:y2-h;
  return Ln(x,y1,x,yb,col,w)+'<polygon points="'+x.toFixed(1)+','+y2.toFixed(1)+' '+(x-hw).toFixed(1)+','+yb.toFixed(1)+' '+(x+hw).toFixed(1)+','+yb.toFixed(1)+'" style="fill:'+col+'"/>'}
function hatch(x,y){var s='';for(var t=-18;t<=18;t+=9)s+=Ln(x+t*G,y,x+(t-7)*G,y+9*G,"var(--fg)",1.4*G);return s}
function pinAt(x,y){return '<polygon points="'+x+','+(y+4*G)+' '+(x-15*G)+','+(y+30*G)+' '+(x+15*G)+','+(y+30*G)+'" style="fill:none;stroke:var(--fg)" stroke-width="'+2.5*G+'"/>'+Ln(x-22*G,y+31*G,x+22*G,y+31*G,"var(--fg)",2*G)+hatch(x,y+31*G)}
function rollerAt(x,y){return '<polygon points="'+x+','+(y+4*G)+' '+(x-15*G)+','+(y+26*G)+' '+(x+15*G)+','+(y+26*G)+'" style="fill:none;stroke:var(--fg)" stroke-width="'+2.5*G+'"/>'+
  '<circle cx="'+(x-7*G)+'" cy="'+(y+31*G)+'" r="'+4.5*G+'" style="fill:none;stroke:var(--fg)" stroke-width="'+2*G+'"/><circle cx="'+(x+7*G)+'" cy="'+(y+31*G)+'" r="'+4.5*G+'" style="fill:none;stroke:var(--fg)" stroke-width="'+2*G+'"/>'+
  Ln(x-22*G,y+37*G,x+22*G,y+37*G,"var(--fg)",2*G)+hatch(x,y+37*G)}
function hingeAt(x,y){return '<circle cx="'+x+'" cy="'+y.toFixed(1)+'" r="'+8*G+'" style="fill:var(--panel);stroke:var(--hinge)" stroke-width="'+3*G+'"/>'}
function dim(x1,x2,y,label,fs){return Ln(x1,y,x2,y,"var(--muted)",1.2*G)+Ln(x1,y-7*G,x1,y+7*G,"var(--muted)",1.2*G)+Ln(x2,y-7*G,x2,y+7*G,"var(--muted)",1.2*G)+T((x1+x2)/2,y-6*G,label,{size:13*fs,anchor:"middle",fill:"var(--muted)"})}
function sideRight(f,x,v){if(x>=1100)return false;var n=f(x+5);return !((v>0&&n>v+1e-9)||(v<0&&n<v-1e-9))}
/* every line is linear between the breakpoints XJ, so areas and shading are computed exactly, splitting at zero crossings */
function brk(f){var pts=[];for(var i=0;i<XJ.length;i++){var x=XJ[i],v=f(x);if(i){var p=pts[pts.length-1];if((p[1]>0&&v<0)||(p[1]<0&&v>0)){var xz=p[0]+(x-p[0])*p[1]/(p[1]-v);pts.push([xz,0])}}pts.push([x,v])}return pts}
function sampleArea(f,sign){return brk(f).map(function(q){return [q[0],sign>0?Math.max(q[1],0):Math.min(q[1],0)]})}
function areaOf(f){var pts=brk(f),pos=0,neg=0;for(var i=1;i<pts.length;i++){var a=0.5*(pts[i][1]+pts[i-1][1])*(pts[i][0]-pts[i-1][0]);if(a>0)pos+=a;else neg+=a}return [pos,neg]}

function figureSVG(c){
  var fs=c.fs||1,keys=c.keys||[],mode=c.mode||"unit",out=[],K=52*fs*(INSLIDE?0.52:1);setG(fs);
  var hasLoad=(c.x!=null),loads=hasLoad?loadsFor(c.x,mode):[];
  var top=6,beamY=0,hb=0;
  if(c.bridge!==false){
    /* load labels: greedy rows so that labels of closely spaced loads never overlap */
    var labs=loads.map(function(l){var t=mode==="unit"?"1":(kg(l[1])+" kg"),w=t.length*0.6*16*fs+10*G,cx=Math.max(w/2+2,Math.min(W-w/2-2,px(l[0])));return {x:px(l[0]),cx:cx,t:t,w:w,r:0}}),rowEnd=[];
    labs.forEach(function(L){for(var r=0;r<4;r++){if(rowEnd[r]===undefined||L.cx-L.w/2>rowEnd[r]){L.r=r;rowEnd[r]=L.cx+L.w/2;return}}L.r=3});
    var nrows=labs.reduce(function(m,L){return Math.max(m,L.r+1)},1);
    beamY=hasLoad?(66*G+18*fs+(nrows-1)*22*fs):(14*G+10);
    var lab1=beamY+44*G+15*fs,lab2=lab1+6+13*fs,arrTop=lab2+10*G,nameY=arrTop+56*G+15*fs,valY=nameY+17*fs;
    hb=c.reactions?valY+16*fs:(c.dims?lab2+22+12*fs:lab2+10);
    out.push(Ln(px(0),beamY,px(xC)-9*G,beamY,"var(--fg)",7*G),Ln(px(xC)+9*G,beamY,px(xD)-9*G,beamY,"var(--fg)",7*G),Ln(px(xD)+9*G,beamY,px(xF),beamY,"var(--fg)",7*G));
    out.push(hingeAt(px(xC),beamY),hingeAt(px(xD),beamY));
    out.push(pinAt(px(0),beamY),rollerAt(px(xB),beamY),rollerAt(px(xE),beamY),pinAt(px(xF),beamY));
    HALTS.forEach(function(h){var main=/^[A-F]$/.test(h[0]);
      if(main)out.push(T(px(h[1]),lab1,h[0],{size:16*fs,anchor:"middle",weight:700}));
      else{out.push(Ln(px(h[1]),beamY+3.5*G,px(h[1]),beamY+14*G,"var(--muted)",1.5*G));out.push(T(px(h[1]),lab2,h[0],{size:13*fs,anchor:"middle",fill:"var(--muted)"}))}});
    if(c.dims){var dy=lab2+14+12*fs;[[0,250,"250"],[250,440,"190"],[440,690,"250"],[690,880,"190"],[880,1130,"250"]].forEach(function(d){out.push(dim(px(d[0]),px(d[1]),dy,d[2]+" mm",fs))})}
    if(hasLoad){
      labs.forEach(function(L){var dy=L.r*22*fs;out.push(vArrow(L.x,beamY-56*G-dy,beamY-6*G,"var(--load)",4));
        out.push(T(L.cx,beamY-62*G-dy,L.t,{size:16*fs,anchor:"middle",weight:700,fill:"var(--load)"}))});
      var tot=loads.reduce(function(s,l){return s+l[1]},0);
      if(c.reactions){var vmax=Math.max(1.76*tot,0.1);
        [["R_A",0],["R_B",xB],["R_E",xE],["R_F",xF]].forEach(function(r){var v=valueOf(r[0],c.x,mode),x=px(r[1]);
          var anc=r[1]===0?"start":(r[1]===xF?"end":"middle"),tx_=r[1]===0?x-14*G:(r[1]===xF?x+14*G:x);
          var zero_=Math.abs(v)<1e-9,col=zero_?"var(--muted)":(v>0?"var(--accent)":"var(--neg)");
          out.push(T(tx_,nameY,Rl(r[0]),{size:13.5*fs,anchor:anc,weight:600,fill:col}));
          out.push(T(tx_,valY,zero_?"0":(tot<=1?f3(v):f2(v)),{size:14.5*fs,anchor:anc,weight:600,fill:col}));
          if(zero_)return;var len=(14+42*Math.min(Math.abs(v)/vmax,1))*G;
          out.push(v>0?vArrow(x,arrTop+len,arrTop,col,3):vArrow(x,arrTop,arrTop+len,col,3))});
        out.push(Ln(px(0),hb-6*fs,px(xF),hb-6*fs,"var(--line)",1.2*G))}
    }
    top=hb;
  }
  var stripTop=top,lastBottom=top,tick=11.5*Math.min(fs,1.6);
  keys.forEach(function(k){var f=IL[k],col=CV[k];
    var labY=top+16*fs+8,zero=labY+13*fs+8*G+1.76*K+8,bottom=zero+Math.max(0.9*K,0.76*K+14*G+13*fs)+6;
    out.push(T(px(0)+10*G,labY,L2("Influence line for ","Influence line bagi ")+Rl(k),{size:15*fs,weight:700,fill:col}));
    if(hasLoad&&loads.length){var hdr=loads.length===1?"η = "+f3(f(loads[0][0]))+L2(" at x = "," pada x = ")+Math.round(loads[0][0]):"η = "+loads.map(function(l){return f3(f(l[0]))}).join(" · ");
      out.push(T(px(xF),labY,hdr,{size:15*fs,anchor:"end",weight:700,fill:"var(--load)"}))}
    [1.5,1,0.5,-0.5].forEach(function(g){var y=zero-g*K;out.push(Ln(px(0),y,px(xF),y,"var(--grid)",1));
      if(fs<=1.6||g===1)out.push(T(px(0)-7,y+4*G,String(g).replace("-","−"),{size:fs<=1.6?tick:11.5*fs,anchor:"end",fill:"var(--muted)"}))});
    if(c.area){[1,-1].forEach(function(sg){var p=sampleArea(f,sg);var s=px(0)+','+zero.toFixed(1)+' ';p.forEach(function(q){s+=px(q[0])+','+(zero-q[1]*K).toFixed(1)+' '});s+=px(xF)+','+zero.toFixed(1);
      out.push('<polygon points="'+s+'" style="fill:'+(sg>0?"var(--pos)":"var(--neg)")+';fill-opacity:.22"/>')})}
    out.push(Ln(px(0),zero,px(xF),zero,"var(--fg)",1.5*G));
    out.push('<polyline points="'+XJ.map(function(x){return px(x)+','+(zero-f(x)*K).toFixed(1)}).join(' ')+'" style="fill:none;stroke:'+col+'" stroke-width="'+3.5*G+'" stroke-linejoin="round"/>');
    VERT.forEach(function(x){var v=f(x);if(Math.abs(v)<1e-9)return;var right=sideRight(f,x,v);
      out.push(T(px(x)+(right?9*G:-9*G),zero-v*K+(v>0?-8*G:12*G+13*fs),f2(v),{size:13*fs,anchor:right?"start":"end",fill:col}))});
    if(c.points&&c.points.key===k){c.points.data.forEach(function(p){out.push('<circle cx="'+px(p.x)+'" cy="'+(zero-p.eta*K).toFixed(1)+'" r="'+7*G+'" style="fill:var(--panel);stroke:var(--load)" stroke-width="'+3*G+'"/>')});
      out.push(T(px(xF),labY,c.points.label,{size:13.5*fs,anchor:"end",fill:"var(--load)"}))}
    if(hasLoad){loads.forEach(function(l,j){var v=f(l[0]);out.push('<circle cx="'+px(l[0])+'" cy="'+(zero-v*K).toFixed(1)+'" r="'+(j===0?8:6)*G+'" style="fill:var(--load);stroke:var(--panel)" stroke-width="'+2*G+'"/>')})}
    lastBottom=bottom;top=bottom});
  if(keys.length){
    VERT.forEach(function(x){out.unshift(Ln(px(x),stripTop,px(x),lastBottom,"var(--grid)",1.2*G,' stroke-dasharray="'+5*G+' '+5*G+'"'))});
    VERT.forEach(function(x,i){out.push(T(px(x),lastBottom+12*fs+4,"ABCDEF"[i],{size:14*fs,anchor:"middle",weight:700,fill:"var(--muted)"}))});
    lastBottom+=12*fs+10}
  if(hasLoad&&c.bridge!==false){loads.forEach(function(l){out.push(Ln(px(l[0]),beamY+8*G,px(l[0]),keys.length?lastBottom-12*fs-10:hb,"var(--load)",2*G,' stroke-opacity=".55" stroke-dasharray="'+6*G+' '+5*G+'"'))})}
  return {html:out.join(""),h:Math.max(lastBottom,top)+4}}

function fbdSVG(fs){setG(fs);var o=[],stack=fs>1.45&&!INSLIDE,s=stack?2.3:0.75,top=20*fs+92*G,ph=top+150*G+34*fs+24;
  function P(ox,x){return ox+x*s}
  function title(ox,cx,oy,txt){o.push(T(stack?ox:cx,oy+18*fs,txt,{size:16*fs,anchor:stack?"start":"middle",weight:700}))}
  function beamABC(ox,y){o.push(Ln(P(ox,0),y,P(ox,440),y,"var(--fg)",6*G),pinAt(P(ox,0),y),rollerAt(P(ox,250),y))}
  function up(x,y,col,lab){o.push(vArrow(x,y+120*G,y+58*G,col,3),T(x,y+120*G+20*fs,lab,{size:15*fs,anchor:"middle",fill:col}))}
  function down(x,y,col,lab){o.push(vArrow(x,y+58*G,y+120*G,col,3),T(x,y+120*G+20*fs,lab,{size:15*fs,anchor:"middle",fill:col}))}
  function load(x,y,col,lab,anc){o.push(vArrow(x,y-72*G,y-6*G,col,4),T(anc==="end"?x-10*G:x,y-78*G,lab,{size:15*fs,anchor:anc||"middle",weight:700,fill:col}))}
  var dyo=150*G+30*fs,ox=stack?110:40,oy=0,y=oy+top;
  title(ox,P(ox,220),oy,L2("(a) load on ABC","(a) load pada ABC"));beamABC(ox,y);
  o.push(T(P(ox,440),y-12*G,"C",{size:13*fs,anchor:"middle",fill:"var(--muted)"}));
  load(P(ox,300),y,"var(--load)","1");o.push(dim(P(ox,0),P(ox,300),y-36*G,"x",fs));
  up(P(ox,0),y,"var(--accent)",Rl("R_A"));up(P(ox,250),y,"var(--accent)",Rl("R_B"));
  o.push(dim(P(ox,0),P(ox,250),y+dyo,"250",fs),dim(P(ox,250),P(ox,440),y+dyo,"190",fs));
  ox=stack?330:470;oy=stack?ph:0;y=oy+top;
  title(ox,P(ox,125),oy,L2("(b) load on CD","(b) load pada CD"));
  o.push(Ln(P(ox,0),y,P(ox,250),y,"var(--fg)",6*G),hingeAt(P(ox,0),y),hingeAt(P(ox,250),y));
  o.push(T(P(ox,0),y-16*G,"C",{size:13*fs,anchor:"middle",fill:"var(--muted)"}),T(P(ox,250),y-16*G,"D",{size:13*fs,anchor:"middle",fill:"var(--muted)"}));
  load(P(ox,80),y,"var(--load)","1");
  up(P(ox,0),y,"var(--hinge)",Eta("C"));up(P(ox,250),y,"var(--hinge)",Eta("D"));
  o.push(dim(P(ox,0),P(ox,250),y+dyo,"250",fs));
  ox=stack?110:790;oy=stack?2*ph:0;y=oy+top;
  title(ox,P(ox,220),oy,L2("(c) ABC carrying ","(c) ABC membawa ")+Eta("C"));beamABC(ox,y);
  load(P(ox,440),y,"var(--hinge)",Eta("C"),"end");
  down(P(ox,0),y,"var(--neg)",Rl("R_A")+" &lt; 0");up(P(ox,250),y,"var(--accent)",Rl("R_B"));
  o.push(dim(P(ox,0),P(ox,250),y+dyo,"250",fs),dim(P(ox,250),P(ox,440),y+dyo,"190",fs));
  return {html:o.join(""),h:stack?3*ph:ph}}

/* ---------- supports and hinges: what each restraint passes on ---------- */
function hArrow(x1,x2,y,col,w){var h=Math.min(14*G,Math.abs(x2-x1)*0.6),hw=8*G,dir=x2>x1?1:-1,xb=x2-dir*h;w=(w||3)*G;
  return Ln(x1,y,xb,y,col,w)+'<polygon points="'+x2.toFixed(1)+','+y.toFixed(1)+' '+xb.toFixed(1)+','+(y-hw).toFixed(1)+' '+xb.toFixed(1)+','+(y+hw).toFixed(1)+'" style="fill:'+col+'"/>'}
function supportsSVG(fs){setG(fs);var o=[],stack=fs>1.45&&!INSLIDE,top=10,by0=top+30*fs+92*G,ph=by0+130*G+50*fs+16;
  var P=[{t:L2("Pin · A, F","Pin · A, F"),l1:L2("vertical and horizontal force","daya menegak dan mendatar"),l2:L2("free to rotate","bebas berputar")},
         {t:L2("Roller · B, E","Roller · B, E"),l1:L2("vertical force only","daya menegak sahaja"),l2:L2("free to rotate and roll","bebas berputar dan bergolek")},
         {t:L2("Hinge · C, D","Hinge · C, D"),l1:L2("passes force between members","memindahkan daya antara anggota"),l2:L2("no moment: M = 0","tiada moment: M = 0")}];
  P.forEach(function(q,i){var cx=stack?620:(215+410*i),oy=stack?i*ph:0,by=oy+by0,half=stack?260:150;
    o.push(T(cx,oy+top+18*fs,q.t,{size:16*fs,anchor:"middle",weight:700}));
    if(i<2){o.push(Ln(cx-half,by,cx+half,by,"var(--fg)",6*G));o.push(i===0?pinAt(cx,by):rollerAt(cx,by));
      o.push(vArrow(cx,by+125*G,by+52*G,"var(--accent)",3),T(cx+14*G,by+105*G,"V",{size:15*fs,weight:700,fill:"var(--accent)"}));
      if(i===0)o.push(hArrow(cx-110*G,cx-34*G,by+34*G,"var(--accent)",3),T(cx-112*G,by+26*G,"H",{size:15*fs,weight:700,fill:"var(--accent)"}))}
    else{var g=16*G;o.push(Ln(cx-half,by,cx-g,by,"var(--fg)",6*G),Ln(cx+g,by,cx+half,by,"var(--fg)",6*G));
      o.push('<circle cx="'+(cx-g)+'" cy="'+by+'" r="'+6*G+'" style="fill:var(--panel);stroke:var(--hinge)" stroke-width="'+2.5*G+'"/><circle cx="'+(cx+g)+'" cy="'+by+'" r="'+6*G+'" style="fill:var(--panel);stroke:var(--hinge)" stroke-width="'+2.5*G+'"/>');
      o.push(T(cx-half*0.6,by-14*G,L2("cantilever tip","hujung cantilever"),{size:12.5*fs,anchor:"middle",fill:"var(--muted)"}),T(cx+half*0.6,by-14*G,"suspended span",{size:12.5*fs,anchor:"middle",fill:"var(--muted)"}));
      o.push(vArrow(cx-g,by-78*G,by-10*G,"var(--hinge)",3),T(cx-g-10*G,by-60*G,Rl("R_C"),{size:15*fs,anchor:"end",weight:700,fill:"var(--hinge)"}));
      o.push(vArrow(cx+g,by+80*G,by+10*G,"var(--hinge)",3),T(cx+g+10*G,by+66*G,Rl("R_C"),{size:15*fs,weight:700,fill:"var(--hinge)"}))}
    o.push(T(cx,by+125*G+22*fs,q.l1,{size:14*fs,anchor:"middle"}),T(cx,by+125*G+40*fs,q.l2,{size:14*fs,anchor:"middle",fill:"var(--muted)"}))});
  return {html:o.join(""),h:stack?3*ph:ph}}
/* ---------- load path: which members carry a load on ABC, on CD or on DEF ---------- */
function hingepathSVG(fs){setG(fs);var o=[],top=4,cases=[[300,"ABC"],[560,"CD"],[800,"DEF"]],rh=0;
  cases.forEach(function(cs,i){var x=cs[0],m=cs[1],oy=top+rh*i,beamY=oy+32*fs+70*G,on={ABC:m!=="DEF",CD:m==="CD",DEF:m!=="ABC"};
    var col=function(b){return on[b]?"var(--fg)":"var(--line)"};
    var t=L2(["(a) load on ABC","(b) load on CD","(c) load on DEF"][i],["(a) load pada ABC","(b) load pada CD","(c) load pada DEF"][i]);
    var res=[L2("nothing passes through C or D","tiada daya melalui C atau D"),"R<tspan style=\"font-size:72%\" dy=\"0.3em\">C</tspan><tspan dy=\"-0.3em\"> = "+f2(RC(x))+", R</tspan><tspan style=\"font-size:72%\" dy=\"0.3em\">D</tspan><tspan dy=\"-0.3em\"> = "+f2(RD(x))+"</tspan>",L2("nothing passes through C or D","tiada daya melalui C atau D")][i];
    o.push(T(px(0),oy+20*fs,t,{size:15*fs,weight:700}),T(px(xF),oy+20*fs,res,{size:14.5*fs,anchor:"end",weight:600,fill:i===1?"var(--hinge)":"var(--muted)"}));
    o.push(Ln(px(0),beamY,px(xC)-9*G,beamY,col("ABC"),7*G),Ln(px(xC)+9*G,beamY,px(xD)-9*G,beamY,col("CD"),7*G),Ln(px(xD)+9*G,beamY,px(xF),beamY,col("DEF"),7*G));
    o.push(hingeAt(px(xC),beamY),hingeAt(px(xD),beamY),pinAt(px(0),beamY),rollerAt(px(xB),beamY),rollerAt(px(xE),beamY),pinAt(px(xF),beamY));
    o.push(vArrow(px(x),beamY-54*G,beamY-6*G,"var(--load)",4),T(px(x),beamY-60*G,"1",{size:15*fs,anchor:"middle",weight:700,fill:"var(--load)"}));
    if(i===1){[[xC,RC(x)],[xD,RD(x)]].forEach(function(h){o.push(vArrow(px(h[0]),beamY+12*G,beamY+58*G,"var(--hinge)",3))})}
    ["A","B","C","D","E","F"].forEach(function(nm,j){o.push(T(px(VERT[j])+(j===2||j===3?14*G:0),beamY+62*G,nm,{size:13*fs,anchor:j===2||j===3?"start":"middle",fill:"var(--muted)",weight:600}))});
    rh=beamY+72*G-oy+10*fs});
  var ly=top+rh*3+4*fs;o.push(Ln(px(0),ly,px(0)+46*G,ly,"var(--fg)",6*G),T(px(0)+56*G,ly+5*fs,L2("carries the load","membawa load"),{size:13.5*fs}),
    Ln(px(0)+280*fs,ly,px(0)+280*fs+46*G,ly,"var(--line)",6*G),T(px(0)+290*fs+46*G,ly+5*fs,L2("unloaded","tidak dibebani"),{size:13.5*fs}));
  return {html:o.join(""),h:ly+16*fs}}
var MBREL={R_A:0,R_B:xB,R_C:xC,R_D:xD,R_E:xE,R_F:xF};
function mbSVG(key,d,fs){setG(fs);var o=[],K=62*fs,beamY=26*fs+1.8*K+8,f=IL[key],x0=MBREL[key];
  o.push(Ln(px(0),beamY,px(xF),beamY,"var(--muted)",2*G,' stroke-dasharray="'+7*G+' '+6*G+'"'));
  [["R_A",0,1],["R_B",xB,0],["R_E",xE,0],["R_F",xF,1]].forEach(function(s){if(s[0]===key)return;o.push(s[2]?pinAt(px(s[1]),beamY):rollerAt(px(s[1]),beamY))});
  o.push('<polyline points="'+XJ.map(function(x){return px(x)+','+(beamY-d*K*f(x)).toFixed(1)}).join(' ')+'" style="fill:none;stroke:'+CV[key]+'" stroke-width="'+5*G+'" stroke-linejoin="round"/>');
  [xC,xD].forEach(function(x){var y=beamY-d*K*f(x);if(key==="R_C"&&x===xC)y=beamY-d*K;o.push(hingeAt(px(x),y))});
  if(d>0.02){var yT=beamY-d*K,xr=px(x0),rt=!(f(Math.min(x0+5,1135))>f(x0)+1e-9||x0>=1100);
    o.push(Ln(xr,beamY,xr,yT,"var(--load)",3*G,' stroke-dasharray="'+5*G+' '+4*G+'"'));
    o.push(T(rt?xr+12*G:xr-12*G,yT-10*G,"δ = "+d.toFixed(2),{size:14*fs,anchor:rt?"start":"end",weight:700,fill:"var(--load)"}))}
  var lettersY=beamY+Math.max(0.9*K,50*G)+16*fs;
  VERT.forEach(function(x,i){var v=f(x)*d;o.push(T(px(x),lettersY,"ABCDEF"[i],{size:16*fs,anchor:"middle",weight:700}));
    if(Math.abs(v)>0.02&&x!==x0)o.push(T(px(x)+10*G,beamY-v*K+(v>0?-10*G:12*G+13*fs),f2(v),{size:13*fs,fill:CV[key]}))});
  o.push(T(px(xF),20*fs,L2("released: ","dilepaskan: ")+Rl(key),{size:15*fs,anchor:"end",weight:600,fill:CV[key]}));
  return {html:o.join(""),h:lettersY+10}}

/* ---------- figure registry ---------- */
var LIVE={x:400},MB={key:"R_A",d:1},LAB={key:ST.lab.t1.g||"R_A",points:null},QP={};
function fsOf(el){var w=el.getBoundingClientRect().width;if(!w&&el.parentElement)w=el.parentElement.getBoundingClientRect().width;if(!w)return 1;return Math.min(3,Math.max(1,880/w))}
function renderFig(svg){var k=svg.getAttribute("data-fig"),r=null;INSLIDE=!!svg.closest(".slide");var fs=INSLIDE?1.7:fsOf(svg),E=ST.exp;
  if(k==="model")r=figureSVG({fs:fs,dims:true});
  else if(k==="ils4")r=figureSVG({fs:fs,keys:["R_A","R_B","R_C","R_E"]});
  else if(k==="ils-ab")r=figureSVG({fs:fs,keys:["R_A","R_B"]});
  else if(k==="ils-ce")r=figureSVG({fs:fs,keys:["R_C","R_E"]});
  else if(k==="fbd")r=fbdSVG(fs);
  else if(k==="supports")r=supportsSVG(fs);
  else if(k==="hingepath")r=hingepathSVG(fs);
  else if(k==="mbA")r=mbSVG("R_A",1,fs);
  else if(k==="mbdemo")r=mbSVG(MB.key,MB.d,fs);
  else if(k==="explorer")r=figureSVG({fs:fs,x:E.x,mode:E.mode,keys:E.keys,area:E.area,reactions:true});
  else if(k==="slidelive")r=figureSVG({fs:fs,x:LIVE.x,mode:"unit",keys:["R_A","R_B"],reactions:true});
  else if(k==="lab1")r=figureSVG({fs:fs,keys:[LAB.key],points:LAB.points});
  else if(k.indexOf("q-")===0&&QP[k])r=QP[k](fs);
  if(!r)return;if(k==="slidelive")svg.parentElement.style.maxWidth="calc(68cqh * "+(W/r.h).toFixed(3)+")";
  svg.setAttribute("viewBox","0 0 "+W+" "+Math.ceil(r.h));svg.innerHTML=r.html}
function renderAll(rootEl){(rootEl||document).querySelectorAll("svg.fig[data-fig]").forEach(function(s){if(s.offsetParent!==null||s.closest(".slide"))renderFig(s)})}
function rerenderFigs(){renderAll(document.getElementById("v-"+current));if(current==="slides")renderAll(slides[slideIdx])}
langHooks.push(rerenderFigs);

/* ---------- generated tables (headers carry both languages) ---------- */
function B(en,ms){return '<span class="en">'+en+'</span><span class="ms">'+ms+'</span>'}
function buildTables(){
  document.querySelectorAll('table[data-table="ordinates"]').forEach(function(t){var h='<thead><tr><th class="l">Halt</th><th>x (mm)</th>'+KEYS.map(function(k){return '<th>\\(\\eta_'+k.slice(2)+'\\)</th>'}).join("")+'</tr></thead><tbody>';
    HALTS.forEach(function(r){h+='<tr><td class="l">'+r[0]+'</td><td>'+r[1]+'</td>'+KEYS.map(function(k){return '<td>'+f3(IL[k](r[1]))+'</td>'}).join("")+'</tr>'});t.innerHTML=h+'</tbody>'});
  document.querySelectorAll('table[data-table="vertices"]').forEach(function(t){var h='<thead><tr><th class="l">'+B("Load at","Load di")+'</th>'+KEYS.map(function(k){return '<th>\\(\\eta_'+k.slice(2)+'\\)</th>'}).join("")+'</tr></thead><tbody>';
    VERT.forEach(function(x,i){h+='<tr><td class="l">'+"ABCDEF"[i]+'</td>'+KEYS.map(function(k){return '<td>'+f2(IL[k](x))+'</td>'}).join("")+'</tr>'});t.innerHTML=h+'</tbody>'});
  document.querySelectorAll('table[data-table="compound"],table[data-table="compound-short"]').forEach(function(t){var short=t.getAttribute("data-table")==="compound-short";
    var h='<thead><tr><th class="l">'+B("5 kg at","5 kg di")+'</th><th>x (mm)</th>'+(short?'':'<th>'+B("2.5 kg at (mm)","2.5 kg di (mm)")+'</th>')+'<th>\\(R_A\\) (kgf)</th><th>\\(R_B\\) (kgf)</th></tr></thead><tbody>';
    HALTS.forEach(function(r){if(r[1]>(short?600:690))return;h+='<tr><td class="l">'+r[0]+'</td><td>'+r[1]+'</td>'+(short?'':'<td>'+(r[1]+100)+'</td>')+'<td>'+f2(comp("R_A",r[1]))+'</td><td>'+f2(comp("R_B",r[1]))+'</td></tr>'});t.innerHTML=h+'</tbody>'});
  document.querySelectorAll('table[data-table="practice"]').forEach(function(t){t.innerHTML='<thead><tr><th class="l">Halt</th>'+HALTS.map(function(r){return '<th>'+r[0]+'</th>'}).join("")+'</tr></thead><tbody><tr><td class="l">'+B("Reading (div)","Bacaan (div)")+'</td>'+PRACTICE.map(function(v){return '<td>'+String(v).replace("-","−")+'</td>'}).join("")+'</tr></tbody>'})}

/* =====================================================================
   Views, progress and badges
   ===================================================================== */
var VIEWS=["start","notes","slides","explorer","exercises","lab","glossary"],current="start",typesetDone={};
var NSECS=["n1","n2","n3","n4","n5","n6","n7","n8"],QCS=["qc1","qc6","qc2","qc7","qc3","qc4","qc5"];
function cnt(o){return Object.keys(o).filter(function(k){return o[k]}).length}
function parts(){var lab=0;for(var i=1;i<=5;i++)if(ST.lab.ck["ck"+i])lab++;if(ST.lab.done1)lab++;if(ST.lab.done2)lab++;
  return {notes:[NSECS.filter(function(s){return ST.read[s]}).length,8],slides:[Math.min(cnt(ST.seen),slides.length),slides.length],
    explorer:[Object.keys(ST.pred.ans).length,6],exercises:[cnt(ST.ex.chk),10],lab:[lab,7]}}
function updateProgress(){var p=parts(),sum=0;
  Object.keys(p).forEach(function(k){var b=document.querySelector('[data-bd="'+k+'"]');sum+=p[k][0]/p[k][1];if(b){b.textContent=p[k][0]+"/"+p[k][1];b.classList.toggle("full",p[k][0]>=p[k][1])}});
  var pct=Math.round(sum/5*100),bar=document.getElementById("pbar");bar.firstElementChild.style.width=pct+"%";bar.setAttribute("aria-valuenow",String(pct));
  document.getElementById("ppct").textContent=pct+" %";
  if(current==="start")renderStart()}
function show(v,noscroll){if(VIEWS.indexOf(v)<0)v="start";current=v;
  document.querySelectorAll(".view").forEach(function(s){s.hidden=s.getAttribute("data-view")!==v});
  document.querySelectorAll(".tab").forEach(function(t){t.setAttribute("aria-selected",String(t.getAttribute("data-view")===v))});
  var el=document.getElementById("v-"+v);renderAll(el);if(!typesetDone[v]){typesetDone[v]=1;typeset(el)}
  if(v==="slides")goSlide(slideIdx);if(v==="start")renderStart();if(v==="exercises")renderExSummary();
  updatePill();
  try{history.replaceState(null,"","#"+v)}catch(e){}
  if(!noscroll)window.scrollTo({top:0})}
document.querySelectorAll(".tab").forEach(function(t){t.addEventListener("click",function(){show(t.getAttribute("data-view"))})});
document.querySelectorAll("[data-go]").forEach(function(b){b.addEventListener("click",function(){show(b.getAttribute("data-go"))})});
function goTo(view,anchor){show(view,!!anchor);if(anchor){var t=document.getElementById(anchor);if(t)setTimeout(function(){t.scrollIntoView({behavior:"smooth",block:"start"})},60)}}

/* ---------- study time: counted in 15 s steps while the page is visible and in use ---------- */
var lastAct=Date.now();["pointerdown","keydown","scroll","input"].forEach(function(e){window.addEventListener(e,function(){lastAct=Date.now()},{passive:true})});
setInterval(function(){if(document.visibilityState==="visible"&&Date.now()-lastAct<120000){ST.time[current]=(ST.time[current]||0)+15;save()}},15000);

/* =====================================================================
   Notes: key points, mark as read, quick checks
   ===================================================================== */
var art=document.getElementById("notesart");
function setNmode(m){ST.nmode=m;art.classList.toggle("keyonly",m==="key");
  document.querySelectorAll("[data-nmode]").forEach(function(b){b.setAttribute("aria-pressed",String(b.getAttribute("data-nmode")===m))});
  art.querySelectorAll("details.kp").forEach(function(d){d.open=(m==="key")});save()}
document.querySelectorAll("[data-nmode]").forEach(function(b){b.addEventListener("click",function(){setNmode(b.getAttribute("data-nmode"))})});
function syncRead(){NSECS.forEach(function(id){var on=!!ST.read[id],sec=document.getElementById(id);sec.classList.toggle("isread",on);
    var cb=sec.querySelector('input[data-read]');if(cb)cb.checked=on;var a=document.querySelector('[data-toc="'+id+'"]');if(a)a.classList.toggle("isread",on)});
  var n=NSECS.filter(function(s){return ST.read[s]}).length,left=0;NSECS.forEach(function(s){if(!ST.read[s])left+=Number(document.getElementById(s).getAttribute("data-rt"))||0});
  var qok=QCS.filter(function(q){return ST.qc[q]&&ST.qc[q].ok}).length,qn=QCS.filter(function(q){return ST.qc[q]}).length;
  tx(document.getElementById("nstat"),n+" of 8 sections read · about "+left+" min left · quick checks "+qok+"/"+qn,n+" daripada 8 section dibaca · lebih kurang "+left+" min lagi · semakan pantas "+qok+"/"+qn);
  tx(document.getElementById("tocstat"),n+"/8 read",n+"/8 dibaca")}
document.querySelectorAll("input[data-read]").forEach(function(cb){cb.addEventListener("change",function(){ST.read[cb.getAttribute("data-read")]=cb.checked;save();syncRead();updateProgress()})});
function paintQC(box){var id=box.getAttribute("data-qc"),st=ST.qc[id],ans=box.getAttribute("data-ans");
  box.querySelectorAll(".opt").forEach(function(o){var v=o.getAttribute("data-v");o.dataset.state=st?(v===ans?"right":(v===st.v?"wrong":"")):""});
  box.querySelector(".fb").hidden=!st}
document.querySelectorAll(".qc").forEach(function(box){var id=box.getAttribute("data-qc");
  box.querySelectorAll(".opt").forEach(function(o){o.addEventListener("click",function(){if(ST.qc[id])return;ST.qc[id]={v:o.getAttribute("data-v"),ok:o.getAttribute("data-v")===box.getAttribute("data-ans")};save();paintQC(box);syncRead()})});paintQC(box)});
document.querySelectorAll('.toc a').forEach(function(a){a.addEventListener("click",function(e){e.preventDefault();var t=document.querySelector(a.getAttribute("href"));if(t)t.scrollIntoView({behavior:"smooth",block:"start"})})});
langHooks.push(syncRead);

/* =====================================================================
   Slides
   ===================================================================== */
var slides=[].slice.call(document.querySelectorAll("#deck .slide")),slideIdx=Math.min(ST.slide||0,slides.length-1);
slides.forEach(function(s,i){var f=document.createElement("div");f.className="foot";f.innerHTML="<span>SEAA 3012 · Lab S2 Influence Lines</span><span>"+(i+1)+" / "+slides.length+"</span>";s.appendChild(f)});
function goSlide(i){slideIdx=Math.max(0,Math.min(slides.length-1,i));slides.forEach(function(s,j){s.classList.toggle("on",j===slideIdx)});
  document.getElementById("scount").textContent=(slideIdx+1)+" / "+slides.length;
  document.getElementById("sprog").style.width=((slideIdx+1)/slides.length*100)+"%";
  renderAll(slides[slideIdx]);ST.slide=slideIdx;if(current==="slides"&&!ST.seen[slideIdx]){ST.seen[slideIdx]=1;updateProgress()}save()}
document.getElementById("sprev").addEventListener("click",function(){goSlide(slideIdx-1)});
document.getElementById("snext").addEventListener("click",function(){goSlide(slideIdx+1)});
var stage=document.getElementById("stage"),shint=document.getElementById("shint");
function toggleFull(){if(document.fullscreenElement){document.exitFullscreen().catch(function(){});return}
  function no(){tx(shint,"Full screen is not available here; use your browser's full-screen mode.","Full screen tidak tersedia di sini; guna mod full screen browser anda.")}
  if(!stage.requestFullscreen){no();return}
  stage.requestFullscreen().then(function(){setTimeout(function(){renderAll(slides[slideIdx])},120)}).catch(no)}
document.getElementById("sfull").addEventListener("click",toggleFull);
document.addEventListener("fullscreenchange",function(){setTimeout(function(){renderAll(slides[slideIdx])},120)});
document.addEventListener("keydown",function(e){if(e.key==="Escape"&&drawerOpen){closeDrawer();return}
  if(current!=="slides")return;if(e.target.closest&&e.target.closest("input,textarea,select"))return;
  if(e.key==="ArrowRight"||e.key==="PageDown"||e.key===" "){goSlide(slideIdx+1);e.preventDefault()}
  else if(e.key==="ArrowLeft"||e.key==="PageUp"){goSlide(slideIdx-1);e.preventDefault()}
  else if(e.key==="Home"){goSlide(0)}else if(e.key==="End"){goSlide(slides.length-1)}
  else if(e.key==="f"||e.key==="F"){toggleFull()}});
document.querySelectorAll('.slide[data-predict] .opt').forEach(function(b){b.addEventListener("click",function(){var s=b.closest(".slide");
  s.querySelectorAll(".opt").forEach(function(o){o.dataset.state=o.getAttribute("data-ok")==="1"?"right":(o===b?"wrong":"")});var r=s.querySelector(".reveal");r.hidden=false;typeset(r)})});
/* swipe left or right on the slide to change slides (tablets and phones) */
var deck=document.getElementById("deck"),tsx=null,tsy=null;
deck.addEventListener("touchstart",function(e){if(e.touches.length!==1||e.target.closest("input,button")){tsx=null;return}tsx=e.touches[0].clientX;tsy=e.touches[0].clientY},{passive:true});
deck.addEventListener("touchend",function(e){if(tsx===null)return;var t=e.changedTouches[0],dx=t.clientX-tsx,dy=t.clientY-tsy;tsx=null;if(Math.abs(dx)>50&&Math.abs(dx)>1.5*Math.abs(dy))goSlide(slideIdx+(dx<0?1:-1))},{passive:true});
var slive=document.getElementById("slive");
slive.addEventListener("input",function(){LIVE.x=Number(slive.value);HALTS.forEach(function(q){if(Math.abs(q[1]-LIVE.x)<=6)LIVE.x=q[1]});renderFig(document.querySelector('svg[data-fig="slidelive"]'))});

/* =====================================================================
   Explorer
   ===================================================================== */
var EXKEYS=KEYS,E=ST.exp;
if((ST.expv||0)<3){E.keys=["R_A","R_B","R_C"];E.P=[5,2.5,1];E.a=[100,150];ST.expv=3}
E.mode="cus";E.keys=(Array.isArray(E.keys)?E.keys:[]).filter(function(k){return EXKEYS.indexOf(k)>=0});
var xpos=document.getElementById("xpos"),xlabel=document.getElementById("xlabel"),expsvg=document.getElementById("expsvg");
var readout=document.getElementById("readout"),sumline=document.getElementById("sumline"),areanote=document.getElementById("areanote"),rowrap=document.getElementById("rowrap"),ropop=document.getElementById("ropop");
if(!Array.isArray(E.P)||E.P.length!==3)E.P=[5,2.5,1];if(!Array.isArray(E.a)||E.a.length!==2)E.a=[100,150];
function fmtMode(v){var t=loadsFor(E.x,E.mode).reduce(function(s,l){return s+l[1]},0);return (t<=1?f3(v):f2(v))+" kgf"}
/* ---------- how each reaction is computed: one line per load, member by member ---------- */
function n0(v){return String(Math.round(v)).replace("-","−")}
function sub(k){return k.slice(2)}
function f4(v){var s=(Math.abs(v)<5e-5?0:v).toFixed(4);return s.replace("-","−")}
function etaSteps(k,x){var f3=f4,X=n0(x),c=k.slice(2),eC="η<sub>C</sub> = (690 − "+X+")/250 = "+f3(RC(x)),eD="η<sub>D</sub> = (" +X+" − 440)/250 = "+f3(RD(x));
  var on={ABC:L2("on ABC","pada ABC"),CD:L2("on the suspended span CD","pada suspended span CD"),DEF:L2("on DEF","pada DEF")};
  function z(msg){return {m:"",t:"η<sub>"+c+"</sub> = 0 ("+msg+")"}}
  var noABC=L2("a load on ABC does not reach DEF","load pada ABC tidak sampai ke DEF"),noDEF=L2("a load on DEF does not reach ABC","load pada DEF tidak sampai ke ABC"),noCD=L2("the load is not on the suspended span CD","load tiada pada suspended span CD");
  if(k==="R_A"){if(x<=xC)return {m:on.ABC,t:"η<sub>A</sub> = (250 − "+X+")/250 = "+f3(RA(x))};if(x<=xD)return {m:on.CD,t:eC+"; η<sub>A</sub> = −0.76 × η<sub>C</sub> = "+f3(RA(x))};return z(noDEF)}
  if(k==="R_B"){if(x<=xC)return {m:on.ABC,t:"η<sub>B</sub> = "+X+"/250 = "+f3(RB(x))};if(x<=xD)return {m:on.CD,t:eC+"; η<sub>B</sub> = 1.76 × η<sub>C</sub> = "+f3(RB(x))};return z(noDEF)}
  if(k==="R_C"){if(x>=xC&&x<=xD)return {m:on.CD,t:eC};return z(noCD)}
  if(k==="R_D"){if(x>=xC&&x<=xD)return {m:on.CD,t:eD};return z(noCD)}
  if(k==="R_E"){if(x>=xD)return {m:on.DEF,t:"η<sub>E</sub> = (1130 − "+X+")/250 = "+f3(RE(x))};if(x>=xC)return {m:on.CD,t:eD+"; η<sub>E</sub> = 1.76 × η<sub>D</sub> = "+f3(RE(x))};return z(noABC)}
  if(x>=xD)return {m:on.DEF,t:"η<sub>F</sub> = ("+X+" − 880)/250 = "+f3(RF(x))};if(x>=xC)return {m:on.CD,t:eD+"; η<sub>F</sub> = −0.76 × η<sub>D</sub> = "+f3(RF(x))};return z(noABC)}
function explainHTML(k){var c=sub(k),unit=E.mode==="unit",ls=loadsFor(E.x,E.mode),off=offLoads(E.x,E.mode),terms=[],h=[];
  h.push('<b style="color:'+CV[k]+'">R<sub>'+c+'</sub></b> · '+L2("how it is calculated","cara pengiraan"));
  h.push('<p class="eq">R<sub>'+c+'</sub> = '+(unit?"1 × η<sub>"+c+"</sub>(x)":"Σ P<sub>i</sub> η<sub>"+c+"</sub>(x<sub>i</sub>)")+'</p><ol>');
  ls.forEach(function(l){var st=etaSteps(k,l[0]),eta=IL[k](l[0]),nm=unit?L2("Unit load","Unit load"):"P<sub>"+(l[2]+1)+"</sub> = "+kg(l[1])+" kg";
    terms.push(unit?f4(eta):kg(l[1])+"("+f4(eta)+")");
    h.push('<li>'+nm+L2(" at x = "," di x = ")+n0(l[0])+" mm"+(st.m?" ("+st.m+")":"")+':<br>'+st.t+(unit?"":' → '+kg(l[1])+" × "+f4(eta).replace(/^(−.*)$/,"($1)")+" = "+f3(l[1]*eta))+'</li>')});
  off.forEach(function(l){h.push('<li class="muted">P<sub>'+(l[2]+1)+'</sub> = '+kg(l[1])+" kg"+L2(" at x = "," di x = ")+n0(l[0])+" mm: "+L2("beyond F, not on the bridge","di luar F, tiada pada jambatan")+'</li>')});
  if(!ls.length)h.push('<li class="muted">'+L2("No load on the bridge.","Tiada load pada jambatan.")+'</li>');
  var tv=valueOf(k,E.x,E.mode);h.push('</ol><p class="eq">R<sub>'+c+'</sub> = '+(terms.length>1?terms.join(" + ").replace(/\+ −/g,"− ")+" = ":"")+fmtMode(tv)+(Math.abs(tv)>1e-9?" ≈ "+f2(tv*9.80665)+" N":"")+'</p>');
  h.push('<p class="muted">'+(k==="R_C"||k==="R_D"?L2("Positive: the suspended span presses down on the cantilever tip.","Positif: suspended span menekan ke bawah pada hujung cantilever."):L2("Positive: the support pushes up. Negative: the support holds the deck down (uplift).","Positif: support menolak ke atas. Negatif: support menahan deck ke bawah (uplift)."))+'</p>');
  return h.join("")}
var RO={},popKey=null,popPinned=false;
KEYS.forEach(function(k){var d=document.createElement("div");d.className="ro";d.tabIndex=0;d.setAttribute("role","button");d.setAttribute("aria-controls","ropop");d.setAttribute("aria-expanded","false");
  d.innerHTML='<div class="k" style="color:'+CV[k]+'">R<sub>'+k.slice(2)+'</sub>'+(k==="R_C"||k==="R_D"?' <span class="muted" style="font-weight:400">hinge</span>':'')+'<span class="ri" aria-hidden="true">i</span></div><div class="v"></div>';
  d.addEventListener("mouseenter",function(e){if(!popPinned)openPop(k)});
  d.addEventListener("mouseleave",function(){if(!popPinned)closePop()});
  d.addEventListener("focus",function(){if(!popPinned)openPop(k)});
  d.addEventListener("blur",function(){if(!popPinned)closePop()});
  d.addEventListener("click",function(e){e.stopPropagation();if(popPinned&&popKey===k){popPinned=false;closePop()}else{popPinned=true;openPop(k)}});
  d.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();d.click()}else if(e.key==="Escape"){popPinned=false;closePop()}});
  readout.appendChild(d);RO[k]=d});
function openPop(k){popKey=k;KEYS.forEach(function(j){RO[j].setAttribute("aria-expanded",String(j===k));RO[j].classList.toggle("on",j===k)});ropop.innerHTML=explainHTML(k);ropop.hidden=false;placePop()}
function closePop(){popKey=null;ropop.hidden=true;KEYS.forEach(function(j){RO[j].setAttribute("aria-expanded","false");RO[j].classList.remove("on")})}
function placePop(){if(!popKey)return;var d=RO[popKey],Wr=rowrap.clientWidth,pw=Math.min(440,Wr);ropop.style.width=pw+"px";
  var left=Math.max(0,Math.min(Wr-pw,d.offsetLeft+d.offsetWidth/2-pw/2));ropop.style.left=left+"px";ropop.style.top=(d.offsetTop+d.offsetHeight+8)+"px"}
document.addEventListener("click",function(e){if(popPinned&&!ropop.contains(e.target)){popPinned=false;closePop()}});
window.addEventListener("resize",placePop);
function refreshExplorer(){renderFig(expsvg);
  KEYS.forEach(function(k){var v=valueOf(k,E.x,E.mode),d=RO[k];d.classList.toggle("neg",v<-1e-9);d.querySelector(".v").textContent=fmtMode(v)});
  if(popKey){ropop.innerHTML=explainHTML(popKey);placePop()}
  var s=valueOf("R_A",E.x,E.mode)+valueOf("R_B",E.x,E.mode)+valueOf("R_E",E.x,E.mode)+valueOf("R_F",E.x,E.mode),off=offLoads(E.x,E.mode);
  var offTxt=off.length?L2(" ("+off.map(function(l){return E.mode==="cmp"?"the 2.5 kg mass":"P"+(l[2]+1)}).join(", ")+" beyond the end of the model)"," ("+off.map(function(l){return E.mode==="cmp"?"jisim 2.5 kg":"P"+(l[2]+1)}).join(", ")+" di luar hujung model)"):"";
  sumline.textContent=L2("Check: R_A + R_B + R_E + R_F = "+fmtMode(s)+" = total load on the model","Semakan: R_A + R_B + R_E + R_F = "+fmtMode(s)+" = jumlah load pada model")+offTxt;
  areanote.innerHTML=E.area?E.keys.map(function(k){var a=areaOf(IL[k]);return '<b style="color:'+CV[k]+'">R<sub>'+k.slice(2)+'</sub></b>: '+L2("positive area +"+f1(a[0])+" mm, negative area "+(a[1]<-0.05?f1(a[1]):"0")+" mm, net "+f1(a[0]+a[1])+" mm, so R = "+f1(a[0]+a[1])+"\u2009w for a uniform load w (kg/mm) over the whole model","area positif +"+f1(a[0])+" mm, area negatif "+(a[1]<-0.05?f1(a[1]):"0")+" mm, bersih "+f1(a[0]+a[1])+" mm, maka R = "+f1(a[0]+a[1])+"\u2009w bagi uniform load w (kg/mm) pada seluruh model")}).join("<br>"):"";
  save()}
function setX(x){E.x=Math.max(0,Math.min(1130,Math.round(x)));xpos.value=E.x;var h=haltName(E.x);xlabel.textContent="x = "+E.x+" mm"+(h?" ("+h+")":"");
  document.querySelectorAll("#halts .chip").forEach(function(c){c.setAttribute("aria-pressed",String(Number(c.getAttribute("data-x"))===E.x))});refreshExplorer()}
xpos.addEventListener("input",function(){setX(Number(xpos.value))});
HALTS.forEach(function(h){var b=document.createElement("button");b.type="button";b.className="chip";b.textContent=h[0];b.setAttribute("data-x",h[1]);b.setAttribute("aria-pressed","false");b.addEventListener("click",function(){setX(h[1])});document.getElementById("halts").appendChild(b)});
[["cP1","P",0,100],["cP2","P",1,100],["cP3","P",2,100],["cA1","a",0,1130],["cA2","a",1,1130]].forEach(function(q){var el=document.getElementById(q[0]);el.value=E[q[1]][q[2]];
  el.addEventListener("input",function(){var v=parseNum(el.value);if(v===null)return;E[q[1]][q[2]]=Math.max(0,Math.min(q[3],v));refreshExplorer()});
  el.addEventListener("change",function(){var v=parseNum(el.value);E[q[1]][q[2]]=v===null?0:Math.max(0,Math.min(q[3],v));el.value=E[q[1]][q[2]];refreshExplorer()})});
var PRESETS={unit:[[1,0,0],null],m25:[[2.5,0,0],null],t2:[[5,2.5,0],[100,null]]};
function syncLoadInputs(){[["cP1","P",0],["cP2","P",1],["cP3","P",2],["cA1","a",0],["cA2","a",1]].forEach(function(q){document.getElementById(q[0]).value=E[q[1]][q[2]]})}
document.querySelectorAll("[data-preset]").forEach(function(b){b.addEventListener("click",function(){var pr=PRESETS[b.getAttribute("data-preset")];E.P=pr[0].slice();if(pr[1]&&pr[1][0]!=null)E.a[0]=pr[1][0];syncLoadInputs();refreshExplorer()})});
var rchips=document.getElementById("rchips");
EXKEYS.forEach(function(k){var b=document.createElement("button");b.type="button";b.className="chip rk";b.style.setProperty("--kc",CV[k]);b.innerHTML="R<sub>"+k.slice(2)+"</sub>";b.setAttribute("aria-pressed",String(E.keys.indexOf(k)>=0));
  b.addEventListener("click",function(){var i=E.keys.indexOf(k);if(i>=0)E.keys.splice(i,1);else{E.keys.push(k);E.keys.sort(function(a,c){return EXKEYS.indexOf(a)-EXKEYS.indexOf(c)})}syncChips();refreshExplorer()});rchips.appendChild(b)});
function syncChips(){rchips.querySelectorAll(".chip").forEach(function(o,j){o.setAttribute("aria-pressed",String(E.keys.indexOf(EXKEYS[j])>=0))})}
document.getElementById("ilall").addEventListener("click",function(){E.keys=EXKEYS.slice();syncChips();refreshExplorer()});
document.getElementById("ilnone").addEventListener("click",function(){E.keys=[];syncChips();refreshExplorer()});
var showarea=document.getElementById("showarea");showarea.checked=!!E.area;showarea.addEventListener("change",function(){E.area=showarea.checked;refreshExplorer()});
var dragging=false;
function dragTo(e){var r=expsvg.getBoundingClientRect();if(!r.width)return;var x=(e.clientX-r.left)/r.width*W-X0;for(var i=0;i<HALTS.length;i++){if(Math.abs(HALTS[i][1]-x)<=7){x=HALTS[i][1];break}}setX(x)}
expsvg.addEventListener("pointerdown",function(e){dragging=true;try{expsvg.setPointerCapture(e.pointerId)}catch(_){}dragTo(e)});
expsvg.addEventListener("pointermove",function(e){if(dragging)dragTo(e)});
["pointerup","pointercancel","lostpointercapture"].forEach(function(t){expsvg.addEventListener(t,function(){dragging=false})});
langHooks.push(refreshExplorer);

var QUESTIONS=[
 {q:["A single mass stands at halt 4 (on the cantilever BC, 150 mm beyond B). The reaction at A is …","Satu jisim berada di halt 4 (pada cantilever BC, 150 mm selepas B). Reaction di A ialah …"],
  o:[["upward (positive)","ke atas (positif)"],["zero: the load is not on span AB","sifar: load tiada pada span AB"],["downward (negative): the support must hold the beam down","ke bawah (negatif): support perlu menahan beam ke bawah"]],a:2,
  e:["Beam ABC is one rigid piece pivoting about B. A load beyond B lifts end A, so the support at A pulls down: η<sub>A</sub>(400) = (250 − 400)/250 = −0.60.","Beam ABC ialah satu kepingan rigid yang berpangsi pada B. Load selepas B mengangkat hujung A, jadi support di A menarik ke bawah: η<sub>A</sub>(400) = (250 − 400)/250 = −0.60."]},
 {q:["Where must a single mass stand to make R<sub>B</sub> as large as possible?","Di mana satu jisim perlu berada untuk menjadikan R<sub>B</sub> sebesar mungkin?"],
  o:[["at B","di B"],["at C (the cantilever tip)","di C (hujung cantilever)"],["at A","di A"],["at D","di D"]],a:1,
  e:["η<sub>B</sub>(x) = x/250 keeps growing past B and peaks at the cantilever tip: η<sub>B</sub>(440) = 1.76, larger than the load itself, because B also has to balance the pull-down at A.","η<sub>B</sub>(x) = x/250 terus meningkat selepas B dan memuncak di hujung cantilever: η<sub>B</sub>(440) = 1.76, lebih besar daripada load itu sendiri, kerana B juga perlu mengimbangi tarikan ke bawah di A."]},
 {q:["The mass is at halt 8 (between D and E). What is R<sub>A</sub>?","Jisim berada di halt 8 (antara D dan E). Berapakah R<sub>A</sub>?"],
  o:[["0","0"],["−0.20","−0.20"],["+0.20","+0.20"]],a:0,
  e:["A load on DEF is carried by E and F only. The suspended span CD is unloaded, so the hinge at D passes nothing to the left half: η<sub>A</sub> = 0 for every x beyond D.","Load pada DEF dibawa oleh E dan F sahaja. Suspended span CD tidak dibebani, jadi hinge di D tidak memindahkan apa-apa ke separuh kiri: η<sub>A</sub> = 0 bagi setiap x selepas D."]},
 {q:["The mass is at halt 5 (on the suspended span CD). Which statement is true?","Jisim berada di halt 5 (pada suspended span CD). Pernyataan mana yang benar?"],
  o:[["R<sub>A</sub> + R<sub>B</sub> = 1","R<sub>A</sub> + R<sub>B</sub> = 1"],["R<sub>A</sub> + R<sub>B</sub> = R<sub>C</sub> = 0.76","R<sub>A</sub> + R<sub>B</sub> = R<sub>C</sub> = 0.76"],["R<sub>A</sub> + R<sub>B</sub> = 0","R<sub>A</sub> + R<sub>B</sub> = 0"]],a:1,
  e:["Beam ABC carries only the hinge force at C, η<sub>C</sub>(500) = (690 − 500)/250 = 0.76, so its two reactions add up to 0.76 (−0.578 + 1.338). The remaining 0.24 goes through D to E and F.","Beam ABC hanya membawa hinge force di C, η<sub>C</sub>(500) = (690 − 500)/250 = 0.76, jadi dua reaction-nya berjumlah 0.76 (−0.578 + 1.338). Baki 0.24 melalui D ke E dan F."]},
 {q:["The 5 kg + 2.5 kg pair moves to the right, with the 2.5 kg mass 100 mm in front of (to the right of) the 5 kg mass. The most negative R<sub>A</sub> occurs when …","Pasangan 5 kg + 2.5 kg bergerak ke kanan, dengan jisim 2.5 kg 100 mm di hadapan (di kanan) jisim 5 kg. R<sub>A</sub> paling negatif berlaku apabila …"],
  o:[["the 5 kg mass is at C","jisim 5 kg di C"],["the 2.5 kg mass is at C","jisim 2.5 kg di C"],["both masses are on the suspended span","kedua-dua jisim pada suspended span"]],a:0,
  e:["η<sub>A</sub> is piecewise linear with its minimum (−0.76) at C, so the extreme of the sum occurs with a load on that vertex. The heavier load there gives 5(−0.76) + 2.5(−0.456) = −4.94 kgf, against −3.70 kgf with the 2.5 kg mass at C.","η<sub>A</sub> adalah piecewise linear dengan minimum (−0.76) di C, jadi nilai ekstrem jumlahnya berlaku dengan satu load pada vertex itu. Load yang lebih berat di situ memberi 5(−0.76) + 2.5(−0.456) = −4.94 kgf, berbanding −3.70 kgf dengan jisim 2.5 kg di C."]},
 {q:["The influence line for R<sub>A</sub> is one straight line from A to C although there is a support at B. Why?","Influence line bagi R<sub>A</sub> ialah satu garis lurus dari A ke C walaupun terdapat support di B. Mengapa?"],
  o:[["ABC is a single rigid beam, so moments about B give R<sub>A</sub> = (250 − x)/250 for any x on it","ABC ialah satu rigid beam, jadi moment terhadap B memberi R<sub>A</sub> = (250 − x)/250 bagi sebarang x padanya"],["B carries no load","B tidak membawa load"],["the structure is symmetric","struktur ini simetri"]],a:0,
  e:["B is where the moment is taken, not where the beam bends: for any load on ABC the same lever rule applies, and the line passes through zero at B and continues negative to C.","B ialah titik di mana moment diambil, bukan tempat beam melentur: bagi sebarang load pada ABC, lever rule yang sama digunakan, dan garis melalui sifar di B serta berterusan negatif hingga C."]}];
var qlist=document.getElementById("qlist"),scoreEl=document.getElementById("score");
function li(p){return ST.lang==="ms"?p[1]:p[0]}
function renderPreds(){qlist.innerHTML="";var P=ST.pred;
  QUESTIONS.forEach(function(Q,i){var d=document.createElement("div");d.className="q";d.innerHTML="<p>"+(i+1)+". "+li(Q.q)+"</p>";var o=document.createElement("div");o.className="opts";var a=P.ans[i];
    Q.o.forEach(function(t,j){var b=document.createElement("button");b.type="button";b.className="opt";b.innerHTML=li(t);if(a!==undefined)b.dataset.state=(j===Q.a)?"right":(j===a?"wrong":"");
      b.addEventListener("click",function(){if(P.ans[i]!==undefined)return;if(!P.t0)P.t0=Date.now();P.ans[i]=j;if(Object.keys(P.ans).length===6)P.t1=Date.now();save();renderPreds();updateProgress()});o.appendChild(b)});
    d.appendChild(o);if(a!==undefined){var fb=document.createElement("p");fb.className="fb";fb.innerHTML="<b>"+(a===Q.a?L2("Correct.","Betul."):L2("Not quite.","Belum tepat."))+"</b> "+li(Q.e);d.appendChild(fb)}qlist.appendChild(d)});
  var n=Object.keys(P.ans).length,c=0;Object.keys(P.ans).forEach(function(k){if(P.ans[k]===QUESTIONS[k].a)c++});
  scoreEl.textContent=n?L2("Score "+c+" / "+n+" answered","Skor "+c+" / "+n+" dijawab")+(P.t1?L2(" · time "," · masa ")+mmss(P.t1-P.t0):""):""}
document.getElementById("predreset").addEventListener("click",function(){ST.pred={ans:{},t0:0,t1:0};save();renderPreds();updateProgress()});
langHooks.push(renderPreds);

/* ---------- Müller–Breslau demo ---------- */
var mbchips=document.getElementById("mbchips"),mbd=document.getElementById("mbd"),mbdv=document.getElementById("mbdv");
KEYS.forEach(function(k){var b=document.createElement("button");b.type="button";b.className="chip rk";b.style.setProperty("--kc",CV[k]);b.innerHTML="R<sub>"+k.slice(2)+"</sub>";b.setAttribute("aria-pressed",String(k===MB.key));
  b.addEventListener("click",function(){MB.key=k;mbchips.querySelectorAll(".chip").forEach(function(o,j){o.setAttribute("aria-pressed",String(KEYS[j]===k))});renderFig(document.querySelector('svg[data-fig="mbdemo"]'))});mbchips.appendChild(b)});
mbd.addEventListener("input",function(){MB.d=Number(mbd.value);mbdv.textContent=MB.d.toFixed(2);renderFig(document.querySelector('svg[data-fig="mbdemo"]'))});

/* =====================================================================
   Exercises: answers, first attempt, attempts, hints, confidence, timer
   ===================================================================== */
var X=ST.ex,QX=[].slice.call(document.querySelectorAll("article.qx"));
function parseNum(s){if(s==null)return null;s=String(s).trim().replace(/[−–]/g,"-").replace(",",".");if(s===""||s==="-"||s===".")return null;var v=Number(s);return isFinite(v)?v:null}
function evalField(el){
  if(el.matches("input.ans")){if(el.getAttribute("data-type")==="text"){var t=el.value.trim().toUpperCase();if(!t)return null;return el.getAttribute("data-ans").split("|").indexOf(t)>=0}
    var v=parseNum(el.value);if(v===null)return null;return Math.abs(v-Number(el.getAttribute("data-ans")))<=Number(el.getAttribute("data-tol"))}
  var sel=[].slice.call(el.querySelectorAll('button[aria-pressed="true"]')).map(function(b){return b.getAttribute("data-v")});if(!sel.length)return null;
  if(el.classList.contains("choice"))return sel[0]===el.getAttribute("data-ans");
  return sel.sort().join(",")===el.getAttribute("data-ans").split(",").sort().join(",")}
function fieldsOf(q){return [].slice.call(q.querySelectorAll("input.ans,.choice,.multi"))}
function okCount(q){var ok=0;fieldsOf(q).forEach(function(el){if(evalField(el))ok++});return ok}
var CONF=[["sure","Sure","Yakin"],["unsure","Not sure","Kurang pasti"],["guess","Guess","Teka"]];
function resText(q){var fl=fieldsOf(q),res=q.querySelector(".res"),meta=q.querySelector(".qmeta");if(!X.chk[q.id]){res.textContent="";if(meta)meta.textContent="";return}
  if(!fl.length){tx(res,"Compare your answers with the model answers below.","Bandingkan jawapan anda dengan jawapan model di bawah.");}
  else{var ok=okCount(q);tx(res,ok+" of "+fl.length+" correct",ok+" daripada "+fl.length+" betul")}
  if(meta&&X.first[q.id]&&fl.length){var f=X.first[q.id];tx(meta,"first attempt "+f.ok+"/"+f.n+" · checks "+(X.att[q.id]||1)+(X.hint[q.id]?" · hint used":""),"first attempt "+f.ok+"/"+f.n+" · semakan "+(X.att[q.id]||1)+(X.hint[q.id]?" · petunjuk digunakan":""))}}
function paintFields(q){fieldsOf(q).forEach(function(el){var r=evalField(el);el.setAttribute("data-state",r===true?"right":"wrong")})}
function checkQ(q,restoring){var fl=fieldsOf(q);
  if(!restoring){X.att[q.id]=(X.att[q.id]||0)+1;
    if(!X.chk[q.id]){X.first[q.id]={ok:okCount(q),n:fl.length};X.confAt[q.id]=X.conf[q.id]||null}
    X.chk[q.id]=1;if(cnt(X.chk)===10&&!X.done){X.done=elapsed();if(X.timer.run)pauseTimer()}save()}
  if(fl.length)paintFields(q);
  var sb=q.querySelector(".sls");if(sb)sb.hidden=false;else{var so=q.querySelector(".sol");so.hidden=false;typeset(so)}
  resText(q);var pk=q.getAttribute("data-plot");if(pk)plotQ(q,pk);
  if(!restoring){renderExSummary();updateProgress()}}
function plotQ(q,k){var box=q.querySelector(".qplot");if(!box)return;var id="q-"+k;
  if(k==="q2"||k==="q5"){var keys=k==="q2"?["R_D","R_F"]:["R_E","R_F"],base=k==="q2"?"q2-":"q5-";
    var pts=function(row){return [440,690,880,1130].map(function(x,i){var v=parseNum(document.getElementById(base+(row*4+i+1)).value);return v===null?null:{x:x,eta:v}}).filter(Boolean)};
    QP[id]=function(fs){var lab=L2("○ your ordinates","○ ordinate anda"),a=figureSVG({fs:fs,keys:[keys[0]],points:{key:keys[0],data:pts(0),label:lab},bridge:false}),b=figureSVG({fs:fs,keys:[keys[1]],points:{key:keys[1],data:pts(1),label:lab},bridge:false});
      return {html:a.html+'<g transform="translate(0,'+a.h+')">'+b.html+'</g>',h:a.h+b.h}}}
  else if(k==="q6"){QP[id]=function(fs){return figureSVG({fs:fs,keys:["R_A"],points:{key:"R_A",data:HALTS.map(function(h,i){return {x:h[1],eta:PRACTICE[i]/50}}),label:L2("○ illustrative readings","○ bacaan ilustrasi")},bridge:false})}}
  if(!box.firstElementChild)box.innerHTML='<svg class="fig" data-fig="'+id+'" role="img" aria-label="Your answer against the correct influence line"></svg>';
  if(box.offsetParent!==null)renderFig(box.querySelector("svg"))}
QX.forEach(function(q){
  /* confidence control and attempt line, inserted into every auto-marked question */
  var qbar=q.querySelector(".qbar");
  if(fieldsOf(q).length){var c=document.createElement("span");c.className="conf";c.setAttribute("role","group");
    c.innerHTML='<span>'+B("Confidence","Keyakinan")+'</span>'+CONF.map(function(k){return '<button type="button" data-c="'+k[0]+'" aria-pressed="false">'+B(k[1],k[2])+'</button>'}).join("");
    qbar.insertBefore(c,qbar.firstChild);
    c.querySelectorAll("button").forEach(function(b){if(X.conf[q.id]===b.getAttribute("data-c"))b.setAttribute("aria-pressed","true");
      b.addEventListener("click",function(){X.conf[q.id]=b.getAttribute("data-c");c.querySelectorAll("button").forEach(function(o){o.setAttribute("aria-pressed",String(o===b))});save()})});
    var m=document.createElement("div");m.className="qmeta";qbar.parentNode.insertBefore(m,qbar.nextSibling)}
  q.querySelectorAll("input.ans,textarea.free").forEach(function(el){if(X.v[el.id]!=null)el.value=X.v[el.id];el.addEventListener("input",function(){X.v[el.id]=el.value;el.removeAttribute("data-state");save()})});
  q.querySelectorAll(".choice,.multi").forEach(function(g){var single=g.classList.contains("choice"),saved=X.sel[g.id]||[];
    g.querySelectorAll("button").forEach(function(b){if(saved.indexOf(b.getAttribute("data-v"))>=0)b.setAttribute("aria-pressed","true");
      b.addEventListener("click",function(){if(single)g.querySelectorAll("button").forEach(function(o){o.setAttribute("aria-pressed","false")});b.setAttribute("aria-pressed",String(single?true:b.getAttribute("aria-pressed")!=="true"));
        g.removeAttribute("data-state");X.sel[g.id]=[].slice.call(g.querySelectorAll('button[aria-pressed="true"]')).map(function(o){return o.getAttribute("data-v")});save()})})});
  q.querySelector(".chk").addEventListener("click",function(){checkQ(q)});
  var hn=q.querySelector(".hnt");if(hn)hn.addEventListener("click",function(){var h=q.querySelector(".hintbox");h.hidden=!h.hidden;if(!h.hidden){typeset(h);if(!X.hint[q.id]){X.hint[q.id]=1;save();resText(q);renderExSummary()}}});
  var sb=q.querySelector(".sls");if(sb)sb.addEventListener("click",function(){var s=q.querySelector(".sol");s.hidden=!s.hidden;sb.setAttribute("aria-expanded",String(!s.hidden));if(!s.hidden)typeset(s)});
});
function estMarks(which){var m=0,tot=0;QX.forEach(function(q){var mk=Number(q.getAttribute("data-marks")),fl=fieldsOf(q).length;if(q.getAttribute("data-bonus")||!fl)return;tot+=mk;
  if(!X.chk[q.id])return;var r=which==="first"?(X.first[q.id]?X.first[q.id].ok/X.first[q.id].n:0):okCount(q)/fl;m+=mk*r});return [m,tot]}
function exStats(){var fo=0,fn=0,no=0,nn=0,att=0,h=0;QX.forEach(function(q){if(!X.chk[q.id])return;var fl=fieldsOf(q).length;if(!fl)return;var f=X.first[q.id]||{ok:0,n:fl};fo+=f.ok;fn+=f.n;no+=okCount(q);nn+=fl});
  att=Object.keys(X.att).reduce(function(s,k){return s+X.att[k]},0);h=cnt(X.hint);return {fo:fo,fn:fn,no:no,nn:nn,att:att,h:h}}
function renderExSummary(){var t=document.getElementById("extable");
  var h='<thead><tr><th class="l">'+B("Question","Soalan")+'</th><th>'+B("Marks","Markah")+'</th><th>'+B("First attempt","First attempt")+'</th><th>'+B("Now","Sekarang")+'</th><th>'+B("Checks","Semakan")+'</th><th>'+B("Hint","Petunjuk")+'</th><th class="l">'+B("Confidence","Keyakinan")+'</th></tr></thead><tbody>';
  QX.forEach(function(q,i){var fl=fieldsOf(q).length,c=X.chk[q.id],f=X.first[q.id],cf=X.confAt[q.id],cl=CONF.filter(function(k){return k[0]===cf})[0];
    h+='<tr><td class="l">'+(i+1)+'</td><td>'+q.getAttribute("data-marks")+(q.getAttribute("data-bonus")?" (bonus)":"")+'</td><td>'+(c&&fl&&f?f.ok+"/"+f.n:"–")+'</td><td>'+(c&&fl?okCount(q)+"/"+fl:"–")+'</td><td>'+(X.att[q.id]||"–")+'</td><td>'+(X.hint[q.id]?"✓":"–")+'</td><td class="l">'+(cl?B(cl[1],cl[2]):"–")+'</td></tr>'});
  t.innerHTML=h+'</tbody>';
  var s=exStats(),mf=estMarks("first"),mn=estMarks("now");
  var cal={sr:0,sw:0,ur:0,uw:0};QX.forEach(function(q){var f=X.first[q.id],cf=X.confAt[q.id];if(!f||!cf||!f.n)return;var right=f.ok===f.n;if(cf==="sure"){right?cal.sr++:cal.sw++}else{right?cal.ur++:cal.uw++}});
  tx(document.getElementById("excal"),"Confidence at first check: sure and fully right "+cal.sr+", sure but not fully right "+cal.sw+", unsure or guessing but fully right "+cal.ur+", unsure or guessing and not fully right "+cal.uw+".",
     "Keyakinan pada semakan pertama: yakin dan betul sepenuhnya "+cal.sr+", yakin tetapi tidak betul sepenuhnya "+cal.sw+", kurang pasti atau teka tetapi betul sepenuhnya "+cal.ur+", kurang pasti atau teka dan tidak betul sepenuhnya "+cal.uw+".");
  var kv=document.getElementById("exkv");
  kv.innerHTML='<div><b>'+cnt(X.chk)+'/10</b><span>'+B("questions checked","soalan disemak")+'</span></div><div><b>'+(s.fn?s.fo+"/"+s.fn:"–")+'</b><span>'+B("fields right, first attempt","medan betul, first attempt")+'</span></div><div><b>'+(s.fn?mf[0].toFixed(1)+"/"+mf[1]:"–")+'</b><span>'+B("estimated marks, first attempt","anggaran markah, first attempt")+'</span></div><div><b>'+s.h+'</b><span>'+B("hints opened","petunjuk dibuka")+'</span></div><div><b>'+(X.done?mmss(X.done):mmss(elapsed()))+'</b><span>'+(X.done?B("time to check all ten","masa untuk menyemak kesemua sepuluh"):B("time on the timer","masa pada timer"))+'</span></div>'}
QX.forEach(function(q){if(X.chk[q.id])checkQ(q,true)});
langHooks.push(function(){QX.forEach(resText);renderExSummary();QX.forEach(function(q){var pk=q.getAttribute("data-plot");if(pk&&X.chk[q.id])plotQ(q,pk)})});
var exArmed=false,exreset=document.getElementById("exreset");
exreset.addEventListener("click",function(){if(!exArmed){exArmed=true;tx(exreset,"Tap again to erase all answers","Tekan sekali lagi untuk memadam semua jawapan");setTimeout(function(){exArmed=false;tx(exreset,"Erase all answers","Padam semua jawapan")},4000);return}
  exArmed=false;tx(exreset,"Erase all answers","Padam semua jawapan");ST.ex=fresh().ex;X=ST.ex;save();
  document.querySelectorAll("article.qx input.ans,article.qx textarea").forEach(function(el){el.value="";el.removeAttribute("data-state")});
  document.querySelectorAll("article.qx .choice,article.qx .multi").forEach(function(g){g.removeAttribute("data-state");g.querySelectorAll("button").forEach(function(b){b.setAttribute("aria-pressed","false")})});
  document.querySelectorAll("article.qx .conf button").forEach(function(b){b.setAttribute("aria-pressed","false")});
  document.querySelectorAll("article.qx .sol,article.qx .hintbox").forEach(function(s){s.hidden=true});document.querySelectorAll("article.qx .sls").forEach(function(b){b.hidden=true});
  document.querySelectorAll("article.qx .res,article.qx .qmeta,article.qx .qplot").forEach(function(r){r.innerHTML=""});tickTimer();renderExSummary();updateProgress()});

/* ---------- exercise timer ---------- */
var tstart=document.getElementById("tstart"),tclock=document.getElementById("tclock"),tpill=document.getElementById("tpill");
function elapsed(){var t=X.timer;return t.el+(t.run?Date.now()-t.t0:0)}
function startTimer(){X.timer.run=true;X.timer.t0=Date.now();save();tickTimer()}
function pauseTimer(){X.timer.el=elapsed();X.timer.run=false;save();tickTimer()}
function tickTimer(){var e=elapsed();tclock.textContent=mmss(e);tclock.style.color=e>3600000?"var(--neg)":"";
  if(X.timer.run)tx(tstart,"Pause","Jeda");else tx(tstart,e>0?"Resume":"Start timer",e>0?"Sambung":"Mula timer");updatePill()}
function updatePill(){var show_=X.timer.run&&current==="exercises";tpill.hidden=!show_;if(show_)tpill.textContent="⏱ "+mmss(elapsed())+" / 60:00"}
tstart.addEventListener("click",function(){if(X.timer.run)pauseTimer();else startTimer()});
document.getElementById("treset").addEventListener("click",function(){X.timer={el:0,run:false,t0:0};X.done=0;save();tickTimer();renderExSummary()});
tpill.addEventListener("click",function(){document.getElementById("extimer").scrollIntoView({behavior:"smooth",block:"center"})});
setInterval(function(){if(X.timer.run)tickTimer()},1000);
langHooks.push(tickTimer);

/* =====================================================================
   Lab
   ===================================================================== */
var LB=ST.lab;
function mkRows(tb,pre){HALTS.forEach(function(h,i){var tr=document.createElement("tr");
  tr.innerHTML='<td class="l">'+h[0]+'</td><td>'+h[1]+'</td><td><input class="rd" type="text" inputmode="decimal" id="'+pre+'-'+i+'" aria-label="reading at '+h[0]+'"></td><td class="a"></td><td class="b"></td><td class="c"></td>';tb.appendChild(tr)})}
var t1b=document.querySelector("#t1 tbody"),t2b=document.querySelector("#t2 tbody");mkRows(t1b,"r1");mkRows(t2b,"r2");
var g1=document.getElementById("g1"),k1=document.getElementById("k1"),m1=document.getElementById("m1"),g2=document.getElementById("g2"),k2=document.getElementById("k2");
g1.value=LB.t1.g;k1.value=LB.t1.k;m1.value=LB.t1.m;g2.value=LB.t2.g;k2.value=LB.t2.k;
HALTS.forEach(function(h,i){var a=document.getElementById("r1-"+i),b=document.getElementById("r2-"+i);a.value=LB.t1.v[i]||"";b.value=LB.t2.v[i]||"";
  a.addEventListener("input",function(){LB.t1.v[i]=a.value;save()});b.addEventListener("input",function(){LB.t2.v[i]=b.value;save()})});
[["g1","t1","g"],["k1","t1","k"],["m1","t1","m"],["g2","t2","g"],["k2","t2","k"]].forEach(function(p){var el=document.getElementById(p[0]);el.addEventListener("change",function(){LB[p[1]][p[2]]=el.value;save()})});
function lab1(){var key=g1.value,c=Number(k1.value)||0.05,m=Number(m1.value)||2.5,data=[];
  HALTS.forEach(function(h,i){var tr=t1b.rows[i],th=IL[key](h[1]),r=parseNum(document.getElementById("r1-"+i).value);tr.querySelector(".b").textContent=f3(th);
    if(r===null){tr.querySelector(".a").textContent="";tr.querySelector(".c").textContent="";return}
    var e=r*c/m,d=e-th;data.push({x:h[1],eta:e});tr.querySelector(".a").textContent=f3(e);
    tr.querySelector(".c").innerHTML=(d>=0?"+":"")+f3(d)+(Math.abs(th)>=0.1?' <span class="muted">('+(d/Math.abs(th)*100).toFixed(1).replace("-","−")+' %)</span>':'')});
  LAB={key:key,points:{key:key,data:data,label:L2("○ your readings","○ bacaan anda")}};renderFig(document.querySelector('svg[data-fig="lab1"]'));
  var big=data.length?data.reduce(function(a,p){var d=Math.abs(p.eta-IL[key](p.x));return d>a.d?{d:d,x:p.x}:a},{d:-1,x:0}):null,s1=document.getElementById("s1");
  if(!big){tx(s1,"Enter at least one reading.","Masukkan sekurang-kurangnya satu bacaan.");return}
  LB.done1=true;LB.big={d:big.d,h:haltName(big.x),g:key.slice(2)};save();updateProgress();
  var en="Largest absolute difference "+big.d.toFixed(3)+" at halt "+haltName(big.x),ms="Perbezaan mutlak terbesar "+big.d.toFixed(3)+" di halt "+haltName(big.x);
  if(big.d<=0.03){en+=", within the ±0.03 expected.";ms+=", dalam lingkungan ±0.03 yang dijangka."}
  else if(big.d<=0.045){en+=", slightly more than the ±0.03 expected (two divisions): repeat that halt if time allows.";ms+=", sedikit melebihi ±0.03 yang dijangka (dua division): ulang halt itu jika masa mengizinkan."}
  else{en+=", well beyond the ±0.03 expected: check that reading and repeat the halt.";ms+=", jauh melebihi ±0.03 yang dijangka: semak bacaan itu dan ulang halt tersebut."}
  tx(s1,en,ms)}
document.getElementById("c1").addEventListener("click",lab1);
document.getElementById("e1").addEventListener("click",function(){g1.value="R_A";k1.value="0.05";m1.value="2.5";LB.t1={g:"R_A",k:"0.05",m:"2.5",v:PRACTICE.map(String)};HALTS.forEach(function(h,i){document.getElementById("r1-"+i).value=PRACTICE[i]});save();lab1();
  var s1=document.getElementById("s1");tx(s1,"Example readings (illustrative, not measured). "+s1.getAttribute("data-en"),"Bacaan contoh (ilustrasi, bukan ukuran). "+s1.getAttribute("data-ms"))});
document.getElementById("x1").addEventListener("click",function(){HALTS.forEach(function(h,i){document.getElementById("r1-"+i).value="";var tr=t1b.rows[i];tr.querySelector(".a").textContent="";tr.querySelector(".b").textContent="";tr.querySelector(".c").textContent=""});
  LB.t1.v=[];LB.done1=false;LB.big=null;save();updateProgress();LAB={key:g1.value,points:null};renderFig(document.querySelector('svg[data-fig="lab1"]'));tx(document.getElementById("s1"),"","")});
function lab2(){var key=g2.value,c=Number(k2.value)||0.05,any=false;
  HALTS.forEach(function(h,i){var tr=t2b.rows[i],th=comp(key,h[1]),r=parseNum(document.getElementById("r2-"+i).value);tr.querySelector(".b").textContent=f2(th)+(h[1]+100>xF?" *":"");
    if(r===null){tr.querySelector(".a").textContent="";tr.querySelector(".c").textContent="";return}any=true;var v=r*c;tr.querySelector(".a").textContent=f2(v);tr.querySelector(".c").textContent=(v-th>=0?"+":"")+f2(v-th)});
  if(any){LB.done2=true;save();updateProgress()}
  tx(document.getElementById("s2"),"* 5 kg mass only; the 2.5 kg mass would be beyond F.","* jisim 5 kg sahaja; jisim 2.5 kg akan berada di luar F.")}
document.getElementById("c2").addEventListener("click",lab2);
/* illustrative Test 2 readings: theory in divisions with a fixed ±1–2 division scatter */
var NZ2=[1,-1,0,2,-1,1,-2,0,1,-1,0,1,0,-1,1,0,0];
document.getElementById("e2").addEventListener("click",function(){var key=g2.value,c=Number(k2.value)||0.05;LB.t2.g=key;
  HALTS.forEach(function(h,i){var th=comp(key,h[1]),r=Math.round(th/c)+(Math.abs(th)<1e-9?0:NZ2[i]);document.getElementById("r2-"+i).value=r;LB.t2.v[i]=String(r)});save();lab2();
  var s2=document.getElementById("s2");tx(s2,"Example readings (illustrative, not measured). "+s2.getAttribute("data-en"),"Bacaan contoh (ilustrasi, bukan ukuran). "+s2.getAttribute("data-ms"))});
document.getElementById("x2").addEventListener("click",function(){HALTS.forEach(function(h,i){document.getElementById("r2-"+i).value="";var tr=t2b.rows[i];tr.querySelector(".a").textContent="";tr.querySelector(".b").textContent="";tr.querySelector(".c").textContent=""});LB.t2.v=[];LB.done2=false;save();updateProgress();tx(document.getElementById("s2"),"","")});
function copyText(txt,statusEl){function fallback(){var ta=document.createElement("textarea");ta.value=txt;ta.style.minHeight="8em";ta.setAttribute("aria-label","Text to copy");statusEl.innerHTML="";statusEl.appendChild(document.createTextNode(L2("Copy this text: ","Salin teks ini: ")));statusEl.appendChild(ta);ta.select()}
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(function(){tx(statusEl,"Copied.","Disalin.")}).catch(fallback)}else fallback()}
function tableCSV(tb,head){var lines=[head];[].slice.call(tb.rows).forEach(function(tr){var c=tr.cells;lines.push([c[0].textContent,c[1].textContent,c[2].querySelector("input").value,c[3].textContent,c[4].textContent,c[5].textContent].map(function(s){return '"'+String(s).replace(/−/g,"-").replace(/"/g,'""')+'"'}).join(","))});return lines.join("\n")}
document.getElementById("p1").addEventListener("click",function(){lab1();copyText(tableCSV(t1b,"halt,x_mm,reading_div,eta_test,eta_theory,difference"),document.getElementById("s1"))});
document.getElementById("p2").addEventListener("click",function(){lab2();copyText(tableCSV(t2b,"halt,x_5kg_mm,reading_div,R_test_kgf,R_theory_kgf,difference_kgf"),document.getElementById("s2"))});
["ck1","ck2","ck3","ck4","ck5"].forEach(function(id){var el=document.getElementById(id);el.checked=!!LB.ck[id];el.addEventListener("change",function(){LB.ck[id]=el.checked;save();updateProgress()})});
["eqa","eqb","eqe","eqf","eqm","eqk"].forEach(function(id){var el=document.getElementById(id);if(LB.eq[id]!=null)el.value=LB.eq[id];el.addEventListener("input",function(){LB.eq[id]=el.value;save();eqCheck()})});
function eqCheck(){var g=function(id){return parseNum(document.getElementById(id).value)||0};var k=g("eqk")||0.05,m=g("eqm")||2.5,s=(g("eqa")+g("eqb")+g("eqe")+g("eqf"))*k,dv=(s-m)/k;
  var ok=Math.abs(dv)<=2,dvs=(dv>=0?"+":"")+dv.toFixed(1).replace("-","−");
  document.getElementById("eqout").innerHTML=L2("Sum = <b class='num'>"+f2(s)+" kgf</b> against "+f2(m)+" kgf applied ("+dvs+" divisions). "+(ok?"Acceptable: within two divisions.":"More than two divisions out: re-zero the gauges and repeat this halt."),
    "Jumlah = <b class='num'>"+f2(s)+" kgf</b> berbanding "+f2(m)+" kgf dikenakan ("+dvs+" division). "+(ok?"Boleh diterima: dalam lingkungan dua division.":"Melebihi dua division: re-zero gauge dan ulang halt ini."))}
langHooks.push(eqCheck,function(){if(LB.done1)lab1();if(LB.done2)lab2()});

/* ---------- glossary search ---------- */
var gfilter=document.getElementById("gfilter");
gfilter.addEventListener("input",function(){var q=gfilter.value.trim().toLowerCase(),shown=0;
  document.querySelectorAll("#v-glossary .gloss tr").forEach(function(tr){var hit=!q||tr.textContent.toLowerCase().indexOf(q)>=0;tr.hidden=!hit;if(hit)shown++});
  document.getElementById("gnone").hidden=shown>0});

/* =====================================================================
   Short-notes drawer
   ===================================================================== */
var drawer=document.getElementById("drawer"),scrim=document.getElementById("scrim"),snbtn=document.getElementById("snbtn"),drawerOpen=false,drawerTyped=false;
function openDrawer(){drawerOpen=true;drawer.classList.add("open");drawer.setAttribute("aria-hidden","false");scrim.hidden=false;snbtn.setAttribute("aria-expanded","true");if(!drawerTyped){drawerTyped=true;typeset(drawer)}document.getElementById("snclose").focus()}
function closeDrawer(){drawerOpen=false;drawer.classList.remove("open");drawer.setAttribute("aria-hidden","true");scrim.hidden=true;snbtn.setAttribute("aria-expanded","false");snbtn.focus()}
snbtn.addEventListener("click",function(){drawerOpen?closeDrawer():openDrawer()});
document.getElementById("snclose").addEventListener("click",closeDrawer);scrim.addEventListener("click",closeDrawer);

/* =====================================================================
   Start: next step and learning record
   ===================================================================== */
function secTitle(id){var h=document.querySelector("#"+id+" > h2 ."+(ST.lang==="ms"?"ms":"en"));return h?h.textContent:id}
function nextStep(){var p=parts();
  for(var i=0;i<NSECS.length;i++)if(!ST.read[NSECS[i]])return {v:"notes",a:NSECS[i],en:"Notes · "+secTitle(NSECS[i])+" (≈ "+document.getElementById(NSECS[i]).getAttribute("data-rt")+" min)",ms:"Nota · "+secTitle(NSECS[i])+" (≈ "+document.getElementById(NSECS[i]).getAttribute("data-rt")+" min)"};
  if(p.explorer[0]<6)return {v:"explorer",a:"qlist",en:"Explorer · prediction questions ("+p.explorer[0]+" of 6 answered)",ms:"Explorer · prediction question ("+p.explorer[0]+" daripada 6 dijawab)"};
  for(var j=0;j<QX.length;j++)if(!X.chk[QX[j].id])return {v:"exercises",a:QX[j].id,en:"Exercises · Question "+(j+1)+" ("+p.exercises[0]+" of 10 checked)",ms:"Latihan · Soalan "+(j+1)+" ("+p.exercises[0]+" daripada 10 disemak)"};
  if(p.lab[0]<7)return {v:"lab",a:null,en:"Lab · checklist, Test 1 and Test 2 ("+p.lab[0]+" of 7 items)",ms:"Makmal · senarai semak, Test 1 dan Test 2 ("+p.lab[0]+" daripada 7 item)"};
  var miss=QX.filter(function(q){var f=X.first[q.id];return f&&f.n&&f.ok<f.n}).map(function(q){return "Q"+q.id.slice(1)});
  return {v:miss.length?"exercises":"start",a:null,en:"All parts done."+(miss.length?" Questions not fully right at the first attempt: "+miss.join(", ")+".":""),ms:"Semua bahagian selesai."+(miss.length?" Soalan yang tidak betul sepenuhnya pada first attempt: "+miss.join(", ")+".":"")}}
var NEXT=null;
document.getElementById("nextbtn").addEventListener("click",function(){if(NEXT)goTo(NEXT.v,NEXT.a)});
function mins(s){return Math.round((s||0)/60)}
function recordRows(){var p=parts(),s=exStats(),mf=estMarks("first"),P=ST.pred,pc=0;Object.keys(P.ans).forEach(function(k){if(P.ans[k]===QUESTIONS[k].a)pc++});
  var qok=QCS.filter(function(q){return ST.qc[q]&&ST.qc[q].ok}).length,qn=QCS.filter(function(q){return ST.qc[q]}).length,tm=ST.time;
  return [
   [L2("Notes","Nota"),p.notes[0]+"/8 "+L2("sections read","section dibaca"),L2("quick checks right first time: ","semakan pantas betul kali pertama: ")+qok+"/"+qn,mins(tm.notes)],
   ["Slides",p.slides[0]+"/"+p.slides[1]+" "+L2("viewed","dilihat"),"",mins(tm.slides)],
   ["Explorer",p.explorer[0]+"/6 "+L2("predictions","prediction"),Object.keys(P.ans).length?L2("correct ","betul ")+pc+"/"+Object.keys(P.ans).length+(P.t1?L2(" · time "," · masa ")+mmss(P.t1-P.t0):""):"",mins(tm.explorer)],
   [L2("Exercises","Latihan"),p.exercises[0]+"/10 "+L2("checked","disemak"),s.fn?L2("first attempt ","first attempt ")+s.fo+"/"+s.fn+L2(" fields (≈ "," medan (≈ ")+mf[0].toFixed(1)+"/"+mf[1]+L2(" marks) · now "," markah) · sekarang ")+s.no+"/"+s.nn+L2(" · hints "," · petunjuk ")+s.h+L2(" · timer "," · timer ")+mmss(X.done||elapsed()):"",mins(tm.exercises)],
   [L2("Lab","Makmal"),p.lab[0]+"/7 "+L2("items","item"),LB.big?L2("Test 1 gauge "+LB.big.g+": largest difference "+LB.big.d.toFixed(3)+" at halt "+LB.big.h,"Test 1 gauge "+LB.big.g+": perbezaan terbesar "+LB.big.d.toFixed(3)+" di halt "+LB.big.h):"",mins(tm.lab)]]}
function renderStart(){NEXT=nextStep();document.getElementById("nexttxt").textContent=L2(NEXT.en,NEXT.ms);
  var rows=recordRows(),p=parts(),pct=document.getElementById("ppct").textContent;
  var h='<div class="tbl"><table class="stats"><thead><tr><th class="l">'+B("Part","Bahagian")+'</th><th class="l">'+B("Progress","Kemajuan")+'</th><th class="l">'+B("Detail","Butiran")+'</th><th>'+B("Time (min)","Masa (min)")+'</th></tr></thead><tbody>';
  rows.forEach(function(r){h+='<tr><td class="l">'+r[0]+'</td><td class="l">'+r[1]+'</td><td class="l">'+(r[2]||"–")+'</td><td>'+r[3]+'</td></tr>'});
  document.getElementById("record").innerHTML=h+'</tbody></table></div><p class="sumline" style="margin-top:8px">'+L2("Overall progress ","Kemajuan keseluruhan ")+pct+'</p>'}
langHooks.push(function(){if(current==="start")renderStart()});
document.getElementById("reccopy").addEventListener("click",function(){var rows=recordRows(),d=new Date();
  var lines=["SEAA 3012 Lab S2 Influence Lines · "+L2("learning record","rekod pembelajaran")+" · "+d.toISOString().slice(0,16).replace("T"," "),L2("Overall progress ","Kemajuan keseluruhan ")+document.getElementById("ppct").textContent];
  rows.forEach(function(r){lines.push(r[0]+": "+r[1]+(r[2]?" · "+r[2]:"")+" · "+r[3]+" min")});copyText(lines.join("\n"),document.getElementById("recmsg"))});
var recArmed=false,recreset=document.getElementById("recreset");
recreset.addEventListener("click",function(){if(!recArmed){recArmed=true;tx(recreset,"Tap again to erase all progress and answers","Tekan sekali lagi untuk memadam semua kemajuan dan jawapan");setTimeout(function(){recArmed=false;tx(recreset,"Reset all progress","Set semula semua kemajuan")},4000);return}
  var keep={lang:ST.lang,theme:ST.theme};ST=Object.assign(fresh(),keep);saveNow();try{location.reload()}catch(e){}});

/* =====================================================================
   Boot
   ===================================================================== */
applyLang();buildTables();setNmode(ST.nmode);syncRead();renderPreds();
setX(E.x);eqCheck();tickTimer();renderExSummary();
if(LB.done1)lab1();if(LB.done2)lab2();
var start=(location.hash||"").replace("#","");if(VIEWS.indexOf(start)<0)start="start";
show(start,true);updateProgress();
var rt=null;window.addEventListener("resize",function(){clearTimeout(rt);rt=setTimeout(rerenderFigs,150)});
})();
