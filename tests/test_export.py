import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('swg_export',ROOT/'scripts/export.py')
export=importlib.util.module_from_spec(spec);spec.loader.exec_module(export)

class Export(unittest.TestCase):
 def test_self_contained_bundle(self):
  with tempfile.TemporaryDirectory() as directory:
   folder=export.build(directory)
   for name in ['gpt','claude','grok','gemini']:
    self.assertTrue((folder/name/'INSTRUCTIONS.txt').is_file())
   with zipfile.ZipFile(folder/'scientific-writer-ger.zip') as z:
    self.assertIsNone(z.testzip())
    self.assertIn('scientific-writer-ger/SKILL.md',z.namelist())
    self.assertIn('scientific-writer-ger/scripts/writeger.py',z.namelist())
    self.assertIn('scientific-writer-ger/writeger/WriteGer_Model_Parameters_Original_v2.json',z.namelist())
    self.assertFalse(any('/.git/' in name for name in z.namelist()))
   self.assertEqual((folder/'scientific-writer-ger/references/knowledge.txt').read_text(),(folder/'ScientificWriterGer-Knowledge.txt').read_text())
 def test_install_preserves_destination(self):
  with tempfile.TemporaryDirectory() as directory:
   result=subprocess.run([sys.executable,str(ROOT/'scripts/install.py'),directory],capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stderr)
   target=Path(directory)/'scientific-writer-ger'
   self.assertTrue((target/'SKILL.md').is_file())
   data=(target/'SKILL.md').read_bytes()
   result=subprocess.run([sys.executable,str(ROOT/'scripts/install.py'),directory],capture_output=True,text=True)
   self.assertEqual(result.returncode,2)
   self.assertEqual((target/'SKILL.md').read_bytes(),data)

if __name__=='__main__':unittest.main()
