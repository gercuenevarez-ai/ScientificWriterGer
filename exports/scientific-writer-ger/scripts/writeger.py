"""Run the original Spanish WriteGer model without recalibration."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT/'writeger'

def load(name):
    path=ASSETS/f'{name}.py'
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def validate(cfg, extractor):
    core=cfg['core_features'];g=cfg['global_spanish_model']
    if core != extractor.CORE_FEATURES:
        raise ValueError('Feature order does not match original extractor')
    for key in ['mean','sd']:
        v=np.array([g[key][f] for f in core],dtype=float)
        if not np.all(np.isfinite(v)) or (key=='sd' and np.any(v<=0)):
            raise ValueError(f'Invalid model {key}')
    cov=np.array(g['covariance_shrinkage'],dtype=float)
    precision=np.array(g['precision_shrinkage'],dtype=float)
    n=len(core)
    for matrix in [cov,precision]:
        if matrix.shape!=(n,n) or not np.all(np.isfinite(matrix)) or not np.allclose(matrix,matrix.T):
            raise ValueError('Invalid covariance/precision matrix')
        np.linalg.cholesky(matrix)
    if not np.allclose(cov@precision,np.eye(n),atol=1e-8):
        raise ValueError('Covariance and precision do not match')
    th=g['diagnostic_thresholds']
    limits=[th[k] for k in ['median_authentic_LOO','q75_authentic_LOO','q90_authentic_LOO','max_authentic_LOO']]
    if not all(np.isfinite(limits)) or limits!=sorted(limits) or limits[0]<0:
        raise ValueError('Invalid thresholds')
    for section in cfg['section_models'].values():
        for key in core:
            feature=section['features'][key]
            if not np.isfinite(feature['mean']) or not np.isfinite(feature['sd']) or feature['sd']<=0:
                raise ValueError('Invalid section parameters')

def run(path, language, section=None, pdf_reader="original") :
    if language!='es':
        raise ValueError('Original model is calibrated for Spanish; English D_WG is not available')
    extractor=load('WriteGer_Extractor_v2');auditor=load('WriteGer_Auditor_v2')
    cfg=json.loads((ASSETS/'WriteGer_Model_Parameters_Original_v2.json').read_text())
    validate(cfg,extractor)
    if section and section not in cfg['section_models']:
        raise ValueError('Unknown section: '+section)
    if path.suffix.lower()=='.pdf' and pdf_reader=='pypdf':
        from pypdf import PdfReader
        reader=PdfReader(path)
        text='\n\n'.join(page.extract_text() or '' for page in reader.pages)
    else:
        text=extractor.read_input(path)
    features=extractor.extract(text)
    other=auditor.extract(text)
    if any(not np.isclose(features[k],other[k],rtol=1e-12,atol=1e-12) for k in cfg['core_features']):
        raise ValueError('Original extractor and auditor disagree')
    result=auditor.audit(text,cfg,section)
    if not np.isfinite(result['D_WG']):
        raise ValueError('Non-finite distance')
    result['distance_model']='global_spanish_model'
    result['deviation_model']=section or 'global_spanish_model'
    result['language']='es'
    result['input_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    result['text_sha256']=hashlib.sha256(text.encode('utf-8')).hexdigest()
    result['pdf_reader']=pdf_reader if path.suffix.lower()=='.pdf' else None
    result['extraction_note']='pypdf changes PDF text extraction relative to original pdftotext; do not claim identical historical scores' if path.suffix.lower()=='.pdf' and pdf_reader=='pypdf' else 'Original extraction path'
    result['scientific_integrity_verified']=False
    result['provenance']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ASSETS.iterdir()) if p.suffix in ['.py','.json']}
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--language',required=True,choices=['es','en'],help='Declare the manuscript language; this is not automatic detection')
    parser.add_argument('--section',choices=['introduction','methods','results','discussion','results_discussion','conclusions'])
    parser.add_argument('--output',type=Path)
    parser.add_argument('--pdf-reader',choices=['original','pypdf'],default='original')
    args=parser.parse_args()
    try:
        result=run(args.input,args.language,args.section,args.pdf_reader)
        output=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
        if args.output:
            with args.output.open('x',encoding='utf-8') as file:file.write(output)
            print(f'Audit saved: {args.output}')
        else:print(output,end='')
    except (OSError,ValueError,KeyError,ImportError,np.linalg.LinAlgError) as exc:
        parser.exit(2,f'Error: {exc}\n')
