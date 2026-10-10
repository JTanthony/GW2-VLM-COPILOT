# Local 4096-token request budget update

Development folder: C:\Users\jthom\Documents\Codex\Waypoint

Text requests now use the local llama.cpp /apply-template and /tokenize endpoints before inference. The app reserves the requested answer length plus 128 tokens of margin within 4096. Oversized requests reduce previous dialogue and select relevant whole wiki passages, then count again. Current questions and system instructions are retained. Shortened evidence is marked partial. Requests still too large are stopped with a useful error. Image requests retain their existing path; this update does not measure image tokens.

This is application code improvement, not model fine-tuning. No context increase, model download, capture or account change is required.

## Upload source yourself with GitHub Desktop

Add the existing repository at the development folder above. Review and select ONLY these four files:

- src/waypoint/inference/budget.py
- src/waypoint/inference/client.py
- tests/test_inference.py
- docs/CONTEXT_BUDGET_UPDATE.md

Commit with the summary "Budget text requests within 4096 tokens", then click Push origin. Do not select local-data, configuration containing local paths, logs, account data, credentials or model files. The repository ignore rules remain in place.

Pushing source does not update the downloadable executable. After a real local-engine test succeeds, rebuild with .venv\Scripts\python.exe packaging/build_windows.py using a new release version, then upload the new ZIP and checksum to a GitHub pre-release. Do not replace a previous release ZIP silently.

## Acceptance before release

Start one engine and ask the Wyvern Matriarch location question. Repeat after a long conversation and with wiki references. Confirm correct evidence, no HTTP 400, and acceptable timing. Test both an ordinary greeting and a request that remains too large. Automated mocks cover the budget flow; they do not establish live answer quality or endpoint compatibility for every llama.cpp build.
