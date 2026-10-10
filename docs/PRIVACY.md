# Privacy and safe contributions

Model inference uses a loopback server. Approved frames stay in memory; game inputs and microphone listening are not implemented. Wiki research sends validated public search phrases to the official wiki; the optional account adapter sends your key only to the official GW2 API. Local operation is not fully offline when these features are used.

Credentials are saved using Windows user protection. Private account snapshots, conversations, resources and logs can exist under local-data. Model outputs and wiki text are untrusted data, not commands.

Never upload local-data, runtime, .venv, *.local.json, .env, keys, snapshots, logs, screenshots with account information, or model weights. .gitignore does not protect previously tracked files or manually assembled ZIPs. Inspect the actual upload manifest. Report only sanitized failures using synthetic fixtures; never post an API key in an issue.
