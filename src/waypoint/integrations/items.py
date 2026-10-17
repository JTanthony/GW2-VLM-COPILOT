"""Bounded public item metadata; no account token or inventory access."""
import json,re,ssl
from html import unescape
from waypoint.assistant.web_lookup import PinnedHTTPS

def item_records(ids):
    ids=sorted(set(ids))[:8]
    if not ids or any(type(value) is not int or value<=0 for value in ids):
        return []
    connection=PinnedHTTPS('api.guildwars2.com',timeout=8,context=ssl.create_default_context())
    try:
        connection.request('GET','/v2/items?ids='+','.join(map(str,ids))+'&lang=en',
                           headers={'Accept':'application/json','User-Agent':'GW2-VLM-COPILOT'})
        response=connection.getresponse()
        if response.status not in (200,206): raise ValueError('Public item lookup unavailable.')
        if 'application/json' not in response.getheader('Content-Type','').lower():
            raise ValueError('Invalid public item response.')
        raw=response.read(100001)
        if len(raw)>100000: raise ValueError('Public item response too large.')
        records=json.loads(raw)
        if not isinstance(records,list): raise ValueError('Invalid public item response.')
        clean=[]
        for record in records:
            if not isinstance(record,dict) or type(record.get('id')) is not int or record['id'] not in ids or not isinstance(record.get('name'),str): continue
            item={'id':record['id'],'name':record['name'][:200]}
            for key in ('type','rarity','level','flags','restrictions','vendor_value'):
                value=record.get(key)
                if isinstance(value,str): item[key]=value[:200]
                elif type(value) is int: item[key]=value
                elif isinstance(value,list): item[key]=[v[:100] for v in value[:20] if isinstance(v,str)]
            if isinstance(record.get('description'),str):
                item['description']=unescape(re.sub(r'<[^>]*>','',record['description']))[:800]
            clean.append(item)
        return clean
    finally: connection.close()
