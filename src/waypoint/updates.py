"""Read-only public release discovery. No tokens, downloads or installation."""
import http.client,json,re,ssl
from .version import VERSION

REPOSITORY = 'JTanthony93/GW2-VLM-COPILOT'
RELEASES_URL = 'https://github.com/'+REPOSITORY+'/releases'

def version_key(tag):
    match=re.fullmatch(r'v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-(alpha|beta|rc)(?:\.(0|[1-9]\d*))?)?',tag if isinstance(tag,str) else '')
    if not match: return None
    major,minor,patch,stage,number=match.groups()
    return (int(major),int(minor),int(patch),{'alpha':0,'beta':1,'rc':2,None:3}[stage],int(number or 0))

def newer_windows_release(releases,current=VERSION):
    installed=version_key(current)
    if installed is None: raise ValueError('Invalid installed version.')
    if not isinstance(releases,list): raise ValueError('Invalid release list.')
    candidates=[]
    for release in releases:
        if not isinstance(release,dict) or release.get('draft'): continue
        tag=release.get('tag_name'); version=version_key(tag)
        if version is None or version<=installed: continue
        expected='GW2-VLM-COPILOT-v'+tag.removeprefix('v')+'-windows-x64.zip'
        assets=release.get('assets',[])
        if not isinstance(assets,list) or not any(isinstance(a,dict) and a.get('name')==expected and a.get('state')=='uploaded' and isinstance(a.get('size'),int) and a['size']>0 for a in assets): continue
        # Construct a fixed repository URL; never open URLs supplied in release text.
        candidates.append((version,{'version':tag.removeprefix('v'),'url':RELEASES_URL+'/tag/'+tag}))
    return max(candidates,key=lambda item:item[0])[1] if candidates else None

def check_for_update(current=VERSION):
    connection=http.client.HTTPSConnection('api.github.com',timeout=8,context=ssl.create_default_context())
    try:
        connection.request('GET','/repos/'+REPOSITORY+'/releases?per_page=100',headers={'Accept':'application/vnd.github+json','User-Agent':'GW2-VLM-COPILOT/'+current,'X-GitHub-Api-Version':'2022-11-28'})
        response=connection.getresponse()
        if response.status!=200: raise RuntimeError('Release check unavailable.')
        if 'application/json' not in response.getheader('Content-Type','').lower(): raise ValueError('Invalid release response.')
        raw=response.read(1000001)
        if len(raw)>1000000: raise ValueError('Release response too large.')
        return newer_windows_release(json.loads(raw),current)
    finally: connection.close()
