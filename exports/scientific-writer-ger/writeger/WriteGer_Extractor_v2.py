#!/usr/bin/env python3
# WriteGer v2 — Extractor estilométrico autónomo
# Extrae exactamente las 10 variables operativas usadas por el modelo WriteGer v2.

import re
import sys
import json
import subprocess
from pathlib import Path
from collections import Counter
import numpy as np

CONN_ES = [
    'sin embargo','por lo tanto','por tanto','además','asimismo','mientras que',
    'por su parte','de acuerdo con','en cuanto a','en lo que respecta','a su vez',
    'por otro lado','no obstante','debido a','por esta razón','en consecuencia',
    'finalmente','posteriormente','en este sentido','con respecto a',
    'por consiguiente','en cambio','por otra parte','de esta manera','de este modo',
    'así mismo','por ello','por lo cual','por ende'
]

SUB_ES = [
    'que','aunque','porque','mientras','cuando','donde','si','como',
    'debido a que','ya que','puesto que','para que','a pesar de que'
]

FUNC_ES = [
    'de','la','el','y','en','que','los','las','del','se','un','una','por',
    'con','para','al','como','su','sus','entre','a','o','e','lo'
]

ABBR = [
    "et al.","Fig.","Figs.","Dr.","Dra.","Sr.","Sra.","No.","Vol.","pp.","i.e.","e.g."
]

CORE_FEATURES = [
    "mean_wps",
    "cv_wps_pct",
    "mattr100",
    "connectors_per_1000",
    "subordination_markers_per_1000",
    "nominalizations_per_1000",
    "passive_impersonal_per_1000",
    "functional_words_per_1000",
    "commas_per_1000",
    "mean_words_per_para"
]

def read_input(path):
    p = Path(path)
    ext = p.suffix.lower()
    if ext in (".txt", ".md"):
        return p.read_text(encoding="utf-8", errors="ignore")
    if ext == ".pdf":
        return subprocess.check_output(
            ["pdftotext", "-layout", str(p), "-"],
            text=True, stderr=subprocess.DEVNULL
        )
    if ext == ".docx":
        from docx import Document
        d = Document(str(p))
        return "\n\n".join(x.text for x in d.paragraphs if x.text.strip())
    raise ValueError("Formatos soportados: .txt .md .pdf .docx")

def tokens(t):
    return re.findall(
        r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:-[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)?", t
    )

def normalize_body(t):
    lines = []
    for ln in t.splitlines():
        s = ln.strip()
        if not s:
            lines.append("")
            continue
        words = re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", s)
        nums = re.findall(r"\d+(?:[.,]\d+)?", s)
        if len(nums) >= 5 and len(words) < 8:
            continue
        if re.search(r"\b(?:Table|Tabla|Figure|Figura)\s+\d+", s, re.I) and len(words) < 15:
            continue
        lines.append(s)

    t = "\n".join(lines)
    paras = []
    for block in re.split(r"\n\s*\n+", t):
        block = re.sub(r"\s*\n\s*", " ", block)
        block = re.sub(r"\s+", " ", block).strip()
        if len(re.findall(r"\w+", block)) >= 25:
            paras.append(block)

    return " ".join(paras), paras

def split_sentences(t):
    temp = t
    repl = {}
    for i, a in enumerate(ABBR):
        key = f"ABBR{i}X"
        temp = temp.replace(a, key)
        repl[key] = a

    s = re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ])', temp)
    out = []
    for x in s:
        for k, a in repl.items():
            x = x.replace(k, a)
        n = len(tokens(x))
        if 5 <= n <= 100:
            out.append(x.strip())
    return out

def mattr(tok, win=100):
    tok = [x.lower() for x in tok]
    if len(tok) < 20:
        return float("nan")
    if len(tok) < win:
        return len(set(tok)) / len(tok)
    return float(np.mean([
        len(set(tok[i:i+win])) / win
        for i in range(0, len(tok)-win+1, 20)
    ]))

def count_phrases(low, phrases):
    return sum(
        len(re.findall(r"\b" + re.escape(p) + r"\b", low))
        for p in phrases
    )

def extract(text):
    flat, paras = normalize_body(text)
    ss = split_sentences(flat)
    tok = tokens(flat)
    low = flat.lower()
    N = len(tok)

    if N < 100 or len(ss) < 5:
        raise ValueError("Use al menos ~100 palabras y >=5 oraciones.")

    lens = np.array([len(tokens(s)) for s in ss], dtype=float)
    pwords = np.array([len(tokens(p)) for p in paras], dtype=float)
    c = Counter(x.lower() for x in tok)

    noms = sum(
        1 for x in tok
        if re.search(
            r"(ción|ciones|sión|siones|miento|mientos|dad|dades|encia|encias|anza|anzas)$",
            x.lower()
        )
    )

    imp = sum(
        len(re.findall(r"\bse\s+\w+(?:ó|aron|ió|ieron|a|an|e|en)\b", s.lower()))
        for s in ss
    )

    return {
        "mean_wps": float(np.mean(lens)),
        "cv_wps_pct": float(100*np.std(lens, ddof=1)/np.mean(lens)),
        "mattr100": mattr(tok, 100),
        "connectors_per_1000": 1000*count_phrases(low, CONN_ES)/N,
        "subordination_markers_per_1000": 1000*sum(
            c[p] if " " not in p else len(re.findall(r"\b"+re.escape(p)+r"\b", low))
            for p in SUB_ES
        )/N,
        "nominalizations_per_1000": 1000*noms/N,
        "passive_impersonal_per_1000": 1000*imp/N,
        "functional_words_per_1000": 1000*sum(c[w] for w in FUNC_ES)/N,
        "commas_per_1000": 1000*flat.count(",")/N,
        "mean_words_per_para": float(np.mean(pwords)) if len(pwords) else float(N),
        "_words": N,
        "_sentences": len(ss),
        "_paragraphs": len(paras)
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python WriteGer_Extractor_v2.py archivo.(txt|md|pdf|docx)")
        sys.exit(2)

    result = extract(read_input(sys.argv[1]))
    print(json.dumps(result, ensure_ascii=False, indent=2))
