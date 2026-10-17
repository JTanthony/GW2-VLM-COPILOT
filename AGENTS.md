# Project instructions

Canonical development repository: this folder (Waypoint). Keep changes here; do not use downloaded release folders as development checkouts.

## Image privacy and vision development

- In the standard Windows app, live captured images stay in RAM. Never persist screenshots or encoded frames in release builds, including on errors or timeouts.
- The standard Windows app has no recording/logging control. Keep the development review module excluded from packaging and reject its command-line option in packaged runs.
- Source development runs may explicitly enable **Record vision (dev)**. This user-authorized exception saves captured PNG frames at up to 2 FPS alongside sanitized questions, answers, model observations, timing and error types. Logs link records to frame files. It collects review data; it does not train model weights.
- Source recordings stop at one hour or 25 GB, whichever comes first. Keep them private and excluded from Git. Screenshots are not redacted.
- Normal source launches also leave review logging disabled. Launching review does not grant capture permission: the user must still select and approve the window.
- The optional `run-gw2-vision-training.cmd` remains a source-only convenience launcher; the normal source GUI's recording control is sufficient. Keep both the review module and launcher out of the Windows package.
- Logs, credentials, account snapshots, downloaded catalogs and model files stay excluded from Git and release assets. Review logs can contain private visible text even after redaction.
- Existing synthetic image fixtures may be used for development checks. They do not authorize persisting live player screenshots.
