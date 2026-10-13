# Text review improvements: round 4

This update changes application prompts, retrieval and the simulated-player tester. It does not train either model's weights.

- Retain six recent dialogue turns instead of three, preserving constraints for longer follow-ups. History remains bounded and compatible with request-budget compaction.
- Keep an established research subject for unnamed achievement/event/mastery follow-ups; explicitly named new subjects remain eligible to change it.
- Ask for location on unspecified nearby exploration requests instead of submitting a speculative lookup plan.
- Exclude wiki navigation boxes from article extracts. Distinguish mastery tracks, training levels, region-specific points and mount acquisition. Preserve table units and participation reward tiers; use only map-specific completion objective types.
- When an article exceeds the existing response-size limit, try its introduction and at most one relevant section. Mark this evidence partial. Other validation and network failures still fail safely; no limits or allowed-source permissions are expanded.
- Reject unsupported unquoted multiword proper names from the small simulated-player model, using the existing controlled follow-up fallback.

Validation: 137 automated tests passed, including topic switching, longer dialogue, navigation filtering, bounded large-page fallback and invented tester names. These checks verify code behavior with fixtures; a new local text run is still needed to assess answer quality and timing. Vision remains in beta testing, with no capture or recording changes in this update.

Run `run-gw2-wiki-for-training.cmd` for saved-account mode or `run-gw2-wiki-for-training-no-account.cmd` without an account. Both use the eight-hour limit (or 1,000 sessions, whichever comes first). Use `stop-gw2-wiki-for-training.cmd` to stop between inferences. Keep raw reports, account data and models private and out of Git.
