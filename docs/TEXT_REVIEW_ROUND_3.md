# GW2 text review, October 10, 2026

Reviewed local-data/text-playtests/20261010-193047-035277/conversations.jsonl. This stopped run has no summary.json; metrics are calculated from 98 saved turn records across 21 sessions, not a confirmed full three-hour run.

- Median copilot answer-path time: 24.69 seconds, including planning/retrieval.
- Median 1B follow-up generation: 7.44 seconds.
- 15 responses reported lookup failures; 17 reported no matching wiki reference.
- 15 turns used a controlled player-generation fallback; one record has a pipeline error.
- These counts are not an accuracy score. Automated flags missed substantial factual errors.

## Findings

The 1B player sometimes invented names, adopted the helper role, repeated questions or drifted from the scenario. The 12B copilot fabricated Fallen Masks collection steps and Dug In objects, confused nearby mastery-insight directions with the Wyvern boss route, and repeated unsupported prior claims.

Cached evidence explains part of this: the Wyvern route query retrieved Pile of Guano and a mastery insight; Fallen Masks retrieved a broad achievement category and an unrelated adventure. More model instructions alone cannot fix wrong evidence.

## Local changes

Keep the original player question in each 1B follow-up prompt. Reject more helper-role phrasings and newly invented quoted names, using the existing controlled fallback. This is a limited guard, not a complete named-entity validator.

For GW2 regression topics, fetch the canonical mechanics page: Legendary Wyvern Matriarch, Fallen Masks, and Torn from the Sky for Dug In. Other searches preserve MediaWiki search rank. Lookup planning asks for concise subject terms and prioritizes prior user questions over assistant claims. Reference cache version is incremented so old misleading extracts are refetched.

Copilot guidance separates adventures, collections, bosses and story achievements, and prohibits deriving directions or requirements from related links and reward labels.

Official evidence: https://wiki.guildwars2.com/wiki/Fallen_Masks and https://wiki.guildwars2.com/wiki/Torn_from_the_Sky . Fallen Masks is an adventure; Dug In is a story achievement. This update does not hardcode their answers or fine-tune either model.

## Validation and next run

Affected unit checks passed: 11 tester, 12 web lookup, 18 research, and 9 resource tests. The full-suite attempt crashed in Tkinter image teardown, so a full-suite pass is not claimed. No live model-quality retest or Windows rebuild has been performed for these changes.

Close the GUI and let both prior test engines exit. Start run-gw2-wiki-for-training.cmd for the next three-hour text batch. Review the first three regression subjects before a long unattended run. Stop with stop-gw2-wiki-for-training.cmd; allow active inference and cleanup to finish. No capture is started. Reports remain local; do not upload raw account conversations.

These source changes do not update an already downloaded Windows executable. Rebuild and verify the Windows package only after live answer-quality testing. The training launcher prepares test records for review; it does not update model weights.
