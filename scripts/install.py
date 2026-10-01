"""Install a self-contained ScientificWriterGer skill without overwriting work."""
import argparse
import importlib.util
from pathlib import Path
import shutil
import tempfile

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('destination',type=Path,help='Skills directory used by your agent')
args=parser.parse_args()
target=args.destination/'scientific-writer-ger'
if target.exists():parser.exit(2,f'Existing destination preserved: {target}\n')
spec=importlib.util.spec_from_file_location('swg_export',ROOT/'scripts/export.py')
export=importlib.util.module_from_spec(spec);spec.loader.exec_module(export)
with tempfile.TemporaryDirectory() as temporary:
    export.build(temporary)
    shutil.copytree(Path(temporary)/'scientific-writer-ger',target)
print(f'Installed self-contained skill: {target}')
