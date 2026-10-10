# Gemma 3 simulated player

The developer runner tests conversation and account progress only. It does not import capture modules, analyze screenshots, control the game, edit app code or train weights. Gemma 3 1B IT generates short player follow-ups; GW2 VLM COPILOT's configured model answers through the normal Assistant chat path. Controlled starter questions establish a player role and goal. The small model is not the authority on correctness.

## Start and stop

Close GW2 VLM COPILOT with the close button before running this test, so its local engine port is free. Double-click **run-gw2-wiki-for-training.cmd** in the source project folder to test with the saved account token for the configured game (currently Guild Wars 2). A successful earlier connection in Accounts must already have saved that token. The runner uses Windows protection to unlock it inside the account adapter, fetches one dated snapshot, and never prints the token or passes it to either model. Account progress and generated replies may appear in the local test logs; keep those logs private. There is no automatic account refresh during a run.

Double-click **stop-gw2-wiki-for-training.cmd** to request a stop. The current inference finishes before both owned engines close. A new explicit launch clears the stop flag only after both engine ports are free; starting too early shows a message. Existing app engines are never reused or stopped by this runner.

The training launcher sets limits of 1,000 sessions, five turns each and at most three hours, whichever comes first. The command-line runner defaults to four turns and eight hours unless overridden. Despite the launcher name, this is testing and preparation of review material; neither model is trained automatically. Three generation/request errors stop the run early. This batch uses only the official GW2 wiki. Gemma 12B plans the lookup and reasons over the returned plain-text extracts; Gemma 3 generates player follow-up questions. No website commands or downloads are executed. Test goals and notes are isolated under the report directory, not the player's normal project resources.

For a short check with dummy account records:

```powershell
.\.venv\Scripts\python.exe tools\run_text_sessions.py --sessions 4 --turns 2 --hours 0.2 --account-mode dummy
```

The account connection in this tester is restricted to Guild Wars 2. Other titles are excluded from this focused batch.

## Models and settings

`config/player.local.json`: Gemma 3 1B IT Q4_K_M, CPU only (`device=none`, zero GPU layers, CPU KV cache), two threads, 2,048 context, port 17866. Question generation uses temperature 0.8 and a 192-token response limit. Store the downloaded model in a local model directory and set its path in `config/player.local.json`. Keep model files out of Git; record the download revision and checksum privately. Source: [llama.cpp organization's GGUF](https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF).

GW2 VLM COPILOT uses `config/inference.local.json` on port 17865, with the visual projector omitted only in this text-only test process. The normal app's vision configuration is unchanged. Both models stay local. Running the standalone tester consumes no Codex chat allowance; Codex usage applies when reviewing results or making edits. An assisted review still respects the owner's 35% remaining allowance reserve. The standalone process cannot read Codex account usage.

## Debrief

Each timestamped folder under `local-data/text-playtests` contains:

- `conversations.jsonl`: every question, actual reply, response time, error and suggested flag.
- `summary.json`: run counts and stop reason.
- `debrief.md`: flagged turns and errors for review.

Flags identify possible contradictions, unwanted capture discussion, responses over 45 seconds and possible requests for the player to search or paste a guide. They can produce false positives or miss subtle errors. Review the full conversations alongside the applicable evidence before making code changes. Credentials never belong in these logs.

## MMO player pain points

The current runner filters `src/waypoint/testing/test_titles.json` to Guild Wars 2 only. The other title entries are retained as development scaffolding and are not exercised by this batch. The runner uses the official GW2 wiki and one dated account snapshot; it does not establish support for other games.

GW2 regression starters live in `src/waypoint/testing/gw2_wiki_scenarios.json` and are tried before the general scenarios in `src/waypoint/testing/mmo_scenarios.json`. It covers quick achievement wins, complex multi-step achievements, blocked prerequisites, zone checklists, efficient routes, timed events, solo/group barriers, reward and currency choices, returning-player overload, progress that did not count, and research delivered inside chat. The runner adds short-session planning, saved-goal checks and named completion checks when account evidence exists. Scenarios use the selected game; they do not assume GW2 mechanics or that every game has an account connector.

Each session starts with a controlled player question. Gemma 3 then receives a different follow-up intent for each turn and the latest replies: clarify an unlock, ask for ordered steps, request a solo alternative, check uncertainty, or ask for an immediate next action. It must use supplied names rather than inventing locations, achievements or account facts. The small model's questions still need review; scenario coverage does not prove the answers are accurate.

The goal is to keep players in the game. Review whether answers include actionable steps, prerequisites, relevant time/group/cost constraints and honest evidence limits. A source link can support an answer, but sending the player away to assemble the answer fails this goal. Asking which game or achievement they mean is appropriate. The debrief includes this review checklist and attempted scenario coverage. Vision testing remains a separate future phase with real gameplay.

## Historical setup verification — October 9, 2026

95 automated tests passed. The revised real-model smoke check completed four two-turn sessions (eight turns) with dummy account records and no runtime errors. Three turns were flagged: two responses over 45 seconds and one unrequested screen/capture discussion. These are review findings, not a claim that the app's conversation quality is finished. Gemma 3 generated the follow-up questions; initial questions came from controlled scenario starters after the first experiment exposed helper-role confusion.

Observed total GPU memory while both engines were running was 5,253 MiB out of 8,192 MiB, with 2,772 MiB free. This establishes that this text-only configuration ran concurrently during the short check, not that every workload or an additional running game will fit. The small model was configured with CPU device and no GPU KV offload. No eight-hour endurance run or live authenticated account test was performed during setup. Both owned engines stopped at the session limit.

The checked run's debrief is `local-data/text-playtests/20261009-181927-881274/debrief.md`. Full questions, answers and timings remain beside it. Real API mode requires a saved token and uses the normal reviewed account adapter; it was not used for this dummy-data check.
