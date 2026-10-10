# GW2 VLM COPILOT

Experimental Windows local AI copilot for Guild Wars 2. Ask questions, research the official wiki, optionally connect account progress, or approve continuous local window vision. Free, MIT-licensed project code; community contributions welcome. Not affiliated with or endorsed by ArenaNet or Google.

A portable Windows alpha is available on the [Releases page](https://github.com/JTanthony93/GW2-VLM-COPILOT/releases). Extract the ZIP and open GW2-VLM-COPILOT.exe; Python is bundled. See [Windows package instructions](docs/WINDOWS_PACKAGE.md). Fresh-Windows, GPU and gameplay acceptance remain unverified. Model weights and llama.cpp runtime binaries are downloaded separately. Answers can be incorrect: do not treat generated guides or screen readings as verified facts.

## Start here

## Install the Windows download (NVIDIA GPU)

Python and LM Studio are not required. This alpha downloads the engine and model separately; setup only selects files already on your PC.

1. Extract the entire app ZIP into its own folder. Keep `_internal`, `assets`, and `docs` beside `GW2-VLM-COPILOT.exe`.
2. Download BOTH llama.cpp b11512 Windows CUDA 12.4 ZIPs below. Extract both into the SAME separate engine folder, keeping all DLLs beside `llama-server.exe`. Do not select an executable inside a ZIP. Keep your NVIDIA driver installed and current.

   Server: https://github.com/ggml-org/llama.cpp/releases/download/b11512/llama-b11512-bin-win-cuda-12.4-x64.zip

   Required CUDA libraries: https://github.com/ggml-org/llama.cpp/releases/download/b11512/cudart-llama-bin-win-cuda-12.4-x64.zip

3. Download these two files into a model folder. Allow about 7.2 GB for them. The 12B model handles both chat and vision; the 1B development tester is not needed.

   Model (`gemma-4-12B-it-QAT-Q4_0.gguf`): https://huggingface.co/lmstudio-community/gemma-4-12B-it-QAT-GGUF/resolve/main/gemma-4-12B-it-QAT-Q4_0.gguf?download=true

   Matching projector (`mmproj-gemma-4-12B-it-QAT-BF16.gguf`): https://huggingface.co/lmstudio-community/gemma-4-12B-it-QAT-GGUF/resolve/main/mmproj-gemma-4-12B-it-QAT-BF16.gguf?download=true

4. Open `GW2-VLM-COPILOT.exe`. In setup, Browse to the extracted `llama-server.exe`, the model, and its matching projector. Click **Save and open app**, then **Start engine**. Close other copilot engines first to free the GPU and port.
5. Try ordinary chat first. For vision, click **Select window**, choose GW2, and approve capture. Keep the game restored; minimizing pauses capture.

This download recipe targets Windows x64 with an NVIDIA GPU. Hardware affects loading and response speed; other GPU backends require a compatible llama.cpp build and have not been validated here. If the engine exits, check `%LOCALAPPDATA%\GW2 VLM COPILOT\local-data\engine.log`. To change files later, launch `GW2-VLM-COPILOT.exe --setup`.

URLs are written out so they can be copied from Notepad. More details and the clean-Windows checklist are in `docs/WINDOWS_PACKAGE.md`.

## Project documentation

- [Windows setup](docs/SETUP.md)
- [Development, testing and optional fine-tuning](docs/DEVELOPMENT.md)
- [Privacy and contribution safety](docs/PRIVACY.md)
- [Third-party notices](docs/THIRD_PARTY.md)

Gemma 4 12B handles answers and vision through a loopback llama.cpp server. Optional Gemma 3 1B generates GW2 player questions in the text tester. Neither model learns automatically from use. Improvements require deliberate testing and reviewed changes to the app, prompts, or training data. A more capable AI model can assist with that process. Wiki research sends generated public game search terms online; optional account connection calls the official GW2 API. Inference stays local.

## Current limitations

- Windows only; manual runtime/model setup and hardware tuning.
- GW2-focused release. Other adapter scaffolding in source does not establish supported titles.
- Account progress is a dated snapshot, refreshed through Accounts; only an API completion flag confirms completion.
- Captures require explicit approval. Keep the selected game restored; minimizing pauses capture. Frames are sampled at up to 2 FPS, while model analysis is slower and hardware-dependent.
- Text testing does not establish live gameplay accuracy. Earlier development samples averaged about 26 seconds per answer, approximately 48 seconds for GW2; not a benchmark guarantee for this release.
- No game inputs or microphone listening. No automatic chat coaching. No production installer, automatic updater or validated fine-tuning pipeline yet.

## License

[MIT](LICENSE) covers project code. Dependencies, model weights, retrieved wiki content and third-party materials retain their own terms. Do not bundle your credentials, account data, model files or local logs in contributions.
