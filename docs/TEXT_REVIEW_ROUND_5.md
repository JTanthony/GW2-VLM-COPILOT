# Text review improvements: round 5

This changes retrieval, extraction, request compaction and the tester; it does not train model weights.

- Explicit names in structured player requests override speculative model lookup plans.
- GW2 lookup resolves an exact title and wiki redirects before keyword search. Fallback search rejects hits with no substantive title overlap. Turtle Mount and Fishing track requests resolve to the End of Dragons mastery table.
- Requested table rows retain their section, XP, points and descriptions. Matching rows and individual mastery region/track/XP fields receive priority during request compaction. Shortened evidence remains marked partial; no token or response-size limit is increased.
- Coin icon denominations are preserved as plain text. Negative requests for source footers suppress the app-added footer.
- Reference cache extraction version changes to refresh old evidence automatically.
- Malformed generated player questions use the controlled follow-up fallback. Private run metadata records the app version and a digest of the reviewed source files, without reading Git credentials or model configurations into that digest.

Validation: automated regression tests plus read-only official wiki checks for Turtle Mount, Fishing on a Full Tank and Lost Souls. The live check resolved Turtle Mount to the End of Dragons mastery table with its proper XP/points rows, Fishing on a Full Tank to its exact page, and Lost Souls to the Bloodstone Fen event-chain redirect. These checks validate retrieval, not local-model answer accuracy. Run a fresh text batch to evaluate accuracy and speed.

The standard Windows app still keeps screenshots in RAM. No vision or recording changes are part of this update. Keep test reports and account data private. Source changes require a new Windows build before release users receive them.
