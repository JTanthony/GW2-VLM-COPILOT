# Development, testing and optional training

## What this repository actually does

The test runner generates questions and records answers. It does not update model weights. Prompts, resource memory, wiki retrieval, API context and code changes can improve answers without training. More play time or questions do not teach either model automatically.

Gemma 3 1B is the simulated player; Gemma 4 12B is the copilot. The current batch is GW2 only and the 12B research planner is restricted to wiki.guildwars2.com. Retrieved plain-text evidence goes into the answer prompt; completion-only questions may be answered directly from an API record. Wiki requests are bounded and read-only, and may fail or retrieve incomplete evidence.

Download [Gemma 3 1B IT Q4_K_M (GGUF)](https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf?download=true) from the [llama.cpp organization model page](https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF). Save `gemma-3-1b-it-Q4_K_M.gguf` in your local model folder, then select it in tester setup. This is the text-only simulated player; no projector is required. Review the model license on the download page. Do not commit the downloaded weights.

On first launch, `run-gw2-wiki-for-training.cmd` opens the tester setup window if `config/player.local.json` is missing. Browse to your downloaded `llama-server.exe` and Gemma 3 1B IT Q4_K_M GGUF, then click **Save and start tests**. The window saves the CPU settings and port 17866 automatically; closing it cancels without starting engines. Complete the app launcher setup first for Python dependencies and the answering model. The default saved-account batch also requires a prior successful GW2 Accounts connection. Model files must be downloaded separately. Existing player configuration is preserved.

## Run a short text batch

Obtain Gemma 3 1B IT Q4_K_M separately, copy config/player.example.json to config/player.local.json and set its model path. The tester uses CPU-only 1B at port 17866 and the configured 12B at port 17865, without the visual projector. Close the GUI engine first.

```powershell
Copy-Item config/player.example.json config/player.local.json
.\.venv\Scripts\python.exe tools/run_text_sessions.py --sessions 4 --turns 4 --hours 0.2 --account-mode dummy
```

Dummy records are synthetic, not real GW2 achievements; do not judge invented dummy-name mechanics as real guides. Saved mode uses your previously connected GW2 account and creates private snapshot-derived logs. `run-gw2-wiki-for-training.cmd` uses saved mode for Guild Wars 2 with five turns per session, up to 1,000 sessions or three hours, whichever comes first. The launcher name refers to preparing and reviewing test material; it does not train model weights. stop-gw2-wiki-for-training.cmd requests a stop between inferences; wait for both engines before restarting.

Local reports are under local-data/text-playtests. seconds measures the copilot answer; player_seconds measures question preparation; total_seconds measures the full successful turn, excluding the configured inter-turn delay. Flags are review suggestions, not correctness scores.

## Improve 1B question quality without fine-tuning

Edit PLAYER_GUIDANCE and scenarios in src/waypoint/testing/text_sessions.py and mmo_scenarios.json. Cover solo/group prerequisites, multi-step achievements, short sessions, missed steps, ambiguous names and follow-ups. Review generated questions for invented places, repeated questions and assistant-role confusion. Keep realistic difficult questions; do not reward only easy cases. Compare a fixed set of inputs before and after changes.

## Improve 12B answers without fine-tuning

Inspect assistant/research.py, web_lookup.py, local.py and inference/client.py. Determine whether failure comes from an incorrect question, poor lookup query, incomplete evidence, wrong API interpretation or generated hallucination. Keep public game knowledge separate from private account facts. A high progress counter does not prove completion or that a task is easy.

Create a reviewed evaluation set with public questions, expected facts, dated source URLs and answer criteria. Include unavailable-evidence and misleading-premise cases. Measure grounded next actions, unsupported facts, clarification quality, completion correctness, median/p95 latency and errors. Use the same inputs, model/settings and evidence for comparisons. Keep evaluation examples out of any training set.

## Actual fine-tuning: optional contributor initiative

No trainer or validated recipe is shipped. Begin with [Google's tuning guidance](https://ai.google.dev/gemma/docs/tune) and [LoRA example](https://ai.google.dev/gemma/docs/lora_tuning). Confirm framework support for the exact Gemma generation/checkpoint. Do not assume a tutorial for an older Gemma applies unchanged to Gemma 4 12B. Training needs substantially more memory than inference; an 8 GB inference setup is not evidence it can train 12B.

1. Collect and manually review a small dataset. Strip tokens, names, account IDs, private chat and personal snapshots. Obtain permission for contributed data. Record source rights; do not indiscriminately scrape the wiki into training data.
2. For 1B, use scenario + latest answer + follow-up intent as input and a human-reviewed player question as target. Preserve its JSON question format, human-player role and privacy boundaries.
3. For 12B, use question + public wiki evidence + synthetic account context as input and a verified, useful answer as target. Include clarifying questions and explicit unknowns. Train grounded behavior rather than memorizing changing event schedules or account facts. Text-only training does not validate vision.
4. Split by task/achievement and conversation, not random neighboring turns, into train/validation/held-out test sets. Avoid leakage from duplicated evidence or answers.
5. Use a compatible trainable checkpoint and the model's chat template. Configure LoRA or supported QLoRA in a separate training environment; begin with short context and a small batch. Record model revision, library versions, seed, optimizer, learning rate, adapter targets and dataset revision. GGUF files in this app are inference artifacts, not a supplied training pipeline.
6. Compare the trained adapter against the unchanged base on the held-out set. Reject regressions in factuality, completion handling, privacy or latency. Do not use unreviewed 1B/12B outputs as correct labels.
7. Export/merge and convert only through tools compatible with the exact model and llama.cpp. Verify the final quantized artifact, then update local config paths. Re-run structured JSON and multi-turn tests. If vision is retained, verify model/projector compatibility and test real images separately.
8. Publish adapter/model/dataset provenance and compatible licenses separately; never commit weights or private data here. Clearly label reported results as measured, not simulated.

Contributions should state the problem, evidence, exact change and checks. Do not claim training, accuracy gains or speed gains without the corresponding measured experiment.
