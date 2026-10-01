#!/usr/bin/env python3
import re, json, sys, subprocess
from pathlib import Path
from collections import Counter
import numpy as np

CONN_ES=['sin embargo','por lo tanto','por tanto','además','asimismo','mientras que','por su parte','de acuerdo con','en cuanto a','en lo que respecta','a su vez','por otro lado','no obstante','debido a','por esta razón','en consecuencia','finalmente','posteriormente','en este sentido','con respecto a','por consiguiente','en cambio','por otra parte','de esta manera','de este modo','así mismo','por ello','por lo cual','por ende']
SUB_ES=['que','aunque','porque','mientras','cuando','donde','si','como','debido a que','ya que','puesto que','para que','a pesar de que']
HEDGE_ES=['podría','podrían','puede','pueden','posiblemente','probablemente','sugiere','sugieren','parece','parecen','es posible','podría deberse','puede atribuirse']
FUNC_ES=['de','la','el','y','en','que','los','las','del','se','un','una','por','con','para','al','como','su','sus','entre','a','o','e','lo']
ABBR=["et al.","Fig.","Figs.","Dr.","Dra.","Sr.","Sra.","No.","Vol.","pp.","i.e.","e.g."]

def read_input(path):
    p=Path(path); ext=p.suffix.lower()
    if ext in (".txt",".md"): return p.read_text(encoding="utf-8",errors="ignore")
    if ext==".pdf":
        return subprocess.check_output(["pdftotext","-layout",str(p),"-"],text=True,stderr=subprocess.DEVNULL)
    if ext==".docx":
        from docx import Document
        d=Document(str(p)); return "\n\n".join(x.text for x in d.paragraphs if x.text.strip())
    raise ValueError("Supported: .txt .md .pdf .docx")

def tokens(t):
    return re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:-[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)?",t)

def normalize_body(t):
    lines=[]
    for ln in t.splitlines():
        s=ln.strip()
        if not s:
            lines.append(""); continue
        words=re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+",s)
        nums=re.findall(r"\d+(?:[.,]\d+)?",s)
        if len(nums)>=5 and len(words)<8: continue
        if re.search(r"\b(?:Table|Tabla|Figure|Figura)\s+\d+",s,re.I) and len(words)<15: continue
        lines.append(s)
    t="\n".join(lines)
    paras=[]
    for block in re.split(r"\n\s*\n+",t):
        block=re.sub(r"\s*\n\s*"," ",block)
        block=re.sub(r"\s+"," ",block).strip()
        if len(re.findall(r"\w+",block))>=25: paras.append(block)
    return " ".join(paras),paras

def split_sentences(t):
    temp=t; repl={}
    for i,a in enumerate(ABBR):
        key=f"ABBR{i}X"; temp=temp.replace(a,key); repl[key]=a
    s=re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ])',temp)
    out=[]
    for x in s:
        for k,a in repl.items(): x=x.replace(k,a)
        n=len(tokens(x))
        if 5<=n<=100: out.append(x.strip())
    return out

def mattr(tok,win=100):
    tok=[x.lower() for x in tok]
    if len(tok)<20:return float("nan")
    if len(tok)<win:return len(set(tok))/len(tok)
    return float(np.mean([len(set(tok[i:i+win]))/win for i in range(0,len(tok)-win+1,20)]))

def count_phrases(low,phrases):
    return sum(len(re.findall(r"\b"+re.escape(p)+r"\b",low)) for p in phrases)

def extract(text):
    flat,paras=normalize_body(text); ss=split_sentences(flat); tok=tokens(flat); low=flat.lower(); N=len(tok)
    if N<100 or len(ss)<5: raise ValueError("Use at least ~100 words and >=5 sentences.")
    lens=np.array([len(tokens(s)) for s in ss],dtype=float)
    pwords=np.array([len(tokens(p)) for p in paras],dtype=float)
    c=Counter(x.lower() for x in tok)
    noms=sum(1 for x in tok if re.search(r"(ción|ciones|sión|siones|miento|mientos|dad|dades|encia|encias|anza|anzas)$",x.lower()))
    imp=sum(len(re.findall(r"\bse\s+\w+(?:ó|aron|ió|ieron|a|an|e|en)\b",s.lower())) for s in ss)
    return {
      "mean_wps":float(np.mean(lens)),
      "cv_wps_pct":float(100*np.std(lens,ddof=1)/np.mean(lens)),
      "mattr100":mattr(tok,100),
      "connectors_per_1000":1000*count_phrases(low,CONN_ES)/N,
      "subordination_markers_per_1000":1000*sum(c[p] if " " not in p else len(re.findall(r"\b"+re.escape(p)+r"\b",low)) for p in SUB_ES)/N,
      "nominalizations_per_1000":1000*noms/N,
      "passive_impersonal_per_1000":1000*imp/N,
      "functional_words_per_1000":1000*sum(c[w] for w in FUNC_ES)/N,
      "commas_per_1000":1000*flat.count(",")/N,
      "mean_words_per_para":float(np.mean(pwords)) if len(pwords) else float(N),
      "_words":N,"_sentences":len(ss),"_paragraphs":len(paras)
    }

def audit(text,cfg,section=None):
    f=extract(text); core=cfg["core_features"]; g=cfg["global_spanish_model"]
    x=np.array([f[k] for k in core]); mu=np.array([g["mean"][k] for k in core]); sd=np.array([g["sd"][k] for k in core])
    z=(x-mu)/sd; P=np.array(g["precision_shrinkage"]); D=float(np.sqrt(z@P@z))
    if section and section in cfg["section_models"]:
        sm=cfg["section_models"][section]["features"]
        dz={k:(f[k]-sm[k]["mean"])/sm[k]["sd"] for k in core}
    else: dz={k:float(v) for k,v in zip(core,z)}
    dev=sorted(dz.items(),key=lambda kv:abs(kv[1]),reverse=True)
    th=g["diagnostic_thresholds"]
    if D<=th["q75_authentic_LOO"]: band="núcleo compatible"
    elif D<=th["q90_authentic_LOO"]: band="periferia compatible"
    elif D<=th["max_authentic_LOO"]: band="atípico, pero dentro del rango auténtico observado"
    else: band="fuera del rango auténtico leave-one-out actual"
    return {"D_WG":D,"band":band,"section":section or "global",
            "counts":{"words":f["_words"],"sentences":f["_sentences"],"paragraphs":f["_paragraphs"]},
            "features":{k:f[k] for k in core},
            "largest_deviations":[{"feature":k,"z":float(v)} for k,v in dev[:5]],
            "thresholds":th,
            "interpretation":"Compatibility with the current WriteGer corpus; not an AI or authorship probability."}

if __name__=="__main__":
    if len(sys.argv)<3:
        print("Usage: python WriteGer_Auditor_v2.py WriteGer_v2_config.json text.(txt|md|pdf|docx) [section]")
        sys.exit(2)
    cfg=json.load(open(sys.argv[1],encoding="utf-8"))
    print(json.dumps(audit(read_input(sys.argv[2]),cfg,sys.argv[3] if len(sys.argv)>3 else None),ensure_ascii=False,indent=2))
