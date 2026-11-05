"""Bounded, labeled sections from public wiki text; never account or screen state."""
import re


def body_text(text):
    return text.split('Article details:',1)[-1].strip()


def section(text,heading):
    """Read one known section without importing the next section's meaning."""
    headings=r'Getting there|Access|Map completion|Locations|Objectives|Rewards|NPCs|Notes|Trivia|Walkthrough|Collection items|Related achievements|Achievements|Dialogue|Mechanics|See also|Gallery|References|Acquisition|Crafting|Looting|Vendors|Used in|Available prefixes|Recipe list|Types'
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
    access_lines=[line.strip() for line in section(body,'Getting there').splitlines() if line.strip() and '|' not in line]
    content=[line for line in access_lines if re.search(r'\b(?:required|requires?|unlocked|access to)\b',line,re.I) and not re.search(r'^(?:Using|Complete|By)\b',line,re.I)]
    routes=[line for line in access_lines if line not in content]
    # Only explicitly labeled counters can establish objective counts. Never
    # reinterpret reward gear, area levels or a bare run of numbers as objectives.
    counts=re.findall(r'\b(\d+)\s*\[(waypoints?|renown hearts?|points? of interest|vistas?|hero challenges?)\]',intro,re.I)
    facts=['Map description (takes precedence over assumptions from Type=Zone): '+intro]
    if counts:facts.append('Map objective counts: '+'; '.join(f'{label}: {number}' for number,label in counts))
    else:facts.append('Map objective counts were not retrieved with reliable labels; do not invent them.')
    if content:facts.append('Required content access (NOT whole-episode completion): '+' '.join(content)[:300])
    if routes:
        facts.append('Choose ONE supported entry route, not all routes: '+'; '.join(routes)[:550])
    if access_lines:facts.append('Owning/unlocking required content is not finishing the entire episode. Do not require a story route AND a portal item. Missing objective counts do not mean a zone has no map objectives.')
    reward=re.search(r'(?im)^\s*(\d+ piece of gear[^\n]*drop tables[^\n]*)',section(body,'Map completion'))
    if reward:facts.append('Map completion reward, NOT a requirement: '+reward.group(1).strip()[:200])
    facts.append('Map completion rewards are earned AFTER completion, never items required to complete the map. Adjacent maps are not sub-areas.')
    facts.append('Mail senders and congratulatory mail subjects are not achievement names or a completion checklist.')
    return '\n'.join(facts)


def equipment_context(title,text,question=''):
    """Keep acquisition routes and crafting-rating tables out of each other's scope."""
    body=body_text(text)
    if title in ('Ascended armor','Ascended equipment') and re.search(r'\b(?:stats?|prefix|infusions?|salvag\w*|upgrade slots?)\b',question,re.I):return None
    if title=='Ascended equipment':
        binding=re.search(r'(?i)(?:All\s+)?ascended equipment is account[ -]bound[^.\n]*',body)
        if binding:return binding.group(0)+'.\nAccount-bound finished equipment cannot be bought on the Trading Post. Buying tradable crafting materials/components is a different route; do not describe it as buying finished ascended gear.'
    if title=='Ascended armor':
        crafting=section(body,'Crafting')
        crafting=re.sub(r'(?im)^Primary article:[^\n]*\n?','',crafting)
        paragraphs=[p.strip() for p in re.split(r'\n\s*\n',crafting) if p.strip()]
        routes=[]
        for p in paragraphs:
            label='Collection-specific recipe route' if 'Envoy' in p else 'Crafted mark exchange route' if 'Grandmaster Marks' in p else 'Standard armor crafting route'
            direction='INPUT: crafted Grandmaster Marks; OUTPUT: ascended armor. ' if label=='Crafted mark exchange route' else ''
            routes.append(label+': '+direction+' '.join(p.split())[:850])
        if not routes:return None
        return 'No best route has been established for this player. A profession alone does not justify prioritizing a raid/Envoy route; ask about build, slots, content access and budget.\n'+'\n'.join(routes[:3])+('\nThese are alternative acquisition routes. Envoy collection conditions are not prerequisites for all ascended armor. Daily material crafting limits are not one full armor set per day. Trading Post materials/components are not finished ascended armor. Do not invent player groups as gear vendors.')
    if title=="Crafter's backpack":
        rows=[]
        for line in body.splitlines():
            cells=[c.strip() for c in line.split('|') if c.strip()]
            if len(cells)==3 and cells[0].isdigit() and cells[1].isdigit():
                rows.append(f'Crafting rating={cells[0]}; required character equip level={cells[1]}; item rarity={cells[2]}')
        professions=sorted(set(re.findall(r'\[(?:discipline: )?(Armorsmith|Artificer|Chef|Huntsman|Jeweler|Leatherworker|Scribe|Tailor|Weaponsmith)\]',body)))
        if not professions:
            professions=sorted(set(re.findall(r'\|\s*(Armorsmith|Artificer|Chef|Huntsman|Jeweler|Leatherworker|Scribe|Tailor|Weaponsmith)\s*\|',body)))
        if not rows:return None
        return 'Crafted back-slot equipment, NOT inventory bags.\n'+'\n'.join(rows)+('\nRetrieved recipe disciplines: '+', '.join(professions) if professions else '')+'\nCrafting rating and equip level are distinct. Equippable by a level-80 character does not mean this is a level-80 item. Do not invent a higher tier or omit retrieved disciplines.'
    if title=='Bag':
        crafting=section(body,'Crafting')
        if not crafting and len(body)<400:crafting=body
        professions=sorted(set(re.findall(r'\[(?:discipline: )?(Armorsmith|Artificer|Chef|Huntsman|Jeweler|Leatherworker|Scribe|Tailor|Weaponsmith)\]',crafting)))
        if not professions:professions=sorted(set(re.findall(r'\b(?:Armorsmith|Leatherworker|Tailor)\b',crafting)))
        return 'Inventory bags, NOT back-slot equipment.\n'+('Verified crafting disciplines in the retrieved section: '+', '.join(professions) if professions else 'Crafting discipline names were not retrieved; do not invent a discipline from a bag name.')+'\nCraftsman is a bag type, not a crafting discipline or mastery region. Bag capacity, recipe rating and ingredient quantities are different fields.\nCrafting-section evidence: '+' '.join(crafting.split())[:900]
    return None


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
