# GW2 VLM COPILOT

Experimental Windows local AI copilot for Guild Wars 2. Ask questions, research the official wiki, optionally connect account progress, or approve continuous local window vision. Free, MIT-licensed project code; community contributions welcome. Not affiliated with or endorsed by ArenaNet or Google.

A portable Windows alpha is available on the [Releases page](https://github.com/JTanthony93/GW2-VLM-COPILOT/releases). Extract the ZIP and open GW2-VLM-COPILOT.exe; Python is bundled. See [Windows package instructions](docs/WINDOWS_PACKAGE.md). Fresh-Windows, gameplay quality remain unverified. Model weights and llama.cpp runtime binaries are downloaded separately. Answers can be incorrect: do not treat generated guides or screen readings as verified facts.

## Install the Windows download (NVIDIA GPU)

Python and LM Studio are not required. Download the engine and model separately; setup only selects files already on your PC.

Designed for **Gemma 4 12B QAT Q4_0**, the recommended model for chat and vision. Other llama.cpp-compatible GGUF models may be used; vision requires a compatible model and matching projector. Alternative models are not yet validated. Model weights are not bundled in this alpha.

1. Extract the entire app ZIP into its own folder. Keep `_internal`, `assets`, and `docs` beside `GW2-VLM-COPILOT.exe`. The included `Models` folder is where you put your model and engine downloads; no model weights are bundled.

2. Download BOTH ZIPs below. 

Server: [https://github.com/ggml-org/llama.cpp/releases/download/b11512/llama-b11512-bin-win-cuda-12.4-x64.zip](https://github.com/ggml-org/llama.cpp/releases/download/b11512/llama-b11512-bin-win-cuda-12.4-x64.zip)

Extract the server ZIP, then place its extracted `llama-b11512-bin-win-cuda-12.4-x64` folder inside the app's `Models` folder.

Required CUDA libraries: [https://github.com/ggml-org/llama.cpp/releases/download/b11512/cudart-llama-bin-win-cuda-12.4-x64.zip](https://github.com/ggml-org/llama.cpp/releases/download/b11512/cudart-llama-bin-win-cuda-12.4-x64.zip)

Extract the CUDA libraries. Copy the three files (`cublas64_12.dll`, `cublasLt64_12.dll`, and `cudart64_12.dll`) into the  extracted `llama-b11512-bin-win-cuda-12.4-x64` server folder.

Keep your NVIDIA driver installed and current.

4. Download these two files directly into the app's `Models` folder. Allow about 7.2 GB for them. The 12B model handles both chat and vision; its projector is the companion file that lets it read images, not a second chat model. The optional Gemma 3 1B development tester is not needed to use the app. If you want to help improve the project through testing, see [the development notes](docs/DEVELOPMENT.md).

   Model (`gemma-4-12B-it-QAT-Q4_0.gguf`): [https://huggingface.co/lmstudio-community/gemma-4-12B-it-QAT-GGUF/resolve/main/gemma-4-12B-it-QAT-Q4_0.gguf?download=true](https://huggingface.co/lmstudio-community/gemma-4-12B-it-QAT-GGUF/resolve/main/gemma-4-12B-it-QAT-Q4_0.gguf?download=true)

   Matching projector (`mmproj-gemma-4-12B-it-QAT-BF16.gguf`): [https://huggingface.co/lmstudio-community/gemma-4-12B-it-QAT-GGUF/resolve/main/mmproj-gemma-4-12B-it-QAT-BF16.gguf?download=true](https://huggingface.co/lmstudio-community/gemma-4-12B-it-QAT-GGUF/resolve/main/mmproj-gemma-4-12B-it-QAT-BF16.gguf?download=true)

5. Open `GW2-VLM-COPILOT.exe`. In setup, Browse to the extracted `llama-server.exe`, the model, and its matching projector. Click **Save and open app**, then **Start engine**. Close other copilot engines first to free the GPU and port.

6. Try ordinary chat first. For vision, click **Select window**, choose GW2, and approve capture. Keep the game restored; minimizing pauses capture.

This download recipe targets Windows x64 with an NVIDIA GPU. Hardware affects loading and response speed; other GPU backends require a compatible llama.cpp build and have not been validated here. If the engine exits, check `%LOCALAPPDATA%\GW2 VLM COPILOT\local-data\engine.log`. To change files later, launch `GW2-VLM-COPILOT.exe --setup`.

URLs are written out so they can be copied from Notepad. More details and the clean-Windows checklist are in `docs/WINDOWS_PACKAGE.md`.

## Running from source

Install 64-bit Python 3.12 with the Python launcher and Tcl/Tk. If you already have the Python install manager, open PowerShell and run:

py install 3.12

Alternatively, download Python 3.12 from python.org.
Extract the entire project ZIP, then double-click run-GW2-VLM-COPILOT.cmd. Choose Y to create the local Python environment and install dependencies. This step requires internet access.
The setup window then lets you select your downloaded llama server, answering model, and matching vision projector. Models and llama.cpp are downloaded separately.

## Optional developer tester: Gemma 3 1B

The tester uses Gemma 3 1B to generate player questions and the app’s configured model to answer them. Regular app users do not need the 1B model.

1. Download [Gemma 3 1B IT Q4_K_M.gguf](https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf?download=true) and save it in your local model folder. Review the license on the model page.

2. Complete the app setup above, then close the app and let its engine stop.

3. Run run-gw2-wiki-for-training.cmd.

4. On first launch, select your llama-server.exe and downloaded 1B model, then click Save and start tests. The tester saves its configuration automatically.

No vision projector is needed for the 1B tester. The `run-gw2-wiki-for-training` trainer requires a previously saved GW2 account connection. The `run-gw2-wiki-no-account` is recommended to help support new player base. It runs up to three hours, five turns per session, or 1,000 sessions—whichever limit comes first.

Run stop-gw2-wiki-for-training.cmd to stop. Active inference finishes before the engines close.

Results stay in `local-data/text-playtests`. Keep account-derived logs private. These runs generate material for review; they do not automatically train either model. 

Vision training is an optional development tool reserved only in the source file launcher. Recordings stay in `local-data/vision-review` and stop after 1 hour minutes or 5 GB. It is disabled by default in the standard Windows release and data is only stored in ram.

Once logged an enterprise model such as GPT SOL 6.1 will provide stronger python training rules. Once complete push to upload.

## Project documentation

##### Uninstall the portable app

Close the app and let its engine stop, then double-click `Uninstall.cmd` in the extracted app folder and type `UNINSTALL` to confirm. It removes only packaged app files listed in the manifest. Downloaded models, engine files and saved user data are preserved. A folder installed under Program Files may require running Uninstall as administrator. This portable release does not register itself in Windows Installed apps.

To remove personal data too, delete `%LOCALAPPDATA%\GW2 VLM COPILOT` in Explorer. Protected API tokens are stored separately in `%LOCALAPPDATA%\Waypoint\credentials`; that location may also be used by your development copy, so retain it if you still need those connections. No uninstaller changes that shared token store automatically.

##### More documentation

* [Windows setup](docs/SETUP.md)
* [Development, testing and optional fine-tuning](docs/DEVELOPMENT.md)
* [Privacy and contribution safety](docs/PRIVACY.md)
* [Third-party notices](docs/THIRD_PARTY.md)

Gemma 4 12B handles answers and vision through a loopback llama.cpp server. Optional Gemma 3 1B generates GW2 player questions in the text tester. Neither model learns automatically from use. Improvements require deliberate testing and reviewed changes to the app, prompts, or training data. A more capable AI model can assist with that process. Wiki research sends generated public game search terms online; optional account connection calls the official GW2 API. Inference stays local.

##### Current limitations

* Windows only; manual runtime/model setup and hardware tuning.
* GW2-focused release. Other adapter scaffolding in source does not establish supported titles.
* Account progress is a dated snapshot, refreshed through Accounts; only an API completion flag confirms completion.
* Captures require explicit approval. Keep the selected game restored; minimizing pauses capture. Frames are sampled at up to 2 FPS, while model analysis is slower and hardware-dependent.
* Text testing does not establish live gameplay accuracy. Earlier development samples averaged about 26 seconds per answer, approximately 48 seconds for GW2; not a benchmark guarantee for this release.
* No game inputs or microphone listening. No automatic chat coaching. No production installer, automatic updater or validated fine-tuning pipeline yet.

##### License

[MIT](LICENSE) covers project code. Dependencies, model weights, retrieved wiki content and third-party materials retain their own terms. Do not bundle your credentials, account data, model files or local logs in contributions.
