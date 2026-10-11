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

The initial targeted checks passed; an earlier full-suite attempt crashed during Tkinter image teardown. The subsequent release validation passed all 110 automated tests. The v0.1.8-alpha Windows package was rebuilt and its GUI smoke check exited successfully. No live model-quality retest has been performed; these checks do not establish factual accuracy gains.

Close the GUI and let both prior test engines exit. Start run-gw2-wiki-for-training.cmd for the next eight-hour text batch. Review the first three regression subjects before a long unattended run. Stop with stop-gw2-wiki-for-training.cmd; allow active inference and cleanup to finish. No capture is started. Reports remain local; do not upload raw account conversations.

These source changes do not update an already downloaded Windows executable. The rebuilt alpha is for evaluation; verify live answer quality before claiming improvements. The training launcher prepares test records for review; it does not update model weights.
