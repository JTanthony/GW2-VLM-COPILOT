# Text review round 6

The larger no-account text run exposed missing mastery-track lookups, incorrect
zone/instance classification, aggregate mastery rows treated as levels, and a
long lookup-planning request exceeding the supported 4096-token budget.

## Changes

- Explicit mastery-track names override speculative planner topics.
- Known mount and other mastery tracks route to their official regional wiki
  tables. Requested sections retain complete labeled rows; Total rows are
  excluded from focused training-level evidence. Relevant section unlock notes
  are retained when present.
- Infobox tables and definition lists preserve Type, Region and other identity
  fields as priority evidence. These remain available during answer compaction.
- Unnamed map/zone/encounter follow-ups retain the established lookup subject.
- Typographic dashes and quotes normalize to ordinary search punctuation. URLs,
  credential-like terms and other disallowed punctuation remain blocked.
- Several unspecified first-turn planning requests skip speculative retrieval
  so the assistant can ask for the missing player detail.
- Lookup-planning JSON dialogue can now be compacted without dropping its
  current question or previous topic. The 4096-token limit remains unchanged.
- Answer guidance distinguishes mastery costs from rewards, single selected
  training levels from aggregates, map identity from nearby encounters, and
  achievement-specific prerequisite/exclusivity notes.
- Reference extract cache version is now 8 so old extracts refresh naturally.

## Verification and limits

165 automated tests and the source GUI smoke check passed. Public read-only
wiki checks found the correct Griffon, Warclaw and Gliding regional tables and
retained Inner Nayos as Type: Zone in priority evidence. No live 12B replay was
run: these checks prove retrieval/formatting behavior, not model accuracy or
speed. Custom wiki layouts and arbitrary unnamed follow-ups still need review.
The first-turn clarification rules are bounded patterns, not a general intent
classifier. Automatic model weight training is not performed.

Private logs remain excluded from Git. No Windows package was rebuilt and
neither a release nor a commit was published by this update.
