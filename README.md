# GW2 VLM COPILOT

Experimental Windows local AI copilot for Guild Wars 2. Ask questions, research the official wiki, optionally connect account progress, or approve continuous local window vision. Free, MIT-licensed project code; community contributions welcome. Not affiliated with or endorsed by ArenaNet or Google.

This is a source release, not a ready-to-install executable. Model weights and llama.cpp runtime binaries are downloaded separately. Answers can be incorrect: do not treat generated guides or screen readings as verified facts.

## Start here

- [Windows setup](docs/SETUP.md)
- [Development, testing and optional fine-tuning](docs/DEVELOPMENT.md)
- [Privacy and contribution safety](docs/PRIVACY.md)
- [Third-party notices](docs/THIRD_PARTY.md)

Gemma 4 12B handles answers and vision through a loopback llama.cpp server. Optional Gemma 3 1B generates GW2 player questions in the text tester. Neither model learns automatically from use. Wiki research sends generated public game search terms online; optional account connection calls the official GW2 API. Inference stays local.

## Current limitations

- Windows only; manual runtime/model setup and hardware tuning.
- GW2-focused release. Other adapter scaffolding in source does not establish supported titles.
- Account progress is a dated snapshot, refreshed through Accounts; only an API completion flag confirms completion.
- Captures require explicit approval. Keep the selected game restored; minimizing pauses capture. Frames are sampled at up to 2 FPS, while model analysis is slower and hardware-dependent.
- Text testing does not establish live gameplay accuracy. Earlier development samples averaged about 26 seconds per answer, approximately 48 seconds for GW2; not a benchmark guarantee for this release.
- No game inputs or microphone listening. No automatic chat coaching. No production installer, automatic updater or validated fine-tuning pipeline yet.

## License

[MIT](LICENSE) covers project code. Dependencies, model weights, retrieved wiki content and third-party materials retain their own terms. Do not bundle your credentials, account data, model files or local logs in contributions.
