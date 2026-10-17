"""One deterministic, account-backed introduction per approved vision session."""
import re
from datetime import datetime,timezone
from waypoint.integrations.map_achievements import category_progress

class AchievementIntro:
    def __init__(self,table):
        self.table=table; self.previous=None; self.seen_stamp=None; self.sent=False

    def consider(self,observation,stamp,snapshot):
        if self.sent or not observation or stamp==self.seen_stamp: return None
        self.seen_stamp=stamp
        summary=observation.get('summary','')
        # Browsing a world map/category doesn't prove current player location.
        if re.search(r'(?i)\b(?:map view|world map|viewing.{0,35}map|options|character selection|achievement panel|achievement menu)\b',summary):
            self.previous=None; return None
        map_name=observation.get('map')
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
            self.previous=None; return None
        candidate=(kind,name)
        stable=self.previous==candidate; self.previous=candidate
        if not stable: return None
        try:
            stamp_text=datetime.fromisoformat(result['snapshot_time']).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
        except (ValueError,TypeError): return None
        scope=(f"{name}'s dedicated map achievement categories" if kind=='map' else
               f"Living World Season 1: {name} (episode category)")
        self.sent=True
        return f"You have {result['completed']}/{result['total']} achievements completed in {scope}.\n\nBased on your account snapshot from {stamp_text}; this is not live progress."
