# Continuous local vision

Open run-GW2-VLM-COPILOT.cmd. Start engine, then Select window and confirm continuous capture of the exact game/application.

The approved window is captured directly using Windows Graphics Capture at up to 2 FPS, even while other applications have focus or cover it. Minimize the selected window to pause capture; restore it to resume. The model analyzes the newest frame at its own speed; it does not process two images per second. Only the latest frame is retained, so slow inference cannot build a screenshot backlog.

Keep the game restored, then type a question in GW2 VLM COPILOT and Send. Send freezes a frame no older than ten seconds and takes priority over the next background observation. An observation already running must finish first. If no recent frame exists, the chat tells you to restore the game and wait for new frames. Pause stops capture and clears approval. Stopping the engine or closing GW2 VLM COPILOT also stops the feed and waits for active work.

Screenshots and observations stay in memory. No game inputs, microphone access, automatic chat updates, or disk screenshot history are enabled. Borderless/windowed mode is the recommended test mode. Other applications covering the selected window are excluded. There is no desktop-screen fallback. Games that stop rendering while inactive may stop producing frames; GW2 VLM COPILOT reports waiting for frames and preserves actual frame timestamps.

## Source map

- src/waypoint/capture/windows.py: selected-window identity and minimized/visibility checks.
- src/waypoint/capture/graphics.py: exact HWND Windows Graphics Capture session, bounded PNG encoding, freshness and shutdown.
- src/waypoint/capture/feed.py: bounded 2 FPS capture loop and separate serial model analysis.
- src/waypoint/ui/app.py: selection, permission, Pause, Send and visible errors.
- src/waypoint/assistant/local.py: local observation and answer prompts.
- local-data/gui-errors.log: Send failure tracebacks, without screenshot payloads.

## Verification

The local engine returned a real text answer. Unit tests cover window identity/minimize protection, bounded history, feed shutdown, stale-frame refusal and question priority. Actual GW2 continuous capture and gameplay answer quality still need a user test. Capture rate is a target, not a measured gameplay performance guarantee.


## Vision-to-chat handoff

Contextual chat also receives the last completed observation when its source frame is no older than 90 seconds. The prompt includes its age and requires the model to describe dated evidence rather than current health/timers. Explicit screen questions still require a recent frame; a new analysis can take tens of seconds, and its final answer is labeled internally with the actual frame age. Greetings remain text chat.

When no observation is ready, text chat receives app capture state (approval, frame count, ages, analysis state and errors), so it should explain that analysis is pending instead of asking for an already approved window again. Cached evidence older than 90 seconds is excluded.

local-data/vision-status.json is updated approximately once per second by the GUI. It contains state/counts/ages/errors and an update timestamp, without screenshot pixels or observation text. Use it to distinguish capture from model analysis problems; a stopped/stale GUI record is not live evidence. The GUI status shows how old the last analyzed frame is and preserves model errors separately from capture-state messages.

Verification: 32 tests passed. A GUI Send integration check delivered a simulated 35-second-old observation to contextual chat and displayed the answer. This verifies wiring, not actual current GW2 visibility; the first real frame still needs checking after reopening and approving the game window.


## Numeric readings and rechecks

"Check again", "confirm I have", "my gold" and "gold balance" require a recent frame and bypass cached observation reuse. Gold checks request independent currency transcription without sending the player's suggested number to the vision prompt. A deterministic answer uses only gold-labelled visible_text; missing/conflicting readings return uncertainty, not unrelated stats. Numeric personal stats absent from visible_text and invalid GW2 player-level claims are blocked. These checks cannot prove that OCR itself is correct.

The current fast profile caps Gemma's image token budget to physical_batch_size=256 (the runtime reports a normal budget of 1120). The higher-detail profile has now passed a saved-fixture test and is the default: physical batch 1152, logical batch 2048, 24 GPU layers, and up to 1920-pixel-wide capture. The fast 256-image-token profile is preserved in config/inference.12b-fast.local.json. Actual small GW2 currency text remains unverified. Increasing image detail can increase latency and GPU workspace requirements.


The internal `App.view_frame()` development preview (no player toolbar button) shows the actual captured PNG in a scrollable window at its original pixel size. It does not save screenshots or alter the game's inputs. Keep the game restored so there is a recent frame; the caption shows its age. This helps distinguish wrong-window/hidden-wallet capture from model reading errors. Normal captures now preserve up to 1920 pixels of width instead of 1280 in the quality profile.

Higher-detail test: load 8.17 s, greeting 2.02 s, saved-fixture vision 40.34 s, follow-up 5.84 s. All five fields and BLUE-482 matched. This confirms projector compatibility and fixture reading, not the user's actual balance. The preview UI and all 37 tests passed. Raw result: local-data/performance-8192-quality.json.

## Background capture verification

The controlled native-window test (`tools/verify_window_capture.py`) confirmed that a red selected window remained red in captured pixels while a blue foreground window covered it; minimize blocked frame access; restore produced a new green frame. No real game was captured during that test. Unit tests also cover unchanged frame timestamps, clearing the frame when paused, and session shutdown. Actual GW2 background rendering still needs a player test.

Dependency pins are in `requirements.txt`. Install into the project environment with `.venv\Scripts\python.exe -m pip install -r requirements.txt`. The WGC adapter uses the approved HWND, never title matching or monitor capture. Screenshots remain in memory. Public backend documentation: https://github.com/NiiightmareXD/windows-capture/tree/main/windows-capture-python


## Development-only vision review

Standard Windows builds keep captured images in RAM and have no recording control. Packaging excludes the review module; packaged launches reject its development flag.

Source runs can explicitly enable **Record vision (dev)** in the toolbar. Start the engine, select and approve the game window, then play and ask questions. Recording saves captured PNG frames at up to 2 FPS (subject to capture/disk speed) under `local-data/vision-review`, with a JSONL index beside each session's frame folder. It does not start capture or the engine automatically. The optional `run-gw2-vision-training.cmd` enables this same recording mode on source startup.

Frame records carry capture timestamps. Question records link the recent frame at submission; answer/observation records link the actual analyzed frame, including when an earlier observation is reused. A missing frame link is explicitly null rather than claiming visual evidence. Analysis timing and error types are retained. Raw model observations are not proof of screenshot accuracy; reviewers can inspect the linked frames.

Recording is OFF on normal launch. It stops when disabled, on app exit, or after one hour/5 GB of images, whichever comes first. Text log size is capped near 20 MB. Restart recording for a new session. Existing files remain until manually deleted. Saved screenshots can contain private screen information and are not redacted. Credential-like text fields are sanitized and account snapshots excluded. Keep recordings out of Git/releases. This is review-data collection, not automatic model training.

The release privacy rule and source-development exception are maintained in [AGENTS.md](../AGENTS.md).
