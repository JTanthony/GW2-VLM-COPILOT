# v0.1.12-alpha — Settings and OCR

- Settings beside Collapse, with model loading, model choices and GPU guidance.
- Qwen 3.5 4B with local Tesseract OCR, alongside Gemma 4 12B QAT image vision.
- First-time setup supports either mode. Qwen does not require a Gemma download;
  Gemma's matching vision companion is selected for image inference.
- Model choice and paths are remembered per Windows user. One answer model loads
  at a time; stop the engine before changing models.
- Update preference/check button moved to Settings, with transient status text.
  Update discovery now targets the repository configured for this project.
- Five-second capture cadence, updated freshness checks and current welcome copy.
- Shared wiki evidence improvements for equipment, crafting, collection counters,
  map objectives/access and mastery progression. Answers still require checking.
- Windows build excludes developer recording, readings-review controls, training
  runners, experiment diagnostics and private data. Images/OCR crops stay in RAM.

The portable ZIP includes Python and an empty Models folder. llama.cpp, model
weights and Tesseract are separately obtained; the README contains setup links.

Validation: 299 source tests passed. The executable passed import/module-exclusion
checks, Settings/model-switch smoke checks and rejection of the recording option
before setup. The extracted ZIP also passed with isolated app data and a
system-only PATH. ZIP file hashes/private-artifact checks passed. These checks
were on the development PC; fresh-machine installation and real gameplay/GPU
acceptance remain for manual testing. This build has not been published.
