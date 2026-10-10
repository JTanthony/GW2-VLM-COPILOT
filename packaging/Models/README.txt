Put your downloaded model and engine files in this folder.

Recommended model: gemma-4-12B-it-QAT-Q4_0.gguf
Matching vision companion: mmproj-gemma-4-12B-it-QAT-BF16.gguf

The vision companion lets the 12B model read images. It is not the
optional Gemma 3 1B development tester.

Also place the extracted llama.cpp server folder here. Copy the CUDA
runtime DLLs into that server folder beside llama-server.exe.

Open the app and use Browse to select llama-server.exe, the model,
and its vision companion. See ../README.md for download links and
complete instructions. No models or engine binaries are bundled.

Uninstall preserves files you add here.
