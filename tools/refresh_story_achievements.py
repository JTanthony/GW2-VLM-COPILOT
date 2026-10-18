"""Public story-category membership and conservative exact-title chapter links."""
import json,re,sys
from html import unescape
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from refresh_map_achievements import fetch,batches

def title(value):
    value=re.sub(r'^\s*\d+\.\s*','',value)
    return ' '.join(re.findall(r'\w+',value.casefold())).removeprefix('the ')

def build():
    groups=fetch('/v2/achievements/groups?ids=all')
    group=next(g for g in groups if g['name']=='Story Journal')
    categories=batches('/v2/achievements/categories?ids=',group['categories'])
    ids=sorted({a['id'] if isinstance(a,dict) else a for c in categories for a in c['achievements']})
    details=batches('/v2/achievements?ids=',ids)
    if {a['id'] for a in details}!=set(ids): raise ValueError('Incomplete story achievement details.')
    by_id={a['id']:a for a in details}
    seasons={s['id']:s['name'] for s in fetch('/v2/stories/seasons?ids=all')}
    stories=[s for s in fetch('/v2/stories?ids=all') if seasons.get(s['season']) not in ('My Story',"Scarlet's War")]
    quests=fetch('/v2/quests?ids=all')
    rows=[]
    for c in categories:
        members=[a['id'] if isinstance(a,dict) else a for a in c['achievements']]
        rows.append({'category_id':c['id'],'category_name':c['name'],'scope':'story category, not current-instance achievement list',
            'source':'https://api.guildwars2.com/v2/achievements/categories/'+str(c['id']),
            'achievements':[{'id':i,'name':by_id[i]['name'],'flags':by_id[i].get('flags',[]),
                'prerequisites':by_id[i].get('prerequisites',[])} for i in sorted(set(members))]})
    chapters=[]; unresolved=[]
    for story in stories:
        name=re.sub(r'^\s*\d+\.\s*','',story['name']).strip()
        direct=[c for c in rows if title(c['category_name'])==title(name)]
        matches=direct or [c for c in rows if any(title(a['name'])==title(name) for a in c['achievements'])]
        if len(matches)!=1:
            unresolved.append({'story_id':story['id'],'title':name,'season':seasons[story['season']],
                'reason':'No unique exact category or achievement-title match; no inferred act mapping.'})
            continue
        chapter_quests=[{'quest_id':q['id'],'title':q['name']} for q in quests if q['story']==story['id']]
        related=[]
        for achievement in matches[0]['achievements']:
            raw=by_id[achievement['id']]
            text=unescape(re.sub(r'<[^>]*>','',raw.get('description','')+'\n'+raw.get('requirement','')))
            instance=re.search(r'Story Instance:\s*["“]([^"”\n]+)',text,re.I)
            if title(achievement['name'])==title(name) or (instance and title(instance.group(1))==title(name)):
                related.append(achievement['id'])
        chapters.append({'story_id':story['id'],'title':name,'season':seasons[story['season']],
            'category_id':matches[0]['category_id'],'mapping_basis':'exact category title' if direct else 'exact achievement title',
            'chapter_achievement_ids':related,
            'quests':chapter_quests})
    return {'schema_version':1,'verified_at':datetime.now(timezone.utc).isoformat(),
        'scope':'Public Story Journal categories and exact-title story/quest links, Season 1 through Visions of Eternity. Instance entry and availability are not inferred.',
        'categories':rows,'chapters':chapters,'unresolved_chapters':unresolved,
        'sources':['https://api.guildwars2.com/v2/stories?ids=all','https://api.guildwars2.com/v2/quests?ids=all',
                   'https://wiki.guildwars2.com/wiki/Story_Journal/table']}

def main():
    data=build();target=ROOT/'data/gw2/story_achievements.json';target.parent.mkdir(parents=True,exist_ok=True)
    temporary=target.with_suffix('.tmp');temporary.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');temporary.replace(target)
    print(json.dumps({'categories':len(data['categories']),'achievements':sum(len(c['achievements']) for c in data['categories']),
        'mapped_chapters':len(data['chapters']),'unresolved_chapters':len(data['unresolved_chapters'])}))
    print('Night of Fires:',[(c['title'],c['category_id']) for c in data['chapters'] if c['title']=='Night of Fires'])
    print('Mapped seasons:',sorted({c['season'] for c in data['chapters']}))

if __name__=='__main__':main()
