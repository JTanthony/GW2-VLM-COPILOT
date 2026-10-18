"""Exact green-tracker title recognition; never claims instance entry."""
import json,re
from functools import lru_cache
from waypoint.paths import app_root

def normalized(value):
    return ' '.join(re.findall(r'\w+',value.casefold()))

@lru_cache(maxsize=1)
def load_story_table():
    data=json.loads((app_root()/'data/gw2/story_achievements.json').read_text('utf-8'))
    if data.get('schema_version')!=1: raise ValueError('Unsupported story reference.')
    return data

def selected_story(observation,snapshot=None,table=None):
    if not observation: return None
    if table is None:
        try: table=load_story_table()
        except (OSError,ValueError): return None
    labels=[]
    for value in observation.get('visible_text',[]):
        match=re.fullmatch(r'(?:Story chapter|Story episode):\s*(.+)',value,re.I)
        if match: labels.append(normalized(match.group(1)))
    if not labels: return None
    matches=[chapter for chapter in table['chapters'] if any(label in
        {normalized(chapter['title']),*(normalized(q['title']) for q in chapter['quests'])} for label in labels)]
    if len(matches)!=1: return None
    chapter=matches[0]
    category=next((c for c in table['categories'] if c['category_id']==chapter['category_id']),None)
    if category is None: return None
    result={'title':chapter['title'],'season':chapter['season'],'category_name':category['category_name'],
            'category_id':category['category_id'],'total':len(category['achievements']),
            'instance_state':'selected story only; instance entry unconfirmed',
            'chapter_achievement_ids':chapter.get('chapter_achievement_ids',[])}
    if snapshot and snapshot.get('fetched_at') and isinstance(snapshot.get('records'),list):
        completed={r.get('id') for r in snapshot['records'] if type(r.get('id')) is int and r.get('done') is True}
        result['completed']=sum(a['id'] in completed for a in category['achievements'])
        result['snapshot_time']=snapshot['fetched_at']
        related=set(chapter.get('chapter_achievement_ids',[]))
        result['unfinished_chapter_achievements']=[a for a in category['achievements'] if a['id'] in related and a['id'] not in completed][:8]
    return result

def story_context(observation,accounts):
    with accounts.lock:
        snapshot=accounts.snapshot if accounts.key and accounts.selected_game=='Guild Wars 2' else None
    result=selected_story(observation,snapshot)
    if not result: return ''
    return ('\nVerified story reference matched to visually read title (untrusted screen reading): '+json.dumps(result)+
        '\nThis identifies a selected story, not proof of being inside an instance. Category totals are not per-instance totals. '
        'Only chapter_achievement_ids are linked to this chapter by exact title or explicit Story Instance text; other category entries may belong elsewhere. '
        'Research the wiki before offering mechanics, missable requirements or a next step. Do not infer current eligibility from unfinished status.\n')
