# Windows source setup

Use 64-bit Windows and Python 3.12 with tkinter (included in the normal python.org Windows installer). An NVIDIA CUDA-compatible GPU is the development target. The app was developed on an 8 GB RTX 3060 Ti with partial offload; expect slow responses. VRAM requirements depend on context, image size and offload. Close competing model servers before launch.

## Install Python dependencies

Download or clone this repository, open PowerShell in its root, then run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item config/inference.example.json config/inference.local.json
```

## Install the engine and model

Download Windows llama.cpp server binaries from the [official releases](https://github.com/ggml-org/llama.cpp/releases). Development used [b11512](https://github.com/ggml-org/llama.cpp/releases/tag/b11512), Windows CUDA 12.4. Download the server archive and any matching CUDA dependency archive required by that release. Verify published checksums when available. Keep required DLLs with llama-server.exe under runtime/llama-b11512, or change executable in your local config. Newer releases may change flags; this project does not promise compatibility with every version.

Separately obtain a Gemma 4 12B instruction-tuned QAT GGUF and its matching multimodal projector through [Google's Gemma documentation](https://ai.google.dev/gemma/docs/core). Development used gemma-4-12B-it-QAT-Q4_0.gguf and mmproj-gemma-4-12B-it-QAT-BF16.gguf. Review the model's own license. Never pair an unrelated projector with the model.

Edit config/inference.local.json: set model_path and projector_path to the downloaded files and executable to your server. Paths in the example are placeholders. Start with the example's conservative context; lower context/batches or GPU offload if memory is exhausted. For text-only use, omit projector_path; vision then requires adding it back. Keep port 17865 free. Neither the app nor setup commands download models automatically.

## Launch

Double-click run-waypoint.cmd, or run:

```powershell
.\.venv\Scripts\python.exe tools/run_gui.py
```

Click Start engine. Ordinary chat does not require capture. For vision, Select window and explicitly approve capture. Pause revokes capture approval. Close with the app's close button so owned work and the server can shut down.

Accounts is optional: create an official GW2 key with account and progression permissions and enter it only in Accounts, not chat. A successful connection saves it with Windows user protection. Leave the field blank to reconnect; Refresh retrieves a new snapshot, and Forget saved token removes it.

## Checks and troubleshooting

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -q
.\.venv\Scripts\python.exe tools/run_gui.py --smoke
```

Smoke opens and closes the UI without starting inference or capture. An occupied port means another engine is active; close it normally rather than trying to reuse it. Check local-data/engine.log privately for missing models, DLLs, unsupported flags or memory errors. Never upload raw logs containing user data.

Optional saved-image inference check (starts the local model, not live capture):

```powershell
.\.venv\Scripts\python.exe tools/test_inference.py
```

Inspect local-data/inference-test.json, including accuracy_passed: transport success alone does not mean the fixture was read correctly. A clean-machine installation has not yet been validated; report reproducible issues without keys or personal data.
