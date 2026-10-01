"""Freeze review inputs and flag numerical edits; no external calls."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from xml.etree import ElementTree


def read_text(path):
    if path.suffix.lower() == '.docx':
        with zipfile.ZipFile(path) as archive:
            parts = [n for n in archive.namelist() if n == 'word/document.xml' or re.fullmatch(r'word/(footnotes|endnotes|header\d+|footer\d+)\.xml', n)]
            texts = []
            for part in sorted(parts):
                root = ElementTree.fromstring(archive.read(part))
                ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
                texts.extend(''.join(t.text or '' for t in p.iter(ns+'t')) for p in root.iter(ns+'p'))
            return '\n'.join(texts)
    if path.suffix.lower() not in {'.txt', '.md', '.tex'}:
        raise ValueError('Use TXT, MD, TEX or DOCX; PDF requires prior text extraction.')
    return path.read_text(encoding='utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def freeze(source, directory):
    data = source.read_bytes()
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / source.name
    manifest = directory / 'review-manifest.json'
    if target.exists() or manifest.exists():
        raise ValueError('Review destination already contains this snapshot; choose a new directory.')
    record = {'manuscript': source.name, 'sha256': digest(data), 'bytes': len(data), 'reviewers': ['Gemini', 'Claude'], 'sent': False}
    with target.open('xb') as stream:
        stream.write(data)
    with manifest.open('x', encoding='utf-8') as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
    return record


def verify(directory):
    record = json.loads((directory/'review-manifest.json').read_text())
    name = record['manuscript']
    if Path(name).name != name:
        raise ValueError('Invalid manuscript path in manifest')
    return digest((directory/name).read_bytes()) == record['sha256']


def integrity(before, after):
    pattern = r'(?<!\w)[−+\-]?\d+(?:[.,]\d+)*(?:[eE][+\-]?\d+)?%?'
    a = Counter(re.findall(pattern, read_text(before)))
    b = Counter(re.findall(pattern, read_text(after)))
    return {'removed': dict(a-b), 'added': dict(b-a), 'numeric_tokens_equal': a == b,
            'scope': 'Numeric token multiset only; units, citations, semantics and placement require review.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    cmd = sub.add_parser('freeze');cmd.add_argument('manuscript', type=Path);cmd.add_argument('directory', type=Path)
    cmd = sub.add_parser('verify');cmd.add_argument('directory', type=Path)
    cmd = sub.add_parser('integrity');cmd.add_argument('before', type=Path);cmd.add_argument('after', type=Path)
    args = parser.parse_args()
    try:
        if args.action == 'freeze':
            print(json.dumps(freeze(args.manuscript, args.directory), indent=2))
        elif args.action == 'verify':
            ok = verify(args.directory);print('MATCH' if ok else 'CHANGED');sys.exit(0 if ok else 1)
        else:
            result = integrity(args.before, args.after);print(json.dumps(result, indent=2));sys.exit(0 if result['numeric_tokens_equal'] else 1)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, ElementTree.ParseError) as exc:
        parser.exit(2, f'Error: {exc}\n')
