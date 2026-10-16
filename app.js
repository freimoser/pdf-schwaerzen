// PDF sicher schwärzen – Oberfläche. Alles lokal, kein Upload.
(function(){
const $=s=>document.querySelector(s);let W=null,seq=0;const pend={};
function call(cmd,a,t){if(!W){W=new Worker("/pdf-schwaerzen/worker.js",{type:"module"});W.onmessage=e=>{const p=pend[e.data.id];delete pend[e.data.id];e.data.ok?p[0](e.data.r):p[1](new Error(e.data.err));};W.onerror=e=>{msg("Die Schwärzungs-Engine konnte nicht geladen werden: "+(e.message||"unbekannter Fehler"),1);Object.values(pend).forEach(p=>p[1](new Error("Engine-Fehler")));};}
 return new Promise((res,rej)=>{const id=++seq;pend[id]=[res,rej];W.postMessage({id,cmd,a},t||[]);});}
let files=[],cur=null,info=null,marks=[],sugs=[],pw="",outUrl=null;const SCALE=1.5;
const msg=(t,err)=>{const m=$("#msg");m.hidden=!t;m.textContent=t||"";m.className="msg"+(err?" err":"");};
function addFiles(list){for(const f of list)if(/pdf$/i.test(f.name)||f.type==="application/pdf")files.push(f);renderFileList();if(files.length&&!cur)load(files[0]);}
function renderFileList(){const s=$("#files");s.hidden=files.length<2;s.innerHTML=files.map((f,i)=>`<option value="${i}"${f===cur?" selected":""}>${f.name.replace(/</g,"")}</option>`).join("");}
$("#files").onchange=e=>load(files[+e.target.value]);
async function load(f){cur=f;marks=[];sugs=[];pw="";renderFileList();msg("PDF wird lokal geöffnet … (beim ersten Mal wird die Schwärzungs-Engine geladen)");
 try{const buf=await f.arrayBuffer();let r=await call("open",{buf},[buf]);
  while(r.needsPassword){const p=prompt("Diese PDF ist passwortgeschützt. Bitte Passwort eingeben (es bleibt auf deinem Gerät):");if(p===null){msg("Ohne Passwort kann die PDF nicht geöffnet werden.",1);return;}pw=p;const b2=await f.arrayBuffer();r=await call("open",{buf:b2,pw},[b2]);}
  info=r;msg("");$("#app").hidden=false;$("#res").hidden=true;
  $("#find").innerHTML=r.findings.length?"Gefunden (wird beim Bereinigen entfernt): "+r.findings.map(x=>x.replace(/</g,"&lt;")).join(" · "):"Keine Metadaten oder versteckten Inhalte gefunden.";
  const sc=r.pages.filter(p=>p.scanned).length;$("#scan").hidden=!sc;$("#scan").textContent=sc?`${sc} Seite(n) enthalten keinen Text (vermutlich gescannt). Die automatische Erkennung und Suche finden dort nichts – Rechtecke ziehen funktioniert trotzdem und entfernt die Bildpixel.`:"";
  await drawPages();}catch(e){msg("Die Datei konnte nicht geöffnet werden. Ist es eine gültige, unbeschädigte PDF? ("+e.message+")",1);}}
async function drawPages(){const pv=$("#pv");pv.innerHTML="";
 for(let i=0;i<info.pages.length;i++){const p=info.pages[i];const d=document.createElement("div");d.className="pg";d.dataset.p=i;d.style.width="100%";d.style.maxWidth=Math.round(p.w*SCALE)+"px";d.style.aspectRatio=p.w+"/"+p.h;
  const img=document.createElement("img");img.alt="Seite "+(i+1);img.width=Math.round(p.w*SCALE);img.height=Math.round(p.h*SCALE);d.appendChild(img);pv.appendChild(d);bindDraw(d,i);
  if(i<3)await renderPage(d,i);}
 const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting&&!en.target.dataset.r){renderPage(en.target,+en.target.dataset.p);}}),{root:null,rootMargin:"400px"});
 pv.querySelectorAll(".pg").forEach(d=>io.observe(d));drawBoxes();}
async function renderPage(d,i){d.dataset.r=1;const png=await call("render",{page:i,scale:SCALE});d.querySelector("img").src=URL.createObjectURL(new Blob([png],{type:"image/png"}));}
function toPct(i,r){const p=info.pages[i];return [(r[0]-p.x0)/p.w*100,(r[1]-p.y0)/p.h*100,(r[2]-r[0])/p.w*100,(r[3]-r[1])/p.h*100];}
function drawBoxes(){document.querySelectorAll(".bx").forEach(b=>b.remove());
 const put=(m,cls,k,fn)=>{const d=document.querySelector(`.pg[data-p="${m.page}"]`);if(!d)return;const [x,y,w,h]=toPct(m.page,m.rect);const b=document.createElement("div");b.className="bx "+cls;b.style.cssText=`left:${x}%;top:${y}%;width:${w}%;height:${h}%`;
  const x2=document.createElement("button");x2.type="button";x2.textContent="×";x2.setAttribute("aria-label","Schwärzung entfernen");x2.onclick=fn;b.appendChild(x2);d.appendChild(b);};
 marks.forEach((m,k)=>put(m,"",k,()=>{marks.splice(k,1);drawBoxes();}));
 sugs.forEach((s,k)=>{if(!s.on)return;put(s,"sug",k,()=>{s.on=false;renderSugs();drawBoxes();});});
 $("#cnt").textContent=`${marks.length} Schwärzung(en), ${sugs.filter(s=>s.on).length} ausgewählte Vorschläge`;}
function bindDraw(d,i){let st=null,box=null;
 d.addEventListener("pointerdown",e=>{if(e.target.tagName==="BUTTON")return;const r=d.getBoundingClientRect();st=[(e.clientX-r.left)/r.width,(e.clientY-r.top)/r.height];box=document.createElement("div");box.className="bx";d.appendChild(box);d.setPointerCapture(e.pointerId);e.preventDefault();});
 d.addEventListener("pointermove",e=>{if(!st)return;const r=d.getBoundingClientRect();const c=[(e.clientX-r.left)/r.width,(e.clientY-r.top)/r.height];box.style.cssText=`left:${Math.min(st[0],c[0])*100}%;top:${Math.min(st[1],c[1])*100}%;width:${Math.abs(c[0]-st[0])*100}%;height:${Math.abs(c[1]-st[1])*100}%`;});
 const end=e=>{if(!st)return;const r=d.getBoundingClientRect();const c=[Math.max(0,Math.min(1,(e.clientX-r.left)/r.width)),Math.max(0,Math.min(1,(e.clientY-r.top)/r.height))];const p=info.pages[i];
  const x0=Math.min(st[0],c[0]),x1=Math.max(st[0],c[0]),y0=Math.min(st[1],c[1]),y1=Math.max(st[1],c[1]);st=null;box.remove();
  if((x1-x0)*p.w>3&&(y1-y0)*p.h>3)marks.push({page:i,rect:[p.x0+x0*p.w,p.y0+y0*p.h,p.x0+x1*p.w,p.y0+y1*p.h],term:null});drawBoxes();};
 d.addEventListener("pointerup",end);d.addEventListener("pointercancel",()=>{st=null;box&&box.remove();});}
function renderSugs(){const el=$("#sugs");if(!sugs.length){el.innerHTML="<p class=small>Keine Vorschläge.</p>";return;}
 el.innerHTML=sugs.map((s,k)=>`<label><input type="checkbox" data-k="${k}"${s.on?" checked":""}><span><strong>${s.label}</strong> · S. ${s.page+1}: ${s.text.replace(/</g,"&lt;")}</span></label>`).join("");
 el.querySelectorAll("input").forEach(c=>c.onchange=()=>{sugs[+c.dataset.k].on=c.checked;drawBoxes();});}
$("#auto").onclick=async()=>{msg("Suche nach Personendaten …");const names=$("#names").value.split(/[\n,;]/).map(s=>s.trim()).filter(Boolean);
 const r=await call("detect",{names});sugs=r.map(x=>({...x,on:false}));msg(r.length?"":"Keine Personendaten erkannt. Prüfe die PDF trotzdem selbst.");renderSugs();drawBoxes();$("#allSug").hidden=!sugs.length;};
$("#allSug").onclick=()=>{sugs.forEach(s=>s.on=true);renderSugs();drawBoxes();};
$("#kto").onclick=async()=>{const r=await call("bookings",{});const mode=$("#ktoMode").value;
 if(!r.length){msg("Keine Buchungszeilen (Zeilen mit Datum und Betrag) erkannt.");return;}msg("");
 sugs=sugs.concat(r.map(b=>mode==="line"||!b.midRect?{label:"Buchungszeile",text:b.text,page:b.page,rect:b.rect,on:false}:{label:"Buchung ohne Datum/Betrag",text:b.mid,page:b.page,rect:b.midRect,on:false}));renderSugs();drawBoxes();$("#allSug").hidden=false;};
$("#doSearch").onclick=async()=>{const q=$("#q").value.trim();if(!q)return;const r=await call("search",{q,cs:$("#cs").checked});
 r.forEach(h=>marks.push({...h,term:q}));msg(r.length?`${r.length} Vorkommen von „${q}“ zum Schwärzen markiert.`:`„${q}“ wurde nicht gefunden.`);drawBoxes();};
$("#q").addEventListener("keydown",e=>{if(e.key==="Enter")$("#doSearch").click();});
$("#clear").onclick=()=>{marks=[];sugs.forEach(s=>s.on=false);renderSugs();drawBoxes();};
$("#apply").onclick=async()=>{const all=marks.concat(sugs.filter(s=>s.on).map(s=>({page:s.page,rect:s.rect,term:s.text})));
 if(!all.length&&!$("#clean").checked){msg("Noch nichts markiert. Ziehe ein Rechteck, suche einen Begriff oder übernimm Vorschläge.",1);return;}
 msg("Schwärzungen werden dauerhaft angewendet und geprüft …");$("#apply").disabled=true;
 try{const buf=await cur.arrayBuffer();await call("open",{buf,pw},[buf]);
  const terms=[...new Set(all.map(m=>m.term).filter(Boolean))];
  const r=await call("apply",{marks:all.map(m=>({page:m.page,rect:m.rect})),terms,pw,opt:{clean:$("#clean").checked,label:$("#label").checked}});
  const good=r.report.every(x=>x.ok);$("#res").hidden=false;
  $("#rep").innerHTML=r.report.map(x=>`<li class="${x.ok?"g":"r"}">${x.ok?"✔":"✖"} <strong>${x.what.replace(/</g,"&lt;")}</strong>: ${x.detail.replace(/</g,"&lt;")}</li>`).join("");
  if(outUrl)URL.revokeObjectURL(outUrl);const dl=$("#dl");
  if(good){outUrl=URL.createObjectURL(new Blob([r.out],{type:"application/pdf"}));dl.href=outUrl;dl.download=cur.name.replace(/\.pdf$/i,"")+"_geschwaerzt.pdf";dl.hidden=false;$("#bad").hidden=true;}
  else{dl.hidden=true;$("#bad").hidden=false;}
  msg("");$("#res").scrollIntoView({behavior:"smooth"});}
 catch(e){msg("Fehler beim Schwärzen: "+e.message,1);}finally{$("#apply").disabled=false;}};
const drop=$("#drop");["dragover","dragenter"].forEach(t=>drop.addEventListener(t,e=>{e.preventDefault();drop.classList.add("over");}));
["dragleave","drop"].forEach(t=>drop.addEventListener(t,()=>drop.classList.remove("over")));
drop.addEventListener("drop",e=>{e.preventDefault();addFiles(e.dataTransfer.files);});
$("#fileIn").onchange=e=>addFiles(e.target.files);
$("#sample").onclick=async()=>{const b=await call("sample",{});addFiles([new File([b],"beispiel-arztbrief.pdf",{type:"application/pdf"})]);if(cur&&cur.name!=="beispiel-arztbrief.pdf")load(files[files.length-1]);};
})();
