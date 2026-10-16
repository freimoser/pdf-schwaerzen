// PDF sicher schwärzen – Kernlogik (Browser-Worker und Node-Test). AGPL-3.0, nutzt MuPDF.
// Prüfverfahren: IBAN nach ISO 13616 / ISO 7064 Mod 97-10; Kreditkarte nach Luhn (ISO/IEC 7812-1);
// Steuer-ID nach § 139b AO, Prüfziffer ISO 7064 Mod 11,10 (BZSt-Spezifikation). Siehe quellen.md.
export function ibanOk(s){s=s.replace(/\s/g,"").toUpperCase();if(!/^[A-Z]{2}\d{2}[A-Z0-9]{10,30}$/.test(s))return false;
 const r=(s.slice(4)+s.slice(0,4)).replace(/[A-Z]/g,c=>c.charCodeAt(0)-55);let m=0;for(const d of r)m=(m*10+ +d)%97;return m===1;}
export function luhnOk(s){s=s.replace(/\D/g,"");if(s.length<13||s.length>19)return false;let t=0;for(let i=0;i<s.length;i++){let d=+s[s.length-1-i];if(i%2){d*=2;if(d>9)d-=9}t+=d}return t%10===0;}
export function steuerIdOk(s){s=s.replace(/\s/g,"");if(!/^[1-9]\d{10}$/.test(s))return false;
 const c={};for(const d of s.slice(0,10))c[d]=(c[d]||0)+1;const n=Object.values(c);if(!(n.filter(x=>x>1).length===1&&Math.max(...n)<=3))return false;
 let p=10;for(let i=0;i<10;i++){let x=(+s[i]+p)%10;if(x===0)x=10;p=(x*2)%11;}let z=11-p;if(z===10)z=0;return z===+s[10];}
const DET=[
 ["IBAN",/\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){3,7}(?: ?[A-Z0-9]{1,3})?\b/g,ibanOk],
 ["Kreditkarte",/\b(?:\d[ -]?){12,18}\d\b/g,luhnOk],
 ["Steuer-ID",/\b\d{2} ?\d{3} ?\d{3} ?\d{3}\b/g,steuerIdOk],
 ["BIC",/\b[A-Z]{4}DE[A-Z0-9]{2}(?:[A-Z0-9]{3})?\b/g],
 ["Sozialversicherungsnr.",/\b\d{2} ?\d{6} ?[A-Z] ?\d{3}\b/g],
 ["Krankenversichertennr.",/\b[A-Z]\d{9}\b/g],
 ["Geburtsdatum",/\b(?:0?[1-9]|[12]\d|3[01])\.(?:0?[1-9]|1[0-2])\.(?:19|20)\d{2}\b/g,null,/geb|Geburt/i],
 ["E-Mail",/\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b/g],
 ["Telefon",/(?:\+49|\b0)[1-9][\d \/-]{6,14}\d\b/g],
 ["PLZ + Ort",/\b\d{5} [A-ZÄÖÜ][a-zäöüß]+(?:[ -][A-ZÄÖÜ]?[a-zäöüß]+)?/g],
 ["Straße + Nr.",/\b[A-ZÄÖÜ][a-zäöüß-]+(?:straße|strasse|str\.|weg|gasse|platz|allee|ring|damm)\s?\d{1,4}\s?[a-z]?\b/g],
];
export function detect(text,names=[]){const out=[],seen=new Set();
 for(const [label,re,check,ctx] of DET){for(const m of text.matchAll(re)){const v=m[0].trim();if(check&&!check(v))continue;
  if(ctx&&!ctx.test(text.slice(Math.max(0,m.index-40),m.index)))continue;const k=label+v;if(seen.has(k))continue;seen.add(k);out.push({label,text:v});}}
 for(const n of names){const t=n.trim();if(t.length>1&&text.toLowerCase().includes(t.toLowerCase()))out.push({label:"Name (Liste)",text:t});}
 return out.filter(a=>!out.some(b=>b!==a&&b.text.length>a.text.length&&b.text.includes(a.text)));}

export function open(mupdf,buf,pw){const doc=mupdf.Document.openDocument(buf,"application/pdf");
 if(doc.needsPassword()&&!(pw&&doc.authenticatePassword(pw)))return {doc,needsPassword:true};
 return {doc:doc.asPDF?doc.asPDF()||doc:doc,needsPassword:false};}
export function pageInfo(doc){const n=doc.countPages(),pages=[];for(let i=0;i<n;i++){const p=doc.loadPage(i),b=p.getBounds(),t=p.toStructuredText("preserve-whitespace").asText();pages.push({w:b[2]-b[0],h:b[3]-b[1],x0:b[0],y0:b[1],text:t,scanned:t.trim().length<5});}return pages;}
const qr=q=>[Math.min(q[0],q[4]),Math.min(q[1],q[3]),Math.max(q[2],q[6]),Math.max(q[5],q[7])];
export function search(doc,needle,caseSens){const res=[];const n=doc.countPages();
 for(let i=0;i<n;i++){const st=doc.loadPage(i).toStructuredText("preserve-whitespace");
  if(caseSens){const txt=st.asText();if(!txt.includes(needle))continue;}
  for(const hit of st.search(needle,caseSens?{}:undefined)||[])res.push({page:i,rect:hit.map(qr).reduce((a,r)=>[Math.min(a[0],r[0]),Math.min(a[1],r[1]),Math.max(a[2],r[2]),Math.max(a[3],r[3])])});}
 return res;}
export function lines(doc,i){const out=[];const j=JSON.parse(doc.loadPage(i).toStructuredText("preserve-whitespace").asJSON());
 for(const b of j.blocks||[])for(const l of b.lines||[])out.push({text:l.text,rect:[l.bbox.x,l.bbox.y,l.bbox.x+l.bbox.w,l.bbox.y+l.bbox.h]});return out;}
export function findings(doc){const f=[];const keys=["info:Title","info:Author","info:Subject","info:Keywords","info:Creator","info:Producer","info:CreationDate","info:ModDate"];
 for(const k of keys){const v=doc.getMetaData(k);if(v)f.push(k.slice(5)+": "+v);}
 const root=doc.getTrailer().get("Root");for(const [k,l] of [["Metadata","XMP-Metadaten"],["Outlines","Lesezeichen"],["AcroForm","Formularfelder"],["OpenAction","Startaktion"],["Names","Namensbaum (eingebettete Dateien/JavaScript)"]])if(root.get(k)&&!root.get(k).isNull())f.push(l);
 let a=0;for(let i=0;i<doc.countPages();i++)a+=doc.loadPage(i).getAnnotations().length;if(a)f.push(a+" Kommentare/Anmerkungen");return f;}
// marks: [{page, rect:[x0,y0,x1,y1]}] in PDF-Seitenkoordinaten (MuPDF, Ursprung oben links)
export function apply(mupdf,doc,marks,opt={}){const clean=opt.clean!==false;
 for(let i=0;i<doc.countPages();i++){const pm=marks.filter(m=>m.page===i);if(!pm.length)continue;const p=doc.loadPage(i);
  for(const m of pm){const a=p.createAnnotation("Redact");a.setRect(m.rect);if(opt.label)a.setOverlayText?.("geschwärzt");a.update?.();}
  p.applyRedactions(true,mupdf.PDFPage.REDACT_IMAGE_PIXELS,mupdf.PDFPage.REDACT_LINE_ART_REMOVE_IF_COVERED,mupdf.PDFPage.REDACT_TEXT_REMOVE);}
 if(clean){const tr=doc.getTrailer();const info=tr.get("Info");if(info&&!info.isNull())tr.delete("Info");
  const root=tr.get("Root");for(const k of ["Metadata","Outlines","AcroForm","OpenAction","AA","Names","PieceInfo","StructTreeRoot","MarkInfo","SpiderInfo"])root.delete(k);
  for(let i=0;i<doc.countPages();i++){const p=doc.loadPage(i);for(const a of p.getAnnotations())p.deleteAnnotation(a);const o=p.getObject();o.delete("AA");o.delete("Metadata");o.delete("PieceInfo");}}
 return doc.saveToBuffer(clean?"garbage=4,compress,clean,sanitize":"garbage=1,compress").asUint8Array().slice();}
// Prüfung der fertigen Datei
export function verify(mupdf,bytes,marks,terms,clean){const doc=mupdf.Document.openDocument(bytes,"application/pdf").asPDF();const res=[];
 for(const [n,m] of marks.entries()){const p=doc.loadPage(m.page);const r=m.rect;let hit="";
  p.toStructuredText("preserve-whitespace").walk({onChar(c,o,f,s,q){const x=(q[0]+q[2]+q[4]+q[6])/4,y=(q[1]+q[3]+q[5]+q[7])/4;if(x>r[0]&&x<r[2]&&y>r[1]&&y<r[3]&&c.trim())hit+=c;}});
  res.push({ok:!hit,what:`Schwärzung ${n+1} (Seite ${m.page+1})`,detail:hit?`Unter der Fläche steht noch Text: „${hit.slice(0,40)}“`:"Kein Text mehr unter der Fläche"});}
 let all="";for(let i=0;i<doc.countPages();i++)all+=doc.loadPage(i).toStructuredText("preserve-whitespace").asText()+"\n";
 const raw=new TextDecoder("latin1").decode(doc.saveToBuffer("decompress").asUint8Array());
 const norm=s=>s.toLowerCase().replace(/\s+/g," ");
 for(const t of terms){const inText=norm(all).includes(norm(t)),inRaw=raw.toLowerCase().includes(t.toLowerCase());
  res.push({ok:!inText&&!inRaw,what:`Begriff „${t}“`,detail:inText?"Noch im Text der PDF auffindbar":inRaw?"Noch in den Dateibytes (z. B. Metadaten) vorhanden":"Nirgends mehr in der Datei"});}
 if(clean){const f=findings(doc);res.push({ok:!f.length,what:"Metadaten & versteckte Inhalte",detail:f.length?"Noch vorhanden: "+f.join(", "):"Alles entfernt"});}
 return res;}
// Beispiel-PDF mit erfundenen Daten
export const SAMPLE_LINES=["Arztbrief (Beispiel mit erfundenen Daten)","Patientin: Erika Musterfrau, geb. 12.03.1980","Musterstraße 12, 80331 München","Tel. 089 1234567, erika.musterfrau@example.de","IBAN DE89 3704 0044 0532 0130 00","Steuer-ID 86095742719","Das Geheimwort steht mitten im Satz, der Rest bleibt lesbar.","Diagnose: Befund unauffällig. Dieser Text bleibt durchsuchbar."];
export function makeSample(mupdf,lines=SAMPLE_LINES,meta=true){const doc=new mupdf.PDFDocument();
 const font=doc.addSimpleFont(new mupdf.Font("Helvetica"),"Latin");
 const res=doc.addObject({Font:{F1:font}});
 const esc=s=>Array.from(s).map(ch=>{const c=ch.charCodeAt(0);if(ch=="("||ch==")"||ch=="\\")return "\\"+ch;return c>126?"\\"+c.toString(8).padStart(3,"0"):ch}).join("");
 let cs="BT /F1 12 Tf 60 780 Td\n"+lines.map((l,i)=>`${i?"0 -18 Td ":""}(${esc(l)}) Tj`).join("\n")+"\nET";
 const page=doc.addPage([0,0,595,842],0,res,cs);doc.insertPage(-1,page);
 if(meta){doc.setMetaData("info:Author","Max Mustermann");doc.setMetaData("info:Title","Befund Erika Musterfrau");}
 return doc.saveToBuffer("compress").asUint8Array().slice();}
// Kontoauszug-Modus: Buchungszeilen = Zeilen mit Datum und Betrag
const DATE=/\b\d{2}\.\d{2}\.(?:\d{2,4})?/g, AMT=/[-+]?\d{1,3}(?:\.\d{3})*,\d{2}(?:\s?[-+HS])?/g;
export function bookings(doc){const out=[];for(let i=0;i<doc.countPages();i++)for(const l of lines(doc,i)){
 if(!/\d{2}\.\d{2}\./.test(l.text)||!/\d,\d{2}/.test(l.text))continue;
 const mid=l.text.replace(DATE,"").replace(AMT,"").trim();let midRect=null;
 if(mid.length>1){const st=doc.loadPage(i).toStructuredText("preserve-whitespace");for(const h of st.search(mid)||[]){const r=h.map(qr).reduce((a,r)=>[Math.min(a[0],r[0]),Math.min(a[1],r[1]),Math.max(a[2],r[2]),Math.max(a[3],r[3])]);if(r[1]>=l.rect[1]-2&&r[3]<=l.rect[3]+2){midRect=r;break;}}}
 out.push({page:i,text:l.text,rect:l.rect,mid,midRect});}return out;}
