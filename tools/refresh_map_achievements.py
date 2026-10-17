"""Refresh the public dedicated-map category reference; no account access."""
import json,ssl,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from waypoint.assistant.web_lookup import PinnedHTTPS

GROUPS={'Heart of Thorns','Path of Fire','End of Dragons','Secrets of the Obscure','Janthir Wilds','Visions of Eternity'}
# Deliberate exceptions, not fuzzy matches to story titles or encounters.
GENERAL_MAPS={'Dry Top','The Silverwastes'}
EXCLUDED_MAP_CATEGORIES={'Convergence: Nexus of Eternity'}
SECTION_CATEGORIES={403:1526,409:1526,416:1526}
PREFERRED_MAPS={'Verdant Brink':1052}
SEASON_ONE={328:'Flame and Frost',329:'Sky Pirates',43:'Clockwork Chaos',44:"Emissary Vorpp's Field Assistant",
            53:'Tower of Nightmares',54:'The Nightmares Within',56:'The Nightmare Is Over',
            62:"Escape from Lion's Arch",65:"The Battle for Lion's Arch"}

def fetch(endpoint):
    if not endpoint.startswith(('/v2/achievements/groups?ids=', '/v2/achievements/categories?ids=', '/v2/achievements?ids=', '/v2/maps?ids=')):
        raise ValueError('Unsupported public endpoint.')
    connection=PinnedHTTPS('api.guildwars2.com',timeout=30,context=ssl.create_default_context())
    try:
        connection.request('GET',endpoint+'&lang=en&v=2024-07-20T01:00:00.000Z',headers={'Accept':'application/json','User-Agent':'GW2-VLM-COPILOT public reference refresh'})
        response=connection.getresponse()
        if response.status!=200: raise ValueError('Public reference returned HTTP '+str(response.status))
        if 'application/json' not in response.getheader('Content-Type','').lower(): raise ValueError('Expected JSON.')
        raw=response.read(2_000_001)
        if len(raw)>2_000_000: raise ValueError('Public reference too large.')
        result=json.loads(raw)
        if not isinstance(result,list): raise ValueError('Expected public record list.')
        return result
    finally: connection.close()

def batches(endpoint,ids):
    rows=[]
    for offset in range(0,len(ids),200): rows.extend(fetch(endpoint+','.join(map(str,ids[offset:offset+200]))))
    return rows

def select_maps(groups,categories,maps):
    selected={}
    for category in categories:
        parents=[g for g in groups if category['id'] in g['categories']]
        parents=[g for g in parents if g['name'] in GROUPS or (g['name']=='General' and category['name'] in GENERAL_MAPS)]
        if len(parents)!=1 or category['name'] in EXCLUDED_MAP_CATEGORIES: continue
        section_map=SECTION_CATEGORIES.get(category['id'])
        candidates=[m for m in maps if m.get('type')=='Public' and
                    (m['id']==section_map if section_map else m['name']==category['name'])]
        if not candidates: continue
        preferred=PREFERRED_MAPS.get(category['name'])
        if preferred: candidates=[m for m in candidates if m['id']==preferred]
        if len(candidates)!=1: raise ValueError('Ambiguous map identity: '+category['name'])
        map_record=candidates[0]; key=map_record['id']; group=parents[0]
        row=selected.setdefault(key,{'expansion':group['name'] if group['name']!='General' else 'Core Tyria / Living World Season 2',
            'group_id':group['id'],'map_id':key,'map_name':map_record['name'],'categories':[]})
        if row['group_id']!=group['id']: raise ValueError('Conflicting map groups.')
        row['categories'].append(category)
    return sorted(selected.values(),key=lambda r:(r['expansion'],r['map_name']))

def build():
    groups=fetch('/v2/achievements/groups?ids=all')
    ids=sorted({value for group in groups for value in group['categories']})
    categories=batches('/v2/achievements/categories?ids=',ids)
    maps=fetch('/v2/maps?ids=all')
    selected=select_maps(groups,categories,maps)
    if not selected: raise ValueError('No map categories found.')
    story_groups=[g for g in groups if g['name']=='Story Journal']
    if len(story_groups)!=1: raise ValueError('Missing Story Journal group.')
    episode_categories=[]
    for category_id,name in SEASON_ONE.items():
        matches=[c for c in categories if c['id']==category_id and c['name']==name and c['id'] in story_groups[0]['categories']]
        if len(matches)!=1: raise ValueError('Missing Season 1 category: '+name)
        episode_categories.append(matches[0])
    all_ids=sorted({entry['id'] if isinstance(entry,dict) else entry
                   for category in [c for row in selected for c in row['categories']]+episode_categories for entry in category['achievements']})
    records=batches('/v2/achievements?ids=',all_ids)
    if {r['id'] for r in records}!=set(all_ids): raise ValueError('Incomplete achievement details.')
    details={r['id']:r for r in records}
    output={'schema_version':1,'verified_at':datetime.now(timezone.utc).isoformat(),
            'scope':'Dedicated open-world map categories and separately labeled Season 1 episode categories; not every achievement obtainable on each map.',
            'source':'https://api.guildwars2.com/v2/achievements/groups?ids=all','maps':[]}
    for row in selected:
        category_rows=[]; members=set()
        for category in sorted(row.pop('categories'),key=lambda c:c['id']):
            ids=[entry['id'] if isinstance(entry,dict) else entry for entry in category['achievements']]
            if not ids or any(type(value) is not int for value in ids) or len(set(ids))!=len(ids): raise ValueError('Invalid category IDs.')
            members.update(ids)
            category_rows.append({'id':category['id'],'name':category['name'],'achievement_ids':ids,
                'source':'https://api.guildwars2.com/v2/achievements/categories/'+str(category['id']),
                'wiki_source':'https://wiki.guildwars2.com/wiki/'+category['name'].replace(' ','_')+'_(achievements)'})
        row.update({'category_id':category_rows[0]['id'] if len(category_rows)==1 else None,
            'category_name':category_rows[0]['name'] if len(category_rows)==1 else row['map_name']+' dedicated sections',
            'categories':category_rows,
            'achievements':[{'id':value,'name':details[value]['name'],'flags':details[value].get('flags',[]),
                             'prerequisites':details[value].get('prerequisites',[])} for value in sorted(members)]})
        output['maps'].append(row)
    output['episode_categories']=[]
    for category in episode_categories:
        ids=[entry['id'] if isinstance(entry,dict) else entry for entry in category['achievements']]
        if not ids or any(type(value) is not int for value in ids) or len(set(ids))!=len(ids): raise ValueError('Invalid Season 1 IDs.')
        output['episode_categories'].append({'season':'Living World Season 1','scope':'episode/story category, not a map total',
            'category_id':category['id'],'category_name':category['name'],
            'category_source':'https://api.guildwars2.com/v2/achievements/categories/'+str(category['id']),
            'achievements':[{'id':value,'name':details[value]['name'],'flags':details[value].get('flags',[]),
                             'prerequisites':details[value].get('prerequisites',[])} for value in sorted(ids)]})
    supported={r['map_id'] for r in selected}
    output['unmapped_public_maps']=[{'map_id':m['id'],'map_name':m['name'],
        'reason':'No dedicated category matched within scope; mixed story, regional, activity and collection groups are excluded.'}
        for m in maps if m.get('type')=='Public' and m['id'] not in supported]
    return output

def render_document(data):
    lines=['# Dedicated map achievement reference','', 'Verified: '+data['verified_at'],'',
        'Public API membership across dedicated open-world map categories, including expansion maps and hubs. Not every map has its own category; this is not every achievement obtainable in an area. No account data is included.','',
        'Groups are matched to exact official map names and Public map types. General includes only Dry Top and The Silverwastes. Historical, story, collection, regional, raid, PvP, WvW and convergence groups are excluded from map totals. Living World Season 1 Story Journal categories are included separately as an explicitly scoped exception. Inner Nayos combines its three dedicated section categories, deduplicating achievement IDs; section membership remains available separately. Verdant Brink uses map ID 1052 because the API also exposes a second Public map with the same name.','',
        'Every category membership and achievement detail is verified against the public official API. Wiki headline totals may differ; totals below deliberately use API IDs. Per-achievement flags and prerequisite IDs are retained, but membership does not establish current availability or player eligibility. Entries remain in their official category even if an objective refers to another map.','',
        '| Group | Map | Map ID | Category IDs | Entries |','|---|---|---:|---|---:|']
    for row in data['maps']:
        lines.append('| '+row['expansion']+' | '+row['map_name']+' | '+str(row['map_id'])+' | '+', '.join(str(c['id']) for c in row['categories'])+' | '+str(len(row['achievements']))+' |')
    lines+=['','## Refresh and calculation','',
        'Machine-readable data: `data/gw2/map_achievements.json`. Refresh manually with `python tools/refresh_map_achievements.py`. This replaces the JSON and this document only after verifying public records. No account calls or credentials are used. The Windows builder includes only this curated public reference.','',
        '`category_progress` matches unique achievement IDs against a dated account snapshot. Only `done=true` confirms completion; matching current/max or absent records do not. Unknown maps and missing snapshots yield no result, not 0/0. The automatic vision message is not enabled.','',
        '## Coverage gaps','',
        'Other API Public maps are listed in the JSON under `unmapped_public_maps`. They include core zones, Living World maps with combined story/map categories, activities, lounges and duplicate map variants. Their exclusion means no dedicated match within our rules, not no achievements. Mixed groups can be added in a later explicitly broader scope.','']
    for row in data['maps']:
        lines+=['## '+row['map_name'],'']
        for category in row['categories']:
            lines.append('[Official category: '+category['name']+']('+category['source']+') / [Wiki]('+category['wiki_source']+')')
        lines+=['','| Achievement ID | Name | Flags | Prerequisite IDs |','|---:|---|---|---|']
        for achievement in row['achievements']:
            lines.append('| '+str(achievement['id'])+' | '+achievement['name'].replace('|','\\|')+' | '+', '.join(achievement['flags'])+' | '+', '.join(map(str,achievement['prerequisites']))+' |')
        lines.append('')
    lines+=['## Living World Season 1 — separate episode categories','',
        'These nine Story Journal categories are not map totals and never enter automatic map counts. They include side categories alongside the five rereleased main episodes. Category membership does not prove every legacy entry is currently obtainable; original and rereleased achievements may coexist. Festivals and historical-group categories are excluded.','',
        '| Category | API ID | Entries |','|---|---:|---:|']
    for row in data.get('episode_categories',[]):
        lines.append('| '+row['category_name']+' | '+str(row['category_id'])+' | '+str(len(row['achievements']))+' |')
    for row in data.get('episode_categories',[]):
        lines+=['','### '+row['category_name'],'','[Official category]('+row['category_source']+')','',
                '| Achievement ID | Name | Flags | Prerequisite IDs |','|---:|---|---|---|']
        for achievement in row['achievements']:
            lines.append('| '+str(achievement['id'])+' | '+achievement['name'].replace('|','\\|')+' | '+', '.join(achievement['flags'])+' | '+', '.join(map(str,achievement['prerequisites']))+' |')
    return '\n'.join(lines)+'\n'

def main():
    data=build()
    document=render_document(data)
    target=ROOT/'data/gw2/map_achievements.json';target.parent.mkdir(parents=True,exist_ok=True)
    temporary=target.with_suffix('.tmp');temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temporary.replace(target)
    (ROOT/'docs/MAP_ACHIEVEMENTS.md').write_text(document,encoding='utf-8')
    print(json.dumps({'maps':len(data['maps']),'categories':sum(len(r['categories']) for r in data['maps']),
                     'achievement_memberships':sum(len(m['achievements']) for m in data['maps']),
                     'unique_achievements':len({a['id'] for m in data['maps'] for a in m['achievements']})}))
    print('Season 1 categories:',len(data['episode_categories']))
    for row in data['episode_categories']: print(row['category_name'],len(row['achievements']))

if __name__=='__main__': main()
