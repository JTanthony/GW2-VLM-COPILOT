# Experimental OCR and Qwen mode

This feature reads text from an approved game window with Tesseract
and can send that text to a local Qwen 3.5 4B model for reasoning. Gemma 4 12B QAT
remains the image-vision option. This is application testing and prompt/evidence
improvement, not model weight training. Starting with Windows 0.1.12-alpha, the
OCR runtime and Settings are included in the executable. Developer recording,
readings review windows, training adapters and private replay tools stay excluded.

## Setup

1. Follow [source setup](SETUP.md) to install Python dependencies and configure
   `config/inference.local.json` with your local llama.cpp server. Keep this
   private configuration out of Git. No model or installer is bundled.
2. Install Tesseract with English language data. The [official installation
   guide](https://tesseract-ocr.github.io/tessdoc/Installation.html#windows)
   links the Windows installers maintained by UB Mannheim.
3. Download a llama.cpp-compatible Qwen 3.5 4B Q4_K_M GGUF from a trusted model
   distributor. Keep model files outside Git; `local-data/models/` is ignored.
   The runtime must support the chosen model architecture.
4. Open `run-GW2-VLM-COPILOT.cmd`. Click Settings (the gear between Collapse
   and Close), then select **4B Qwen**. The checkboxes allow one model at a time.
5. Click **Load model...** and choose your Qwen GGUF. **Download Tesseract OCR**
   opens the installer page in your browser. **Choose OCR folder...** selects
   the installed folder containing `tesseract.exe` and `tessdata/eng.traineddata`.
6. Click **Start engine**, then select and approve the game window. Settings
   alone does not start capture. Open **Readings** to inspect extracted text.

Stop the engine before changing models or paths. Choose **12B Gemma QAT** to
return to image vision; its matching projector remains configured in the
original inference profile. OCR setup is greyed out for Gemma. File paths are
remembered locally, including the selected model. Capture remains off until
you explicitly start the engine and approve a window.

## Behavior and limits

- Four overlapping regions cover the approved window. Chat and the skill bar
  are masked in the OCR copy using percentage coordinates in `reader.py`.
  Different UI layouts may need adjustments; these masks do not identify chat
  automatically. Capture samples once every five seconds; OCR runs a pass then waits
  five seconds, rather than processing every captured frame.
- Tesseract uses CPU processing and memory pipes. Normal frames and crops stay
  in RAM. The separate, explicitly enabled **Record vision (dev)** control saves
  original unredacted frames under the existing one-hour/25-GB limits.
- Low confidence, small text, moving backgrounds and split names can cause
  mistakes. OCR text does not prove location, icon meaning, story entry,
  inventory ownership or achievement completion. Qwen receives bounded text,
  never images. Enabling OCR does not itself reduce loaded model weights.
- Nearby hints are a small curated experiment, not coverage of every
  achievement. A hint requires repeated fresh matching OCR, an explicit
  unfinished achievement record in a recent account snapshot, and model
  verification. At most one hint is sent per capture session. Completed,
  missing, stale or disconnected account records suppress hints. There is no
  combat coaching or other-map reminder system.
- No game inputs, microphone listening or commands from recognized screen text
  are enabled. Wiki lookup uses the existing approved public-source rules.

## Source text testing

The optional `run-qwen-gw2-wiki-for-training-no-account.cmd` uses Gemma 3 1B as
simulated player and Qwen as answer model. Follow [development setup](DEVELOPMENT.md)
for the 1B model and `config/player.local.json`. The tester's default Qwen file is
`local-data/models/qwen3.5-4b/Qwen3.5-4B-Q4_K_M.gguf`; the app's model picker does
not change this tester path. Close the app and let its engine stop first. Run only one text tester at a time;
Gemma and Qwen testers share the same 1B player port (17866).

The tester requires the local inference configuration for server settings but
does not load Gemma 12B. It refuses occupied app/test ports, checks wiki
availability before loading models, and performs bounded recovery checks after
three consecutive wiki retrieval failures. Default limits are eight hours, 1,000 sessions and five
turns per session. Use `stop-qwen-gw2-wiki-for-training-no-account.cmd` to stop
after active inference finishes. This tester never starts capture or loads
account credentials. Reports stay private under `local-data/text-playtests-qwen/`.

Run regression checks from the repository root:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_*.py'
```

Tests use synthetic data and mocked engines; passing them does not establish
real-game accuracy, VRAM savings or a performance guarantee. Gameplay and clean
machine testing are still needed before including OCR in a Windows release.

Production code now lives in `src/waypoint/ocr/`; source experiment imports
remain compatibility aliases. Packaged first-run setup can select Qwen directly.
Developer recording and readings-review controls are not shipped.
