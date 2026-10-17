# Privacy and safe contributions

Model inference uses a loopback server. Approved frames stay in memory; game inputs and microphone listening are not implemented. Wiki research sends validated public search phrases to the official wiki; the optional account adapter sends your key only to the official GW2 API. Local operation is not fully offline when these features are used.

Credentials are saved using Windows user protection. Private account snapshots, conversations, resources and logs can exist under local-data. Model outputs and wiki text are untrusted data, not commands.

Never upload local-data, runtime, .venv, *.local.json, .env, keys, snapshots, logs, screenshots with account information, or model weights. .gitignore does not protect previously tracked files or manually assembled ZIPs. Inspect the actual upload manifest. Report only sanitized failures using synthetic fixtures; never post an API key in an issue.

## Update notifications

On launch, the app checks the public GitHub release list for newer Windows ZIPs, including prereleases. Uncheck **Check updates on launch** to disable this; **Check updates** remains available manually. GitHub receives your network address and the installed version in the request header. No chat, screenshots, account data or tokens are sent. Checks do not download or install anything. **Download update** opens the project release page in your browser. Offline or failed automatic checks stay quiet.
# Public item lookup

Item research may request public item IDs from `api.guildwars2.com/v2/items`.
These requests use no account key and do not access inventory. Relevant public
item metadata is cached with wiki references; only matching records enter chat
context. Public item information does not establish ownership or live prices.

