"""Public GW2 name catalog. Never reads credentials or account endpoints."""
import json
import random
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

BASE = 'https://api.guildwars2.com/'


def fetch(path):
    for attempt in range(3):
        try:
            with urlopen(BASE + path, timeout=45) as response:
                return json.load(response)
        except (HTTPError, URLError, TimeoutError) as error:
            if attempt == 2 or isinstance(error, HTTPError) and error.code not in (429,500,502,503,504):
                raise
            time.sleep(2 ** attempt)


def build_catalog(get=fetch):
    records = []
    coverage = {}
    for kind, endpoint in [('achievement', 'v2/achievements'), ('map', 'v2/maps'),
                           ('mastery', 'v2/masteries')]:
        try: ids = get(endpoint)
        except (HTTPError, URLError, TimeoutError) as error:
            coverage[kind] = {'error': str(error), 'returned': 0}
            continue
        rows = []
        for offset in range(0, len(ids), 200):
            try: rows.extend(get(endpoint + '?lang=en&ids=' + ','.join(map(str, ids[offset:offset+200]))))
            except (HTTPError, URLError, TimeoutError): continue
        found = {row['id'] for row in rows}
        coverage[kind] = {'requested': len(ids), 'returned': len(found),
                          'missing_ids': [i for i in ids if i not in found]}
        for row in rows:
            if not row.get('name'): continue
            record = {'kind': kind, 'id': row['id'], 'name': row['name'], 'source': BASE+endpoint}
            if kind == 'achievement': record['flags'] = row.get('flags', [])
            if kind == 'map': record['map_type'] = row.get('type', 'unknown')
            records.append(record)
            if kind == 'mastery':
                for index, level in enumerate(row.get('levels', [])):
                    if level.get('name'):
                        records.append({'kind': 'mastery_level', 'id': f"{row['id']}:{index}",
                                        'name': level['name'], 'track': row['name'], 'source': BASE+endpoint})
    event_source='v1/event_names.json'
    try: events = get(event_source+'?lang=en')
    except (HTTPError, URLError, TimeoutError) as error:
        event_source='v1/event_details.json'
        try:
            details=get(event_source+'?lang=en')['events']
            events=[dict(row,id=identifier) for identifier,row in details.items()]
        except (HTTPError, URLError, TimeoutError) as fallback_error:
            events=[]
            coverage['event_error']=str(fallback_error)
    records.extend({'kind': 'event', 'id': row['id'], 'name': row['name'],
                    'source': BASE+event_source} for row in events if row.get('name'))
    coverage['event'] = {'returned': len(events), 'note': 'Legacy API catalog; not a guarantee of every current event.'}
    if 'event_error' in coverage: coverage['event']['error']=coverage.pop('event_error')
    if not records: raise ValueError('No public catalog records could be downloaded')
    return {'version': 1, 'fetched_at': datetime.now(timezone.utc).isoformat(),
            'coverage': coverage, 'records': records}


def catalog_plans(catalog, seed):
    """Balance kinds and shuffle reproducibly, without putting the catalog in a prompt."""
    rng = random.Random(seed)
    groups = {}
    for row in catalog['records']:
        if row['kind'] == 'map' and row.get('map_type') != 'Public': continue
        groups.setdefault(row['kind'], []).append(row)
    for rows in groups.values(): rng.shuffle(rows)
    plans = []
    for index in range(max((len(rows) for rows in groups.values()), default=0)):
        for kind, rows in groups.items():
            if index >= len(rows): continue
            row = rows[index]
            task = {'achievement': 'Explain how to complete this achievement, including prerequisites and whether it is still available',
                    'event': 'Explain where this event happens, its prerequisites, and how to complete it; do not assume it is active now',
                    'map': 'First verify whether this is an open-world zone or an encounter instance. For a zone, explain all applicable map-completion objectives and access; for an instance, explain its encounter instead',
                    'mastery': 'Explain this mastery track, its unlock requirements, and how to progress it',
                    'mastery_level': 'Explain how to unlock this mastery level and what it does'}[kind]
            name = row['name'] + (' (track: '+row['track']+')' if row.get('track') else '')
            plans.append({'name': f"catalog {kind} {row['id']}", 'game': 'Guild Wars 2',
                          'goal': task, 'catalog_record': row,
                          'starter': f"I'm playing Guild Wars 2. {task}: {name}. Research the official wiki. Tell me if the name is ambiguous or the evidence is incomplete.",
                          'followups': ['Ask for the first concrete step.', 'Ask about solo access and prerequisites.',
                                        'Ask what can block progress without assuming account unlocks.']})
    return plans


def mix_plans(fixed, sampled):
    result = []
    for index, plan in enumerate(sampled):
        if index % 3 == 0 and fixed: result.append(fixed[(index//3) % len(fixed)])
        result.append(plan)
    return result or fixed
