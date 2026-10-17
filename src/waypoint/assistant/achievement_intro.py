"""One deterministic, account-backed introduction per approved vision session."""
import re
from datetime import datetime,timezone
from waypoint.integrations.map_achievements import category_progress

class AchievementIntro:
    def __init__(self,table):
        self.table=table; self.previous=None; self.seen_stamp=None; self.sent=False
        self.reason='Waiting for map identification'

    def consider(self,observation,stamp,snapshot):
        if self.sent or not observation or stamp==self.seen_stamp: return None
        self.seen_stamp=stamp
        summary=observation.get('summary','')
        if re.search(r'(?i)\b(?:options|character selection|achievement panel|achievement menu)\b',summary):
            self.reason='Waiting for a readable map name'
            self.previous=None; return None
        browsing=bool(re.search(r'(?i)\b(?:map view|world map|viewing.{0,35}map)\b',summary))
        visible={re.sub(r'(?i)^Map displayed:\s*','',text).strip().casefold()
                 for text in observation.get('visible_text',[])}
        named=[row['map_name'] for row in self.table['maps'] if row['map_name'].casefold() in visible]
        map_name=observation.get('map')
        # A readable map title is useful even if the model correctly leaves
        # current location null while the player browses the map.
        explicit_map=browsing and len(named)==1
        if explicit_map: map_name=named[0]
        result=category_progress(map_name,snapshot,self.table) if isinstance(map_name,str) else None
        kind='map'; name=map_name
        if result is None:
            # Only an explicitly readable story header qualifies; story missions
            # are never mapped to nearby zones or inferred from watch-list names.
            labels=[text[len('Story episode: '):].strip() for text in observation.get('visible_text',[])
                    if text.startswith('Story episode: ')]
            episodes=[row for row in self.table.get('episode_categories',[]) if row['category_name'] in labels]
            if len(episodes)==1 and snapshot and snapshot.get('fetched_at') and isinstance(snapshot.get('records'),list):
                row=episodes[0]; ids={a['id'] for a in row['achievements']}
                done={r.get('id') for r in snapshot['records'] if type(r.get('id')) is int and r.get('done') is True}
                result={'completed':len(ids & done),'total':len(ids),'snapshot_time':snapshot['fetched_at']}
                kind='episode'; name=row['category_name']
        if result is None:
            self.reason='Waiting for a supported map or episode'
            self.previous=None; return None
        candidate=(kind,name)
        stable=explicit_map or self.previous==candidate; self.previous=candidate
        if not stable:
            self.reason='Confirming map on the next vision pass'
            return None
        try:
            datetime.fromisoformat(result['snapshot_time']).astimezone(timezone.utc)
        except (ValueError,TypeError): return None
        scope=(f"{name}'s dedicated map achievement categories" if kind=='map' else
               f"Living World Season 1: {name} (episode category)")
        self.sent=True
        self.reason='Achievement introduction sent'
        location_note='For the displayed map: ' if browsing and kind=='map' else ''
        return f"{location_note}You have {result['completed']}/{result['total']} achievements completed in {scope}."
