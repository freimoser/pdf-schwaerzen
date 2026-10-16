// Web Worker: alle PDF-Arbeit läuft hier, lokal im Browser.
// Engine erst laden, Nachrichten sofort annehmen (Top-Level-Await in mupdf.js)
const ready=Promise.all([import("./vendor/mupdf/mupdf.js"),import("./core.js")]);let mupdf,C;
let bytes=null,doc=null;
const ok=(id,r,t)=>postMessage({id,ok:true,r},t||[]);
onmessage=async e=>{const {id,cmd,a}=e.data;try{if(!C)[mupdf,C]=await ready;
 if(cmd==="sample"){const b=C.makeSample(mupdf);return ok(id,b,[b.buffer]);}
 if(cmd==="open"){bytes=new Uint8Array(a.buf);const o=C.open(mupdf,bytes,a.pw);if(o.needsPassword)return ok(id,{needsPassword:true});doc=o.doc;
  return ok(id,{pages:C.pageInfo(doc).map(p=>({w:p.w,h:p.h,x0:p.x0,y0:p.y0,scanned:p.scanned,text:p.text})),findings:C.findings(doc)});}
 if(cmd==="render"){const p=doc.loadPage(a.page);const pm=p.toPixmap([a.scale,0,0,a.scale,0,0],mupdf.ColorSpace.DeviceRGB,false,true);const png=pm.asPNG().slice();return ok(id,png,[png.buffer]);}
 if(cmd==="search")return ok(id,C.search(doc,a.q,a.cs));
 if(cmd==="detect"){const res=[];const names=a.names||[];const pi=C.pageInfo(doc);const done=new Set();
  for(const p of pi)for(const d of C.detect(p.text,names)){if(done.has(d.text))continue;done.add(d.text);for(const h of C.search(doc,d.text,false))res.push({...d,...h});}
  return ok(id,res);}
 if(cmd==="bookings")return ok(id,C.bookings(doc));
 if(cmd==="apply"){const work=C.open(mupdf,bytes,a.pw).doc;const out=C.apply(mupdf,work,a.marks,a.opt);
  const report=C.verify(mupdf,out,a.marks,a.terms,a.opt.clean!==false);return ok(id,{out,report},[out.buffer]);}
 throw new Error("unbekannt");
}catch(err){postMessage({id,ok:false,err:String(err&&err.message||err)});}};
