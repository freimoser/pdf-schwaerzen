// Kerntest: node test/core-test.mjs  – erzeugt Beispiel-PDF, schwärzt, prüft unabhängig per Rohsuche.
import * as mupdf from "../vendor/mupdf/mupdf.js";
import * as C from "../core.js";
import zlib from "zlib";
const assert=(c,m)=>{if(!c){console.error("FAIL",m);process.exit(1)}console.log("ok",m)};
assert(C.ibanOk("DE89 3704 0044 0532 0130 00")&&!C.ibanOk("DE89 3704 0044 0532 0130 01"),"IBAN-Prüfziffer");
assert(C.steuerIdOk("86095742719")&&!C.steuerIdOk("86095742718"),"Steuer-ID-Prüfziffer");
assert(C.luhnOk("4111 1111 1111 1111")&&!C.luhnOk("4111 1111 1111 1112"),"Luhn");
assert(C.detect("Heute scheint die Sonne über dem Garten.").length===0,"keine Vorschläge ohne Personendaten");
const src=C.makeSample(mupdf);const {doc}=C.open(mupdf,src);
const found=C.detect(C.pageInfo(doc)[0].text);
for(const l of ["IBAN","Steuer-ID","Geburtsdatum","E-Mail","Telefon","PLZ + Ort","Straße + Nr."])assert(found.some(f=>f.label===l),"erkannt: "+l);
const terms=["Geheimwort",...found.map(f=>f.text)];const marks=terms.flatMap(t=>C.search(doc,t,false));
const out=C.apply(mupdf,doc,marks,{clean:true});
assert(C.verify(mupdf,out,marks,terms,true).every(r=>r.ok),"eigene Prüfung grün");
let raw=Buffer.from(out);const s=raw.toString("latin1");for(const m of s.matchAll(/stream\r?\n([\s\S]*?)endstream/g)){try{raw=Buffer.concat([raw,zlib.inflateSync(Buffer.from(m[1],"latin1"))])}catch{}}
const all=raw.toString("latin1");for(const t of ["Geheimwort","86095742719","DE89","Mustermann","12.03.1980"])assert(!all.includes(t),"Rohsuche ohne „"+t+"“");
const txt=mupdf.Document.openDocument(out,"application/pdf").loadPage(0).toStructuredText().asText();assert(txt.includes("Diagnose: Befund unauffällig"),"ungeschwärzter Text bleibt extrahierbar");
