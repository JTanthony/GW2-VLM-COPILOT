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
stop after three consecutive retrieval failures; this does not prove a sitewide
outage. Request statistics record token counts, never raw prompts.

The text runner fingerprints the shared rules with the other reviewed code.
These changes adjust application behavior; neither model learns automatically
and no model weights are trained. Developer logs and account data stay private.

Run the shared regression checks from the repository root:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_text_rules.py'
```
