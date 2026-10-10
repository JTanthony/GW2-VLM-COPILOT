# Windows portable alpha

Designed for Gemma 4 12B QAT Q4_0. Other llama.cpp-compatible GGUF models may be used; vision requires a compatible model and matching projector. Alternative models are not yet validated. Model weights are downloaded separately, not built into this alpha.

Extract the entire ZIP into a writable folder (for example Downloads or Documents), then open GW2-VLM-COPILOT.exe. Keep the _internal and assets folders beside the executable. Python does not need to be installed. This is an unsigned experimental application, not a signed installer.

The included Models folder is empty. Put your downloaded model, matching vision companion and extracted llama.cpp server folder there. See the top-level README for download links and CUDA DLL instructions. No model weights or engine binaries are bundled.

First launch opens local setup. Download a Windows llama.cpp server and required matching DLLs from https://github.com/ggml-org/llama.cpp/releases/tag/b11512, and separately obtain your Gemma 4 12B GGUF and matching vision projector. Select those local files and save. The app does not silently download or execute files in setup. Click Start engine only when ready. Model/runtime files are not included; NVIDIA drivers and appropriate GPU memory are still required. Leaving the projector blank enables text-only configuration.

Packaged settings, logs and project resources live in %LOCALAPPDATA%/GW2 VLM COPILOT. Saved account keys currently retain the existing %LOCALAPPDATA%/Waypoint/credentials location and Windows user protection. No private state ships in the ZIP. To reconfigure, run GW2-VLM-COPILOT.exe --setup.

## Clean Windows acceptance checklist

Use a new Windows account or VM with no Python, models or prior app data:
1. Verify the ZIP hash, extract it, and launch setup. Cancel: app should exit without inference/capture or configuration.
2. Relaunch, select verified server/model/projector files, save, and check the app title/icons/chat labels.
3. Start engine, send an ordinary greeting, and ask a named GW2 wiki question. Check evidence correctness, not just whether a reply arrives.
4. Optionally connect a newly created GW2 key in Accounts; verify reconnect, refresh and forget. Never include the key in a test report.
5. With the game restored, explicitly approve capture; test Pause and minimize/restore. Confirm no capture occurs before approval.
6. Close the app and verify its engine exits. Relaunch and ensure settings persist. Move the extracted folder and confirm no build-machine paths are needed.

--check-package checks bundled imports, UI assets and a synthetic Windows-protection round trip, writing package-check.json to per-user app data. --smoke opens/closes the UI without loading a model or capturing. These checks are not substitutes for clean-Windows and real GPU/game acceptance.

Build contributors: install requirements.txt and PyInstaller 6.22.3 in a dedicated build environment, then run python packaging/build_windows.py. Output goes to ignored local-data/releases. Do not copy development .local.json files, model weights or account stores into the package.
