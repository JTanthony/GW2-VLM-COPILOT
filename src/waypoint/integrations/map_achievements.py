"""Dedicated map-category membership and deterministic snapshot counts."""
import json
from waypoint.paths import app_root

def load_table():
    path=app_root()/'data/gw2/map_achievements.json'
    data=json.loads(path.read_text('utf-8'))
    if data.get('schema_version')!=1 or not isinstance(data.get('maps'),list):
        raise ValueError('Unsupported map achievement table.')
    return data

def category_progress(map_name,snapshot,table=None):
    """No model arithmetic, inferred ownership, or missing-record completion."""
    if not snapshot or not isinstance(snapshot.get('records'),list) or not snapshot.get('fetched_at'):
        return None
    table=load_table() if table is None else table
    matches=[row for row in table['maps'] if row['map_name'].casefold()==map_name.strip().casefold()]
    if len(matches)!=1: return None
    row=matches[0]; ids={item['id'] for item in row['achievements']}
    completed={record.get('id') for record in snapshot['records']
               if type(record.get('id')) is int and record.get('done') is True}
    return {'map_name':row['map_name'],'category_id':row['category_id'],
            'category_ids':[category['id'] for category in row.get('categories',[])],
            'completed':len(ids & completed),'total':len(ids),
            'snapshot_time':snapshot['fetched_at'],'table_verified_at':table['verified_at'],
            'scope':'dedicated map achievement category'}
