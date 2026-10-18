# Story achievements and vision context

Verified: 2026-10-18T15:34:21.114266+00:00

Public reference covering Story Journal categories from Living World Season 1 through Visions of Eternity, including Living World Seasons 2–4, The Icebrood Saga and expansion acts. Personal-story and Scarlet recap chapters are not included in the chapter index. Category membership may include legacy or mixed story/open-world entries; it is not a claim of present availability.

The current reference contains 66 categories, 1897 achievement memberships, 132 exact-title chapter mappings and 9 unresolved chapters.

## Runtime behavior

Vision preserves a readable green tracker title as `Story chapter: <exact name>`. Exact chapter or quest names resolve to official story/category IDs. Prefix-free watch-list text, partial names and ambiguous matches do not establish a selected story. This identifies selected content only: green tracker visibility never proves the player entered an instance.

For a connected account snapshot, the app counts only `done=true` within the matched category. Category totals are labeled as story-category totals, not counts for one instance. Individual tasks are linked to a chapter only by exact achievement title or explicit Story Instance text in official metadata. Other category achievements may belong elsewhere. Unfinished tasks are candidate research subjects, not proof of eligibility. Missing accounts still allow title recognition without fabricated progress.

The one-time vision introduction may show a selected story category after two consistent observations. An explicitly displayed map retains priority. No additional missable-achievement alerts, combat guidance, per-map-change spam or instance-entry claims are enabled. Normal images remain in RAM. Wiki requirements must be verified before recommending a next step.

## Refresh and limits

Run `.venv\Scripts\python.exe tools/refresh_story_achievements.py` in the source project. It uses public categories, stories, seasons and quests endpoints without a key. Chapter/category matches are conservative exact-title associations; no speculative act mapping is used. Quest API coverage can lag current releases. Missing mappings remain in `unresolved_chapters`, and lookup remains unknown rather than inheriting a neighboring act. Rebuild Windows separately to include new code and public reference data.

189 automated tests and the source GUI smoke check passed for the initial implementation. These check mappings, label handling, separate category counts and lack of instance claims; they do not establish live pixel-reading accuracy. Next vision tests should hold a green title visible, ask for its unfinished tasks, and compare outside/inside-instance behavior.

## Categories

| API ID | Category | Entries |
|---:|---|---:|
| 43 | Clockwork Chaos | 34 |
| 44 | Emissary Vorpp's Field Assistant | 6 |
| 53 | Tower of Nightmares | 32 |
| 54 | The Nightmares Within | 11 |
| 56 | The Nightmare Is Over | 12 |
| 62 | Escape from Lion's Arch | 23 |
| 65 | The Battle for Lion's Arch | 39 |
| 68 | Gates of Maguuma | 11 |
| 70 | Entanglement | 11 |
| 71 | The Dragon's Reach, Part 1 | 8 |
| 72 | The Dragon's Reach, Part 2 | 11 |
| 81 | Echoes of the Past | 9 |
| 82 | Tangled Paths | 8 |
| 83 | Seeds of Truth | 8 |
| 100 | Point of No Return | 10 |
| 104 | Heart of Thorns: Act 1 | 20 |
| 121 | Heart of Thorns: Act 4 | 10 |
| 122 | Heart of Thorns: Act 3 | 14 |
| 123 | Heart of Thorns: Act 2 | 15 |
| 139 | Out of the Shadows | 28 |
| 144 | Rising Flames | 32 |
| 147 | A Crack in the Ice | 25 |
| 154 | The Head of the Snake | 41 |
| 164 | Flashpoint | 37 |
| 171 | One Path Ends | 44 |
| 183 | Path of Fire: Act 2 | 19 |
| 187 | Path of Fire: Act 3 | 20 |
| 188 | Path of Fire: Act 1 | 17 |
| 196 | Daybreak | 55 |
| 203 | A Bug in the System | 51 |
| 209 | Long Live the Lich | 71 |
| 216 | A Star to Guide Us | 71 |
| 224 | All or Nothing | 112 |
| 226 | War Eternal | 61 |
| 236 | Prologue: Bound by Blood | 80 |
| 241 | Whisper in the Dark | 39 |
| 246 | Shadow in the Ice | 50 |
| 251 | Visions of the Past: Steel and Fire | 48 |
| 253 | No Quarter | 74 |
| 254 | Jormag Rising | 69 |
| 266 | Champions | 76 |
| 311 | End of Dragons: Act 1 | 20 |
| 312 | End of Dragons: Act 5 | 14 |
| 319 | End of Dragons: Act 2 | 16 |
| 322 | End of Dragons: Act 3 | 21 |
| 325 | End of Dragons: Act 4 | 18 |
| 328 | Flame and Frost | 28 |
| 329 | Sky Pirates | 43 |
| 347 | Delve into the Haze | 25 |
| 353 | What Lies Within | 38 |
| 354 | End of Dragons: Interlude | 3 |
| 355 | Secrets of the Obscure: Act 1 | 11 |
| 360 | Secrets of the Obscure: Act 3 | 10 |
| 368 | Secrets of the Obscure: Act 2 | 13 |
| 405 | Through the Veil | 10 |
| 408 | The Realm of Dreams | 13 |
| 417 | The Midnight King | 20 |
| 424 | Janthir Wilds: Act 2 | 21 |
| 427 | Janthir Wilds: Act 1 | 26 |
| 442 | Godspawn | 16 |
| 445 | Repentance | 14 |
| 457 | Absolution | 16 |
| 469 | Visions of Eternity: Act 2 | 19 |
| 471 | Visions of Eternity: Act 1 | 23 |
| 481 | The Only Way | 22 |
| 485 | Code of Creation | 25 |

## Chapter mappings

| Season/expansion | Readable chapter | Category ID | Explicitly linked tasks |
|---|---|---:|---:|
| Living World Season 2 | Gates of Maguuma | 68 | 1 |
| Living World Season 2 | Entanglement | 70 | 1 |
| Living World Season 2 | The Dragon's Reach, Part 1 | 71 | 1 |
| Living World Season 2 | The Dragon's Reach, Part 2 | 72 | 1 |
| Living World Season 2 | Echoes of the Past | 81 | 1 |
| Living World Season 2 | Tangled Paths | 82 | 1 |
| Living World Season 2 | Seeds of Truth | 83 | 1 |
| Living World Season 2 | Point of No Return | 100 | 1 |
| Heart of Thorns | City of Hope | 123 | 5 |
| Heart of Thorns | Prized Possessions | 123 | 4 |
| Heart of Thorns | Buried Insight | 122 | 4 |
| Heart of Thorns | The Way In | 122 | 1 |
| Heart of Thorns | Hearts and Minds | 121 | 5 |
| Heart of Thorns | In Their Footsteps | 104 | 1 |
| Heart of Thorns | Bitter Harvest | 121 | 4 |
| Heart of Thorns | Strange Observations | 123 | 4 |
| Heart of Thorns | Torn from the Sky | 104 | 6 |
| Heart of Thorns | Prisoners of the Dragon | 104 | 1 |
| Heart of Thorns | The Jungle Provides | 104 | 5 |
| Heart of Thorns | The Predator's Path | 123 | 1 |
| Heart of Thorns | Roots of Terror | 122 | 7 |
| Heart of Thorns | Establishing a Foothold | 104 | 1 |
| Heart of Thorns | Sign Cutting | 122 | 1 |
| Living World Season 3 | Out of the Shadows | 139 | 0 |
| Living World Season 3 | Rising Flames | 144 | 0 |
| Living World Season 3 | A Crack in the Ice | 147 | 0 |
| Living World Season 3 | The Head of the Snake | 154 | 0 |
| Living World Season 3 | Flashpoint | 164 | 0 |
| Living World Season 3 | One Path Ends | 171 | 0 |
| Path of Fire | Blazing a Trail | 188 | 2 |
| Path of Fire | The Way Forward | 183 | 4 |
| Path of Fire | Hallowed Ground | 183 | 4 |
| Path of Fire | The Departing | 187 | 2 |
| Path of Fire | The Sacrifice | 188 | 5 |
| Path of Fire | Enemy of My Enemy | 187 | 7 |
| Path of Fire | Beast of War | 187 | 4 |
| Path of Fire | Small Victory (Epilogue) | 187 | 3 |
| Path of Fire | Crystalline Memories | 183 | 4 |
| Path of Fire | Facing the Truth | 183 | 6 |
| Path of Fire | To Kill a God | 187 | 3 |
| Path of Fire | Night of Fires | 188 | 5 |
| Path of Fire | Sparking the Flame | 188 | 4 |
| Living World Season 4 | Daybreak | 196 | 0 |
| Living World Season 4 | A Bug in the System | 203 | 0 |
| Living World Season 4 | Long Live the Lich | 209 | 0 |
| Living World Season 4 | A Star to Guide Us | 216 | 0 |
| Living World Season 4 | All or Nothing | 224 | 0 |
| Living World Season 4 | War Eternal | 226 | 0 |
| The Icebrood Saga | Prologue: Bound by Blood | 236 | 0 |
| The Icebrood Saga | Whisper in the Dark | 241 | 0 |
| The Icebrood Saga | Shadow in the Ice | 246 | 0 |
| The Icebrood Saga | Visions of the Past: Steel and Fire | 251 | 0 |
| The Icebrood Saga | No Quarter | 253 | 0 |
| The Icebrood Saga | Jormag Rising | 254 | 0 |
| The Icebrood Saga | Champions | 266 | 0 |
| End of Dragons | Empty | 322 | 1 |
| End of Dragons | The Only One | 312 | 1 |
| End of Dragons | Old Friends | 311 | 6 |
| End of Dragons | To Catch a Spider | 322 | 1 |
| End of Dragons | Deepest Secrets | 319 | 1 |
| End of Dragons | Outreach | 311 | 1 |
| End of Dragons | Extraction Point | 312 | 1 |
| End of Dragons | Fallout | 322 | 1 |
| End of Dragons | Weight of the World | 325 | 1 |
| End of Dragons | The Cycle, Reborn | 312 | 1 |
| End of Dragons | In the Name of the Law | 325 | 1 |
| End of Dragons | The Scenic Route | 319 | 1 |
| End of Dragons | The Future in Jade | 319 | 1 |
| End of Dragons | Can't Trust a Pirate | 311 | 1 |
| End of Dragons | Your Kind of People | 311 | 1 |
| Living World Season 1 | Flame and Frost | 328 | 0 |
| Living World Season 1 | Sky Pirates | 329 | 0 |
| Living World Season 1 | Clockwork Chaos | 43 | 0 |
| Living World Season 1 | The Tower of Nightmares | 53 | 1 |
| Living World Season 1 | The Battle for Lion's Arch | 65 | 1 |
| End of Dragons | What Lies Within | 353 | 1 |
| Secrets of the Obscure | Treachery | 360 | 1 |
| Secrets of the Obscure | Mabon's Fate | 368 | 1 |
| Secrets of the Obscure | Tower of Secrets | 368 | 1 |
| Secrets of the Obscure | The Missing Facet | 368 | 1 |
| Secrets of the Obscure | Into the Obscure | 360 | 1 |
| Secrets of the Obscure | Mother of Stars | 355 | 1 |
| Secrets of the Obscure | Commander without a Cause | 355 | 1 |
| Secrets of the Obscure | Voices beyond the Veil | 368 | 1 |
| Secrets of the Obscure | The World Spire | 360 | 1 |
| Secrets of the Obscure | Hell Breaks Loose | 355 | 1 |
| Secrets of the Obscure | The Survivors | 405 | 1 |
| Secrets of the Obscure | Heitor's Gate | 405 | 1 |
| Secrets of the Obscure | Duress | 405 | 1 |
| Secrets of the Obscure | The War Council | 408 | 1 |
| Secrets of the Obscure | Eventide's March | 408 | 1 |
| Secrets of the Obscure | Forced Hand | 408 | 1 |
| Secrets of the Obscure | Sovereign of Nayos | 417 | 1 |
| Secrets of the Obscure | Desperate Measures | 417 | 1 |
| Secrets of the Obscure | The Eleventh Hour | 417 | 1 |
| Janthir Wilds | Against the Wall | 424 | 1 |
| Janthir Wilds | Missing in Action | 427 | 1 |
| Janthir Wilds | Diplomacy and Discovery | 427 | 1 |
| Janthir Wilds | Finding Balance | 424 | 1 |
| Janthir Wilds | Storm Clouds over Janthir | 424 | 1 |
| Janthir Wilds | Twice Stricken | 424 | 1 |
| Janthir Wilds | Home Sweet Home | 427 | 1 |
| Janthir Wilds | Sorrow in These Halls | 424 | 1 |
| Janthir Wilds | Strangers among Lands | 427 | 1 |
| Janthir Wilds | Unknown Territory | 427 | 1 |
| Janthir Wilds | Trial and Error | 442 | 1 |
| Janthir Wilds | Balrior Peak | 442 | 1 |
| Janthir Wilds | Battle's Eve | 442 | 1 |
| Janthir Wilds | A Legacy Damned | 445 | 1 |
| Janthir Wilds | Into the Valley of Shadow | 445 | 1 |
| Janthir Wilds | Penance for the Past | 445 | 1 |
| Janthir Wilds | Salvation's Cost | 457 | 1 |
| Janthir Wilds | Forced Entry | 457 | 1 |
| Janthir Wilds | A Titanic Undertaking | 457 | 1 |
| Visions of Eternity | Eyes, Ears, and Arms | 471 | 1 |
| Visions of Eternity | Truths Unearthed | 471 | 1 |
| Visions of Eternity | Solid Ground | 471 | 1 |
| Visions of Eternity | Unscheduled Departures | 471 | 1 |
| Visions of Eternity | Beneath the Canopy | 469 | 1 |
| Visions of Eternity | Fumbling in the Dark | 469 | 1 |
| Visions of Eternity | Ruins of the Old World | 469 | 1 |
| Visions of Eternity | A Bold Strategy | 481 | 1 |
| Visions of Eternity | So It Is Written | 481 | 1 |
| Visions of Eternity | Within Your Grasp | 481 | 1 |
| Visions of Eternity | Deeper Revelations | 485 | 1 |
| Visions of Eternity | On the Threshold | 481 | 1 |
| Visions of Eternity | Divitium Nava | 481 | 1 |
| Visions of Eternity | Under Pressure | 485 | 1 |
| Visions of Eternity | Everything That We Are | 485 | 1 |
| Visions of Eternity | So Be It | 485 | 1 |
| Visions of Eternity | The Burden of Seeing | 485 | 1 |
| Visions of Eternity | Ripples in the Pond | 485 | 1 |

## Unresolved chapters

- Heart of Thorns: Prologue: Rally to Maguuma
- End of Dragons: Convergence
- End of Dragons: Deep Research
- End of Dragons: What Lies Beneath
- End of Dragons: Interlude: Forward
- Secrets of the Obscure: Prologue: Uncertain Times
- Janthir Wilds: Prologue: The Tyrian Alliance
- Visions of Eternity: Path of Divinity
- Visions of Eternity: Prologue: On the Sly

## Public sources

- [Story API](https://wiki.guildwars2.com/wiki/API:2/stories)
- [Quest API and coverage caveat](https://wiki.guildwars2.com/wiki/API:2/quests)
- [Story Journal table](https://wiki.guildwars2.com/wiki/Story_Journal/table)

Full achievement IDs, names, flags, prerequisites, quest IDs and mapping evidence are stored in `data/gw2/story_achievements.json`. No account records, credentials or private screenshots are included.
