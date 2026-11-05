"""Select labeled public facts before inference, independent of either model."""
import re
from .sections import body_text,map_context,event_context,collection_names,equipment_context

def focus_articles(question,articles,history=()):
    result=[]
    for source in articles:
        item=dict(source);text=item.get('text','')
        if not isinstance(text,str):result.append(item);continue
        focus=item.get('focus_text','');lines=text.splitlines();support=None
        track_rows=[]
        for line in focus.splitlines():
            fields=dict(part.split(': ',1) for part in line.split(' | ') if ': ' in part)
            if fields.get('Mastery') and fields.get('XP required') and fields.get('Points'):
                track_rows.append(fields)
        if track_rows:
            unlock=next((line for line in focus.splitlines() if line.startswith('Unlock context: ')),None)
            # Retain every retrieved level's name/cost before long descriptions.
            # The full source may still be partial; do not invent missing levels.
            core=[f"Mastery: {row['Mastery']} | XP required: {row['XP required']} | Points: {row['Points']} (cost)" for row in track_rows]
            effects=[f"Trained effect of {row['Mastery']}: {row['Description'][:180]}" for row in track_rows if row.get('Description')]
            focus='Requested mastery track: '+track_rows[0].get('Section',item['title'])+'\n'+'\n'.join(core)
            focus+='\nTraining order is the listed order within this track; later levels require earlier levels. Points are SPENT, not granted. Each row is one training level; XP is per level, not cumulative. Effects are benefits after training, not exclusive XP sources.'
            if unlock:focus+='\n'+unlock[:350]
            focus+='\n'+'\n'.join(effects)
            support=''
        # An achievement redirect can resolve to a chapter containing many
        # achievement rows. Keep the requested row and its attached notes.
        names=item.get('item_names',[])
        matches=[(match.start(),-len(name),name) for name in names if isinstance(name,str) for match in [re.search(r'(?<!\w)'+re.escape(name)+r'(?!\w)',question,re.I)] if match]
        requested=min(matches)[2] if matches else next((name for name in names if name.casefold()==item.get('requested_subject','').casefold()),None)
        comparison=re.search(r'\b(?:choose|branch|which path|which option)\b',question,re.I)
        switch=re.search(r'\b(?:switch|new goal|now help|instead help|work on .* instead)\b',question,re.I)
        anchored_goal=False
        if (comparison and not switch) or not matches:
            for turn in reversed(history):
                if turn.get('role')!='user':continue
                prior_text=turn.get('text','')
                if re.search(r'\b(?:choose|branch|which path|which option)\b',prior_text,re.I) and re.search(r'\bor\b',prior_text,re.I) and not re.search(r'\b(?:switch|new goal|now help|instead help)\b',prior_text,re.I):continue
                prior=[(m.start(),-len(name),name) for name in names for m in [re.search(r'(?<!\w)'+re.escape(name)+r'(?!\w)',prior_text,re.I)] if m]
                if prior:requested=min(prior)[2];anchored_goal=True;break
        if requested:
            standalone=item['title'].casefold()==requested.casefold()
            # Require a real single-line achievement header, not a collection
            # checklist entry or a name in navigation followed by an ellipsis.
            marker=re.search(r'(?m)^[ \t]*\|[ \t]*'+re.escape(requested)+r'[ \t]*\|[^\n]+',text,re.I)
            section=''
            if marker:
                section=text[marker.end():]
                others=[name for name in names if name!=requested]
                next_row=re.search(r'\n[ \t]*\|[ \t]*(?:'+'|'.join(re.escape(name) for name in others)+r')[ \t]*\|',section,re.I) if others else None
                if next_row:section=section[:next_row.start()]
            description=next((line.strip().strip('|').split('|')[0].strip() for line in section.splitlines() if line.strip().startswith('|') and len(line.strip().strip('|').split('|')[0].strip())>8),None)
            focus='Requested achievement: '+requested+' | Parent article: '+item['title']+'\n'
            item['title']=requested+' (entry in '+item['title']+')'
            if description and not re.fullmatch(r'[.\s…]+',description):
                objective=re.split(r'\b(?:Story Instance|Prerequisite|Unlock Item|Reward|Journal):',description,1,flags=re.I)[0].strip()
                unlock_item=re.search(r'Unlock Item:\s*(.*?)(?=\s+Reward:|\n|$)',description,re.I)
                prerequisite=re.search(r'Prerequisite:\s*([^|\n]+?)(?=\s+Reward:|\s*\||\n|$)',section,re.I)
                instance=re.search(r'Story Instance:\s*(.*?)(?=\s+(?:Prerequisite|Reward):|\s*\||\n|$)',section,re.I)
                focus+='Own objective: '+objective[:400]+'\n'
                if unlock_item:focus+='Required unlock item (NOT the target achievement): '+unlock_item.group(1).strip()[:120]+'\n'
                objective_rows=[[c.strip() for c in line.strip().strip('|').split('|')] for line in section.splitlines() if line.strip().startswith('|')]
                thresholds=[cells[1] for cells in objective_rows[:1] if len(cells)>1 and re.search(r'\d',cells[1])]
                thresholds+=[cells[0] for cells in objective_rows[1:] if re.match(r'(?:Unlocked\s+\d+\b|\d+\s+[^|]{0,70}\b(?:Collected|Completed|Exterminated|Unlocked)\b)',cells[0],re.I)]
                if thresholds:focus+='Completion thresholds (not current player progress): '+'; '.join(thresholds)[:400]+'\n'
                if standalone:
                    entries=collection_names(section)
                    if entries:
                        item['collection_items']=entries
                        focus+='Own collection items ('+str(len(entries))+' retrieved names): '+', '.join(entries)+'\n'
                if instance:focus+='Perform inside story instance: '+instance.group(1).strip()[:160]+'\n'
                if prerequisite:focus+='Listed prerequisite: '+prerequisite.group(1).strip()[:160]+'\n'
                # Keep the target's attached walkthrough/eligibility, ending at
                # the NEXT achievement. Do not drop these or import other rows.
                note_lines=[line.strip() for line in section.splitlines() if line.strip() and not line.strip().startswith('|')]
                notes=' '.join(note_lines)[:(450 if standalone else 950)]
                if notes:focus+='Own walkthrough/eligibility notes: '+notes+'\n'
                if instance:focus+='Story-instance objectives occur inside that instance, not in an invented open-world zone. '
                focus+='A prerequisite/category is not the objective. Do not infer an expansion, class, prerequisite or availability from the achievement/category name.'
            else:
                focus+='Evidence status: name confirmed only; its complete objective, walkthrough and availability were not retrieved. Do not invent a guide or infer mechanics from its name/category.'
            support=''
            availability=re.search(r'(?i)(?:This content|This achievement|These achievements|Daily Lunar New Year)[^\n]{0,220}\b(?:only available during|available during|historical|no longer available)[^\n]{0,180}',body_text(text))
            if availability:focus+='\nAvailability context: '+availability.group(0).strip()[:300]
        if re.search(r'\bType: Zone\b',focus,re.I):
            # Area-level rows and achievement-category totals are not map
            # completion counts. Icon-only objective counts need proper labels.
            focus+='\nLevels is area level, not a point total or a verified minimum entry requirement.\n'+map_context(text)
            support=''
        elif re.search(r'\bTrack:',focus) and re.search(r'\b(?:Experience|XP required):',focus):
            after=re.search(r'After completion:\s*(.*?)(?=\n|Before completion:|Notes|[“”]|$)',text,re.S|re.I)
            before=re.search(r'Before completion:\s*(.*?)(?=\n|After completion:|Notes|[“”]|$)',text,re.S|re.I)
            ability=(after or before)
            # The ability is essential, not optional scenery. Keep it ahead of
            # generic guidance so even a reduced prompt retains what is learned.
            if ability:focus='Trained ability (AFTER training): '+ability.group(1).strip()[:500]+'\n'+focus
            note=re.search(r'\nNotes\s*\n(.*?)(?=\n[^\n]+ mastery track|\nCentral Tyria|$)',text,re.S|re.I)
            if note:
                notes=' '.join(note.group(1).split())[:350]
                focus+='\nAbility-specific notes: '+notes
                skill=re.search(r'Levels up (?:the )?(.{1,60}?) crafting discipline to (\d+)',notes,re.I)
                if skill:focus+='\nCrafting skill after THIS training tier: '+skill.group(2)+'. This is not the overall discipline maximum or the character level.'
            focus+='\nSubject type: mastery training level, not an achievement. Experience is required training XP, not an exclusive XP source. Use the matching mastery region; the benefit is not an action required before earning XP.'
            support=''
        equipment=equipment_context(item.get('title',''),text,question)
        if equipment and not requested:focus=equipment;support=''
        event=event_context(question,text,item.get('title','Event'))
        if event and not requested:
            focus=event;support=''
        # Preserve reward-table column labels and the CURRENT timer together.
        # Historical added seconds are not a replacement for the infobox time.
        if re.search(r'\bType:?\s+Adventure\b',text,re.I):
            rows=[]
            for line in lines:
                cells=[c.strip() for c in line.split('|') if c.strip()]
                if len(cells)>=4 and cells[0].casefold() in ('gold','silver','bronze'):
                    row=f'Reward tier: {cells[0]} | Masks soothed: {cells[1]} | Reward XP (earned, not required): {cells[2]}' if 'Masks soothed' in text else ''
                    if row and row not in rows:rows.append(row)
            timer=re.search(r'\bTime limit\s*:?\s*(\d{1,2}:\d{2})\b',text,re.I)
            if rows:
                clock=''
                if timer:
                    minutes,seconds=map(int,timer.group(1).split(':'))
                    clock=f' | Current time limit: {timer.group(1)} ({minutes} minutes {seconds} seconds; not hours)'
                focus='Subject: '+item['title']+' | Type: Adventure'+clock+'\n'+'\n'.join(rows[:3])
                cap=re.search(r'if (\d+) masks have been soothed',text,re.I)
                if cap:focus+='\nAdventure ends at score cap: '+cap.group(1)+'. A lower reward threshold is not the adventure end condition.'
                route=re.search(r'\bGetting there\b(.*?)\bRewards\b',text,re.S)
                support=('Getting there and mechanics:\n'+route.group(1).strip()[:1800]) if route else ''
        if focus:
            if requested and anchored_goal:focus='Active player achievement goal remains '+requested+'. Mentioned alternatives are comparisons, not a goal change. Answer for '+requested+' first.\n'+focus
            item['focus_text']=focus[:2200]
            # Irrelevant navigation and patch notes need not reach the model.
            # Keep the existing text for bounded compaction of supporting detail.
            item['text']='Priority labeled facts (not player progress):\n'+item['focus_text']+'\nSupporting partial article:\n'+(text[:5000] if support is None else support)
            item['details_truncated']=True
        result.append(item)
    return result
