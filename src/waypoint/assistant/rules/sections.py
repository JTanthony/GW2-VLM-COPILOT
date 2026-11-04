"""Bounded, labeled sections from public wiki text; never account or screen state."""
import re


def body_text(text):
    return text.split('Article details:',1)[-1].strip()


def section(text,heading):
    """Read one known section without importing the next section's meaning."""
    headings=r'Getting there|Access|Map completion|Locations|Objectives|Rewards|NPCs|Notes|Trivia|Walkthrough|Collection items|Related achievements|Achievements|Dialogue|Mechanics|See also|Gallery|References'
    match=re.search(r'(?im)^\s*'+re.escape(heading)+r'\s*$',text)
    if not match:return ''
    rest=text[match.end():]
    end=re.search(r'(?im)^\s*(?:'+headings+r')\s*$',rest)
    return (rest[:end.start()] if end else rest).strip()


def map_context(text):
    body=body_text(text)
    intro=re.split(r'(?im)^\s*(?:Getting there|Map completion|Locations|Rewards|Notes)\s*$',body,1)[0]
    intro='\n'.join(line for line in intro.splitlines() if '|' not in line)
    intro=' '.join(intro.split())[:650]
    access=' '.join(section(body,'Getting there').split())[:650]
    # Only explicitly labeled counters can establish objective counts. Never
    # reinterpret reward gear, area levels or a bare run of numbers as objectives.
    counts=re.findall(r'\b(\d+)\s*\[(waypoints?|renown hearts?|points? of interest|vistas?|hero challenges?)\]',intro,re.I)
    facts=['Map description (takes precedence over assumptions from Type=Zone): '+intro]
    if counts:facts.append('Map objective counts: '+'; '.join(f'{label}: {number}' for number,label in counts))
    else:facts.append('Map objective counts were not retrieved with reliable labels; do not invent them.')
    if access:
        facts.append('Access instructions: '+access)
        facts.append('Separate required content access from entry routes. Owning/unlocking an episode is not completing the whole episode. Listed portal, friend-teleport and story-entry routes are alternatives, not cumulative tasks.')
    reward=re.search(r'(?im)^\s*(\d+ piece of gear[^\n]*drop tables[^\n]*)',section(body,'Map completion'))
    if reward:facts.append('Map completion reward, NOT a requirement: '+reward.group(1).strip()[:200])
    facts.append('Map completion rewards are earned AFTER completion, never items required to complete the map. Adjacent maps are not sub-areas.')
    return '\n'.join(facts)


def event_context(question,text,title):
    body=body_text(text)
    if not re.search(r'\bEvent type\s+(?:Dynamic|Group|Meta) event\b',body,re.I):return None
    intro=re.split(r'(?im)^\s*Objectives\s*$',body,1)[0]
    intro=re.sub(r'\|\s*Interactive map.*?(?:\n\s*\n|$)','',intro,flags=re.S)
    facts=['Event: '+title,'Location, event type and chain context: '+' '.join(intro.split())[:1100]]
    objectives=' '.join(section(body,'Objectives').split())[:450]
    notes=' '.join(section(body,'Notes').split())[:650]
    if objectives:facts.append('Own event objective: '+objectives)
    if notes:facts.append('Event notes (preserve which event each condition applies to): '+notes)
    facts.append('Event level is a difficulty label, not proof of a strict entry minimum. Group event recommends a group; it does not itself prove solo participation is forbidden. Preceded by and Followed by refer to different events.')
    if re.search(r'\b(?:reward\w*|coins?|gold|silver|copper|karma|experience|xp)\b',question,re.I):
        rewards=section(body,'Rewards')
        rows=[]
        for line in rewards.splitlines():
            cells=[c.strip() for c in line.split('|') if c.strip()]
            if len(cells)!=4 or cells[0].lower() not in ('gold','silver','bronze'):continue
            if not all(re.fullmatch(r'[\d,]+',c) for c in cells[1:3]):continue
            money=re.findall(r'([\d,]+)\s*\[((?:gold|silver|copper)(?: coin)?)\]',cells[3],re.I)
            if not money:continue
            coins=', '.join(f'{n} {unit.lower().replace(" coin","")}' for n,unit in money)
            rows.append(f'Medal tier={cells[0]}; earned XP={cells[1]}; karma={cells[2]}; currency={coins}. Medal is NOT currency; XP is NOT gold.')
        facts[1:1]=rows
        if not rows:facts.append('Currency units could not be verified; omit precise money amounts.')
        scaling=' '.join(rewards.splitlines()[-2:])
        if 'level' in scaling.lower():facts.append('Reward scaling note: '+scaling[:250])
    else:facts.append('No reward amounts requested. Omit optional reward numbers; focus on starting and completing this event.')
    return '\n'.join(facts)


def collection_names(text):
    names=[]
    for line in section(text,'Collection items').splitlines():
        cells=[c.strip() for c in line.split('|') if c.strip()]
        if len(cells)>=3 and cells[0].isdigit() and cells[1] not in names:
            names.append(cells[1])
    return names[:30]
