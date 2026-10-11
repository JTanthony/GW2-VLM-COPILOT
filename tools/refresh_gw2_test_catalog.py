"""Refresh the public name pool without starting models or connecting an account."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from waypoint.testing.catalog import build_catalog,fetch

if __name__ == '__main__':
    target = ROOT/'local-data/test-catalog/gw2-public.json'
    try:
        def progress(path):
            print('Fetching '+path.split('?')[0],flush=True)
            return fetch(path)
        catalog = build_catalog(progress)
        if target.exists() and any(v.get('error') or v.get('missing_ids') for v in catalog['coverage'].values() if isinstance(v,dict)):
            raise ValueError('Refresh was incomplete; retaining the existing catalog')
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix('.tmp')
        temporary.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding='utf-8')
        temporary.replace(target)
        print(json.dumps({'path': str(target), 'records': len(catalog['records']), 'coverage': catalog['coverage']}, indent=2))
    except Exception as error:
        print(f'Catalog refresh failed; existing catalog preserved: {error}', file=sys.stderr)
        sys.exit(1)
