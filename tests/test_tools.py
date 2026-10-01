import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'scripts'/f'{name}.py')
    m = importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
workflow = module('workflow')
project = module('project')

class Tools(unittest.TestCase):
    def test_freeze_and_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory);source=p/'paper.md';source.write_text('n=30, p=0.05')
            review=p/'review';workflow.freeze(source,review)
            self.assertTrue(workflow.verify(review))
            with self.assertRaises(ValueError):workflow.freeze(source,review)
            (review/source.name).write_text('n=300, p=0.05')
            self.assertFalse(workflow.verify(review))
    def test_integrity(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory);a=p/'a.md';b=p/'b.md'
            a.write_text('n=30; p=0.05; efecto=−2.4')
            b.write_text('Efecto=−2.4; muestra n=30; p=0.05')
            self.assertTrue(workflow.integrity(a,b)['numeric_tokens_equal'])
            b.write_text('n=30; p=0.005; efecto=−2.4')
            self.assertFalse(workflow.integrity(a,b)['numeric_tokens_equal'])
    def test_docx_paragraphs(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'paper.docx'
            with zipfile.ZipFile(p,'w') as z:
                z.writestr('word/document.xml','<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>1</w:t></w:r></w:p><w:p><w:r><w:t>2</w:t></w:r></w:p></w:body></w:document>')
            self.assertEqual(workflow.read_text(p),'1\n2')
    def test_init_preserves_work(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory);project.initialize(p)
            (p/'project.json').write_text('{"name":"Real work"}')
            project.initialize(p)
            self.assertEqual((p/'project.json').read_text(),'{"name":"Real work"}')

if __name__ == '__main__':unittest.main()
