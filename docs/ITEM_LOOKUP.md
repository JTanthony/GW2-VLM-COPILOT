# Item questions in chat

Players can type an item name or ask where to get it, what it is used for, or
whether to keep it. The research planner treats bare item names as lookup
requests and uses the wiki for acquisition, recipes and collection uses.
Ambiguous names require clarification rather than an assumed variant.

The wiki resolver recognizes numeric item IDs in official API links and requests
up to eight records from the public `/v2/items` endpoint in English. These calls
send no authorization token, account progress or inventory. Only selected basic
properties enter the answer context. Descriptions are reduced to plain text;
scripts, images and links from API records are not executed or downloaded.
Vendor value is copper, not a current trading-post quote.

This is an on-demand reference cache, not a full downloaded item catalog or
inventory index. It reuses the existing reference cache and per-user application
data location. Reference cache version 9 refreshes older extracts. Wiki articles
without recognized item links remain wiki-only. API failures do not discard
available wiki evidence. No public item record establishes player ownership.

Validation includes bounded public requests without credentials, official-link
recognition, safe fallback, metadata formatting, and a public live check for
Glob of Ectoplasm (19721). The local model's interpretation still needs player
testing. The Windows package must be rebuilt to receive these source changes.
