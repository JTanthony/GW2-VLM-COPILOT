"""Reduce optional evidence without dropping the current question or instructions."""
import json,re

def compact(prompt,level):
    # History is stored as JSON. Parse it rather than cutting through a turn.
    for match in reversed(list(re.finditer(r'(?:Previous conversation: |\n)(?=\[\{"role")',prompt))):
        start=match.end()
        try: history,end=json.JSONDecoder().raw_decode(prompt[start:])
        except ValueError: continue
        keep=2 if level==1 else 0
        prompt=prompt[:start]+json.dumps(history[-keep:] if keep else [])+prompt[start+end:]
    marker='Distinguish article facts from current screen evidence.\n'
    start=prompt.find(marker)
    if start<0: return prompt
    start+=len(marker)
    try: articles,end=json.JSONDecoder().raw_decode(prompt[start:])
    except ValueError: return prompt
    question=re.search(r'Player question: (.*?)(?:Adapt to the game|$)',prompt,re.S)
    terms=set(re.findall(r'\w{3,}',question.group(1).lower() if question else ''))
    reduced=[]
    for article in articles:
        item=dict(article)
        text=item.get('text','')
        if isinstance(text,str):
            passages=re.split(r'(?<=[.!?])\s+|\n+',text)
            ranked=sorted(enumerate(passages),key=lambda p:-len(terms & set(re.findall(r'\w{3,}',p[1].lower()))))
            selected=[]; limit={1:2200,2:1000,3:400}[level]
            focused=[row for row in item.pop('focus_text','').splitlines() if len(row)<=limit]
            preserved=[]; used=0
            for row in focused:
                if used+len(row)+1<=limit: preserved.append(row); used+=len(row)+1
            for index,passage in ranked:
                if used+len(passage)<=limit:
                    selected.append((index,passage)); used+=len(passage)
            item['text']='\n'.join(preserved+[p for _,p in sorted(selected)])
            item['details_truncated']=True
        # Large lists have a separate deterministic answer path; avoid flooding
        # model requests with duplicate category metadata.
        for key in ('item_names','items'): item.pop(key,None)
        reduced.append(item)
    return prompt[:start]+json.dumps(reduced,ensure_ascii=False)+prompt[start+end:]+ '\nReference extracts were shortened to fit memory. They are partial evidence; do not claim exhaustive coverage.'
