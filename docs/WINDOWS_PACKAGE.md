# Windows alpha — Settings and OCR

Version 0.1.12-alpha adds the Settings menu, model selection and a Qwen/Tesseract
OCR option alongside Gemma vision. The package's top-level README contains the
user setup guide and download links. Models, llama.cpp and Tesseract are separate
installations, not bundled downloads. Python is bundled.

Settings is available beside Collapse in both source and packaged runs. The
selected model, file paths and update preference are saved under the Windows
user's app data. Qwen uses CPU OCR and text-only reasoning; Gemma uses its selected
vision companion for image inference. Only one answer model loads at a time.
Live capture samples every five seconds and requires explicit window approval.

The executable has no developer recording control, OCR readings review window,
training launchers, test runner or private replay tools. Screenshots/OCR crops
stay in RAM. Packaged runs reject the developer `--vision-review` argument.
No model weights, account data, private configuration, logs or recordings ship.

## Clean Windows acceptance

Test with a separate Windows account or VM and no prior app data:

1. Verify the ZIP hash, extract and launch. Cancel setup: no engine/capture starts.
2. Try Qwen setup with its own GGUF and an installed Tesseract folder. No Gemma
   download is required. Confirm English OCR data is required for that choice.
3. Try Gemma setup with its matching companion. Blank companion permits chat
   setup, but image inference needs the matching file.
4. Open Settings, change the model/path after stopping the engine, close/reopen
   Settings and confirm the update controls remain usable. Restart and confirm
   the selected model and paths are retained.
5. Start engine, send a greeting and a wiki question; assess correctness separately
   from whether a response arrived. Select/approve GW2 and test OCR or vision.
6. Minimize/restore the game; Pause must stop capture and clear approval. Confirm
   no screenshots are written. Close the app and check its owned engine exits.
7. Verify recording, developer readings, test buttons and training launchers are
   absent. `--vision-review` must be rejected.
8. Test uninstall choices without deleting source development folders or unrelated
   model/runtime folders. Downloaded models may be stored outside the app folder.

## Setup EXE

Build with an installed [Inno Setup](https://jrsoftware.org/isdl.php) compiler
and the same Python environment used for the portable build.

```powershell
.\.venv\Scripts\python.exe packaging\build_installer.py --iscc "C:\path\to\ISCC.exe"
```

The build puts the installer and SHA-256 file in `local-data/releases`.
Setup installs to `%ProgramFiles%\GW2-VLM-COPILOT` and adds a Start menu shortcut.
Windows Settings provides uninstall. Existing per-user settings and credentials
stay in their established AppData locations.

Test the Setup EXE on a clean Windows VM. Check the shortcut, upgrade in place,
and verify that the model paths survive. Use dummy GGUFs in the installed
`Models` folder to test both uninstall choices. Place another dummy file
outside that folder and confirm it survives either choice.

Automated package checks do not replace real gameplay/GPU testing or acceptance
on another machine. Never start a second engine merely to test installation while
another app/test engine is running. Existing engines must not be reused or stopped.
