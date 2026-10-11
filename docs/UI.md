# GW2 VLM COPILOT GUI

The canonical GUI is now in `src/waypoint/ui/app.py`. Colors/fonts are in `theme.py`; the scrollbar and opacity slider are in `widgets.py`; preferences are in `src/waypoint/storage/preferences.py`. Edit these files in place rather than making alternate GUI versions.

Double-click `run-GW2-VLM-COPILOT.cmd` in the source project folder. The downloadable Windows package launches through `GW2-VLM-COPILOT.exe`. Branding lives in `assets/branding`; the sword images are `gw2-vlm-copilot-24.png` and `gw2-vlm-copilot-32.png`, and `gw2-vlm-copilot.ico` supplies the Windows icon. Internal `waypoint` Python package names remain unchanged. Install the source dependencies as described in [setup](SETUP.md).

1. Click Start engine and wait for Local engine ready.
2. For screen questions, click Select window, choose the game/application, and confirm permission. See [capture steps](CAPTURE.md).
3. Type a question, then press Send or Enter. Shift+Enter inserts a newline.
4. Stop engine unloads the owned llama.cpp process. Closing the window also waits for active local work, then shuts down the engine.

Keep: A−/A+ text sizing, manual resize corner, header dragging, collapse/expand, always-on-top, opacity, chat draft and answer display. Removed: Voice, Small/Tall/Long presets, Codex relay controls and account usage footer. The footer says Local inference. Escape folds the window; there is no global hotkey yet.

Start/stop and inference run off the UI thread. Cancel discards the pending answer and skips any remaining follow-up step; an HTTP request already running completes or times out before cancellation finishes. It is not immediate server cancellation. Closing while loading also waits for completion/failure before shutting down the owned engine.

Preferences save font size and opacity in `local-data/ui-settings.json` under the data root. Source runs use the project folder; packaged runs use `%LOCALAPPDATA%\GW2 VLM COPILOT`. Packaged configuration, logs and project resources also stay under that per-user data root. Saved account tokens use Windows user protection in the existing `%LOCALAPPDATA%\Waypoint\credentials` directory. Normal app launches do not persist chat text. Source development has an opt-in **Record vision (dev)** control for frames and diagnostics; the Windows app has no recording control. See [vision review](CAPTURE.md#development-only-vision-review).

The image picker is removed. Without a selected window, Send provides local text answers. With an approved restored window, continuous capture collects recent frames even while other applications have focus; Send uses a recent frame before answering. Pause clears approval. Conversation history stays in memory for the last three turns. Saved-image tests remain available through tools/test_inference.py. Automatic chat updates, paid entitlements, signed installer, and production update handling remain future work. There are no Codex requests, microphone controls, or game inputs in this GUI.

Game wiki references are retrieved automatically when useful; there are no lookup controls. See [online lookup](ONLINE_LOOKUP.md).

## Product wording and model voice

`src/waypoint/branding.py` is the single home for the owner-approved welcome and copilot voice. The UI displays WELCOME verbatim; the model does not generate or rewrite that message. Both text and screen answers use COPILOT_VOICE, replacing generic companion introductions and rigid brief-answer wording. Edit this file to change product copy or voice. Technical prompts still describe actual capabilities and evidence; they should not introduce competing slogans or repeat launch instructions in normal conversation.

The View frame diagnostic button is removed from the player toolbar. The internal preview method remains available for development.
