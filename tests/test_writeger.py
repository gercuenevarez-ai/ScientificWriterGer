from pathlib import Path
import importlib.util
import json
import tempfile
import unittest
import numpy as np
from docx import Document

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('wg',ROOT/'scripts/writeger.py')
wg=importlib.util.module_from_spec(spec);spec.loader.exec_module(wg)
TEXT=('Se analizaron los registros correspondientes a las unidades experimentales, considerando los criterios de selección que se habían establecido para la investigación. '
'Las observaciones fueron revisadas antes del análisis para que las diferencias entre tratamientos pudieran interpretarse dentro del diseño declarado. '
'Sin embargo, se conservaron los datos originales y se documentaron las transformaciones necesarias para evaluar la distribución de las variables observadas. '
'Por lo tanto, las conclusiones se limitaron a las condiciones del estudio, sin atribuir mecanismos causales que no estuvieran respaldados por la evidencia disponible. '
'Además, la comparación con la literatura permitió identificar semejanzas y diferencias que debían considerarse al explicar el alcance de las estimaciones obtenidas. ')

class WriteGer(unittest.TestCase):
 def test_parameters_and_parity(self):
  cfg=json.loads((ROOT/'writeger/WriteGer_Model_Parameters_Original_v2.json').read_text())
  e=wg.load('WriteGer_Extractor_v2');a=wg.load('WriteGer_Auditor_v2');wg.validate(cfg,e)
  self.assertEqual(e.extract(TEXT),a.extract(TEXT))
  with tempfile.TemporaryDirectory() as directory:
   p=Path(directory)/'text.txt';p.write_text(TEXT)
   result=wg.run(p,'es');section=wg.run(p,'es','discussion')
   self.assertEqual(result['D_WG'],section['D_WG'])
   g=cfg['global_spanish_model'];z=np.array([(result['features'][k]-g['mean'][k])/g['sd'][k] for k in cfg['core_features']])
   expected=np.sqrt(z@np.linalg.solve(np.array(g['covariance_shrinkage']),z))
   self.assertAlmostEqual(result['D_WG'],expected)
   with self.assertRaises(ValueError):wg.run(p,'en')
   with self.assertRaises(ValueError):wg.run(p,'es','unknown')
   doc=Document();doc.add_paragraph(TEXT);q=Path(directory)/'text.docx';doc.save(q)
   self.assertAlmostEqual(result['D_WG'],wg.run(q,'es')['D_WG'])
 def test_short_text(self):
  with self.assertRaises(ValueError):wg.load('WriteGer_Extractor_v2').extract('Texto corto.')
 def test_bad_parameters(self):
  cfg=json.loads((ROOT/'writeger/WriteGer_Model_Parameters_Original_v2.json').read_text())
  cfg['global_spanish_model']['sd']['mean_wps']=0
  with self.assertRaises(ValueError):wg.validate(cfg,wg.load('WriteGer_Extractor_v2'))

if __name__=='__main__':unittest.main()
