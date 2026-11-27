# GW2 VLM COPILOT — Windows alpha

Local Guild Wars 2 chat, official-wiki research, optional account progress and
user-approved screen assistance. Answers can be wrong. OCR/vision are experimental.

## Start here

1. Run the Setup EXE, approve the Windows administrator prompt, and open
   **GW2 VLM COPILOT** from Start. For the portable ZIP, extract everything
   and open `GW2-VLM-COPILOT.exe` in the extracted folder. Python is bundled.
2. In first-time Setup choose **4B Qwen (OCR)** or **12B Gemma QAT (vision)**.
   On **Downloads**, select the server, NVIDIA DLLs and desired model files,
   then click **Download selected**. Each row shows download, verification and
   extraction progress. Cancelled downloads can resume on another attempt.
3. Automatic downloads use `%LOCALAPPDATA%\GW2 VLM COPILOT\runtime\llama-b12387`
   for the server/DLLs and `%LOCALAPPDATA%\GW2 VLM COPILOT\Models` for model files.
   In source development, those folders are under the source project.
   The included server downloads target NVIDIA GPUs. Other compatible servers
   and existing models can be selected in **File locations**.
4. Completed downloads fill the matching file paths automatically. Qwen also
   needs a separate [Tesseract OCR installation](https://github.com/UB-Mannheim/tesseract/wiki)
   with English data. Choose that installation folder in **File locations**.
   Click **Save and open app**.
5. Click **Start engine**. Try ordinary chat first. For screen help, select
   the game window and approve capture. Keep it restored; minimizing pauses it.

## Model choices

- **Qwen 3.5 4B Q4_K_M:** uses local Tesseract OCR text instead of image
  inference. Download `Qwen3.5-4B-Q4_K_M.gguf` from the
  [Qwen GGUF model page](https://huggingface.co/unsloth/Qwen3.5-4B-GGUF/tree/main).
  Install [Tesseract OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
  with English data. Choose its installation folder containing `tesseract.exe`
  and `tessdata/eng.traineddata`. No vision projector is needed for this mode.
- **Gemma 4 12B QAT Q4_0:** uses a matching companion for image vision.
  Download `gemma-4-12B-it-QAT-Q4_0.gguf` and
  `mmproj-gemma-4-12B-it-QAT-BF16.gguf` from the
  [Gemma GGUF model page](https://huggingface.co/lmstudio-community/gemma-4-12B-it-QAT-GGUF/tree/main).
  The companion is optional for ordinary chat and required for image vision.

Only one answer model loads at a time. Hardware and the running game affect
memory use and speed. A compatible llama.cpp version must support your model.

## Settings

The gear beside Collapse opens **Settings**. Stop the engine before switching
models. **Load model** selects a GGUF. **Vision companion** selects Gemma's
matching projector. Qwen enables **Download Tesseract OCR** and **Choose OCR
folder**. Your selected model and paths are remembered locally.

Update controls are at the bottom of Settings. Checks include prereleases;
updates open the release page for a manual download. Nothing is installed
silently. Nearby achievement hints can be switched off in Settings.

## Privacy and capture

Capture samples once every five seconds. Normal images and OCR crops stay in
RAM; this Windows app has no screenshot recording control. OCR can misread text;
it does not prove location, item ownership or completed achievements. Research
uses the existing approved public sources. No microphone or game inputs.

Optional API tokens belong in **Accounts**, never chat. Saved tokens use Windows
user protection. App settings and resources are under
`%LOCALAPPDATA%/GW2 VLM COPILOT/`; saved credentials retain the existing
`%LOCALAPPDATA%/Waypoint/credentials/` location. No personal data ships in the ZIP.

Close other copilot engines before starting. If needed, open
`GW2-VLM-COPILOT.exe --setup` to reconfigure.

For an installed copy, use **Settings → Apps → Installed apps → GW2 VLM
COPILOT → Uninstall**. You can preview and delete GGUF files in the app's
`Models` folders and server/DLL files in its runtime folders during uninstall,
including the current Windows user's automatically downloaded resources.
Keeping them is the default. Saved user data and separately stored models and
runtimes stay in place. For a portable copy, use the supplied `Uninstall.cmd`.

The Windows alpha is unsigned. Not affiliated with
ArenaNet, Google or Qwen. Project code is MIT; separately obtained models,
runtimes and other third-party materials retain their own terms.
