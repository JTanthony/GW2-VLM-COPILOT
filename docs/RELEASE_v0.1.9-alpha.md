# v0.1.9-alpha — Text lookup and conversation improvements

This prerelease focuses on text conversations and official GW2 wiki research. Vision remains in beta testing; live gameplay accuracy has not been established.

- Retain the previous successful lookup subject for unnamed requirements and next-step follow-ups.
- Ask for missing details in the vague zone/achievement requests identified in testing.
- Support event names containing exclamation marks, improve Flying Circus routing, and correct garbled punctuation in reference text.
- Guide map answers to distinguish map completion, lantern achievements and encounter instances, and consider all applicable objective types.
- Provide clearer, sanitized lookup-failure reasons.

Developer source also includes improved simulated-player prompts, no-account testing and a public topic catalog. Test reports count returned lookup failures separately from runner errors. Development frame recording is excluded from this Windows package; release capture stays in RAM.

These are app, prompt and retrieval changes, not retrained model weights. Wiki retrieval can still fail or return incomplete evidence; answers can still be wrong. Typical response times remain hardware dependent. The latest broad text batch had a 29-second median, not a clean-machine performance guarantee.

Download the Windows ZIP, extract it and open GW2-VLM-COPILOT.exe. Python is bundled. llama.cpp, the model GGUF and matching vision projector are downloaded separately; use the README setup instructions. The ZIP includes an empty Models folder. Existing per-user configuration remains under Local AppData.
