# Shared text-response rules

`src/waypoint/assistant/rules/text.py` contains the shared evidence guidance,
answer style and response budgets. `evidence.py` selects the relevant public
reference passages before the assistant answers. Model settings and vision
analysis remain in their existing modules.

The selector keeps requested achievement objectives, story-instance requirements
and attached branch notes; mastery benefits and individual point costs; and
labeled adventure timers and rewards. It preserves the established achievement
goal through comparison follow-ups while allowing explicit goal changes.
Name-only fragments are insufficient evidence for a detailed guide. Source
records and data tables are not modified.

Research distinguishes social introductions from factual questions and reports
wiki maintenance or lookup failures without inventing a guide. Text batches
use bounded recovery after three consecutive retrieval failures; this does not
prove a sitewide outage. Request statistics record token counts, never raw prompts.

The text runner fingerprints the shared rules with the other reviewed code.
These changes adjust application behavior; neither model learns automatically
and no model weights are trained. Developer logs and account data stay private.

Run the shared regression checks from the repository root:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_text_rules.py'
```

## Structured sections

`src/waypoint/assistant/rules/sections.py` reads bounded event reward fields,
map introduction/access sections and collection rows. Medal tiers are distinct
from coin units and earned XP. Unsolicited event reward amounts are omitted.
Achievement completion thresholds are requirements, never account progress.
Map rewards cannot be reinterpreted as completion objectives. Objective icons
retain explicit labels; unlabeled numbers never establish counts.

Mastery rows retain per-level costs and listed progression order. XP-source
questions may add one cached generic Mastery reference; an optional supplement
failure preserves the retrieved ability evidence. This does not establish the
player's current training progress. The text tester fingerprints the section
selector and reminds its simulated player that catalog IDs are not levels.

Reference extraction version 11 refreshes older cached extracts on their next
lookup, allowing new icon labels to be captured. Historical reports are retained.


## Acquisition routes and ambiguous subjects

Armor crafting, crafted-mark exchange and collection-specific recipes retain
separate route labels. Backpack tables keep crafting rating, equip level and
rarity separate. Crafting-discipline and map-objective icon links retain their
labels even when image alt text is absent. The Bag crafting section is retained
before unrelated property tables. Existing cached references refresh on next use.

Qualified story-area names are preserved. Inner Nayos mastery-track questions
are routed separately from Inner Nayos map questions. A collection's Unlock Item
field is treated as a prerequisite rather than its target. Mastery training and
progression questions can request a bounded general Mastery reference.

Map entry routes are alternatives unless the source explicitly says otherwise;
content access, story completion and portal ownership are different conditions.
Mail senders and congratulations are not achievement names. These rules improve
supplied evidence; factual quality still needs end-to-end model testing.
