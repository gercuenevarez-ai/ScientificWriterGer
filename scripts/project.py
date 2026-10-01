"""Local project scaffolding and structural checks; no external verification."""
import argparse
import json
from pathlib import Path
import sys

DEFAULT = {'name': '', 'discipline': 'multidisciplinary', 'language': 'es',
           'deliverable': 'paper', 'study_type': '', 'question': '',
           'requirements': []}

def initialize(root):
    root.mkdir(parents=True, exist_ok=True)
    for name, value in [('project.json', DEFAULT), ('sources.json', []), ('claims.json', [])]:
        path = root / name
        try:
            with path.open('x', encoding='utf-8') as file:
                json.dump(value, file, ensure_ascii=False, indent=2)
                file.write('\n')
            print(f'Created: {path}')
        except FileExistsError:
            print(f'Preserved: {path}')

def check(root):
    errors = []
    values = {}
    for name, expected in [('project.json', dict), ('sources.json', list), ('claims.json', list)]:
        try:
            value = json.loads((root / name).read_text(encoding='utf-8'))
            if not isinstance(value, expected):
                errors.append(f'{name}: expected {expected.__name__}')
            else:
                values[name] = value
        except (OSError, ValueError) as exc:
            errors.append(f'{name}: {exc}')
    project = values.get('project.json', {})
    for field in ['name', 'discipline', 'language', 'deliverable', 'study_type', 'question']:
        if not isinstance(project.get(field), str) or not project[field].strip():
            errors.append(f'project.json: missing text {field}')
    if project.get('deliverable') not in ['paper', 'thesis', 'proposal', 'review']:
        errors.append('project.json: invalid deliverable')
    if not isinstance(project.get('requirements'), list):
        errors.append('project.json: requirements must be a list')
    ids = {}
    for filename in ['sources.json', 'claims.json']:
        seen = set()
        for i, row in enumerate(values.get(filename, [])):
            label = f'{filename}[{i}]'
            if not isinstance(row, dict):
                errors.append(f'{label}: expected object')
                continue
            ident = row.get('id')
            if not isinstance(ident, str) or not ident.strip():
                errors.append(f'{label}: missing id')
            elif ident in seen:
                errors.append(f'{label}: duplicate id {ident}')
            else:
                seen.add(ident)
            fields = ['title', 'locator', 'verification_note'] if filename == 'sources.json' else ['text', 'evidence_note']
            for field in fields:
                if not isinstance(row.get(field), str) or not row[field].strip():
                    errors.append(f'{label}: missing text {field}')
            if filename == 'sources.json':
                if row.get('access') not in ['metadata', 'abstract', 'fulltext']:
                    errors.append(f'{label}: invalid access')
                if not isinstance(row.get('authors'), list) or not row['authors']:
                    errors.append(f'{label}: missing authors list')
                if not isinstance(row.get('year'), int) or isinstance(row.get('year'), bool):
                    errors.append(f'{label}: year must be an integer')
            else:
                if row.get('kind') not in ['literature', 'result', 'interpretation', 'proposal']:
                    errors.append(f'{label}: invalid kind')
                if row.get('status') not in ['pending', 'supported', 'disputed', 'unsupported']:
                    errors.append(f'{label}: invalid status')
                links = row.get('source_ids')
                if not isinstance(links, list) or any(not isinstance(x, str) for x in links):
                    errors.append(f'{label}: source_ids must be a list of strings')
                else:
                    for link in links:
                        if link not in ids.get('sources.json', set()):
                            errors.append(f'{label}: unknown source {link}')
                    if row.get('kind') == 'literature' and row.get('status') == 'supported' and not links:
                        errors.append(f'{label}: supported literature claim needs sources')
                if row.get('status') != 'supported':
                    print(f'Pending review: {label} ({row.get("status")})')
        ids[filename] = seen
    for error in errors:
        print(f'ERROR: {error}')
    print('Structural checks only; source truth and scientific validity are not verified.')
    return 1 if errors else 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['init', 'check'])
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    if args.action == 'init':
        initialize(args.directory)
    else:
        sys.exit(check(args.directory))
