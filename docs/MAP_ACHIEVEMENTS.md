# Dedicated map achievement reference

Verified: 2026-10-17T17:11:24.431406+00:00

Public API membership across dedicated open-world map categories, including expansion maps and hubs. Not every map has its own category; this is not every achievement obtainable in an area. No account data is included.

Groups are matched to exact official map names and Public map types. General includes only Dry Top and The Silverwastes. Historical, story, collection, regional, raid, PvP, WvW and convergence groups are excluded from map totals. Living World Season 1 Story Journal categories are included separately as an explicitly scoped exception. Inner Nayos combines its three dedicated section categories, deduplicating achievement IDs; section membership remains available separately. Verdant Brink uses map ID 1052 because the API also exposes a second Public map with the same name.

Every category membership and achievement detail is verified against the public official API. Wiki headline totals may differ; totals below deliberately use API IDs. Per-achievement flags and prerequisite IDs are retained, but membership does not establish current availability or player eligibility. Entries remain in their official category even if an objective refers to another map.

| Group | Map | Map ID | Category IDs | Entries |
|---|---|---:|---|---:|
| Core Tyria / Living World Season 2 | Dry Top | 988 | 69 | 20 |
| Core Tyria / Living World Season 2 | The Silverwastes | 1015 | 80 | 31 |
| End of Dragons | Arborstone | 1428 | 314 | 23 |
| End of Dragons | Dragon's End | 1422 | 320 | 34 |
| End of Dragons | New Kaineng City | 1438 | 315 | 39 |
| End of Dragons | Seitung Province | 1442 | 323 | 33 |
| End of Dragons | The Echovald Wilds | 1452 | 318 | 48 |
| Heart of Thorns | Auric Basin | 1043 | 111 | 35 |
| Heart of Thorns | Dragon's Stand | 1041 | 109 | 29 |
| Heart of Thorns | Tangled Depths | 1045 | 112 | 44 |
| Heart of Thorns | Verdant Brink | 1052 | 116 | 42 |
| Janthir Wilds | Bava Nisos | 1574 | 455 | 19 |
| Janthir Wilds | Janthir Syntri | 1554 | 430 | 36 |
| Janthir Wilds | Lowland Shore | 1550 | 431 | 61 |
| Janthir Wilds | Mistburned Barrens | 1575 | 446 | 27 |
| Path of Fire | Crystal Oasis | 1210 | 179 | 19 |
| Path of Fire | Desert Highlands | 1211 | 190 | 32 |
| Path of Fire | Domain of Vabbi | 1248 | 174 | 35 |
| Path of Fire | Elon Riverlands | 1228 | 182 | 29 |
| Path of Fire | The Desolation | 1226 | 176 | 32 |
| Secrets of the Obscure | Amnytas | 1517 | 366 | 45 |
| Secrets of the Obscure | Inner Nayos | 1526 | 403, 409, 416 | 95 |
| Secrets of the Obscure | Skywatch Archipelago | 1510 | 358 | 40 |
| Secrets of the Obscure | The Wizard's Tower | 1509 | 357 | 33 |
| Visions of Eternity | Eternity's Garden | 1622 | 482 | 47 |
| Visions of Eternity | Leyspring Hollows | 1633 | 486 | 48 |
| Visions of Eternity | Shipwreck Strand | 1595 | 463 | 53 |
| Visions of Eternity | Starlit Weald | 1593 | 472 | 53 |

## Refresh and calculation

Machine-readable data: `data/gw2/map_achievements.json`. Refresh manually with `python tools/refresh_map_achievements.py`. This replaces the JSON and this document only after verifying public records. No account calls or credentials are used. The Windows builder includes only this curated public reference.

`category_progress` matches unique achievement IDs against a dated account snapshot. Only `done=true` confirms completion; matching current/max or absent records do not. Unknown maps and missing snapshots yield no result, not 0/0. The automatic vision message is not enabled.

## Coverage gaps

Other API Public maps are listed in the JSON under `unmapped_public_maps`. They include core zones, Living World maps with combined story/map categories, activities, lounges and duplicate map variants. Their exclusion means no dedicated match within our rules, not no achievements. Mixed groups can be added in a later explicitly broader scope.

## Dry Top

[Official category: Dry Top](https://api.guildwars2.com/v2/achievements/categories/69) / [Wiki](https://wiki.guildwars2.com/wiki/Dry_Top_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 1631 | Llama Drama | Permanent |  |
| 1632 | Buried Treasure: Prospect Valley | Permanent |  |
| 1633 | Dive Master: Prospect Valley | Permanent |  |
| 1634 | Coin Collector: Prospect Valley | Permanent |  |
| 1635 | Quicksand Survivor | Permanent |  |
| 1636 | Legendary Llama Locator | Permanent |  |
| 1637 | Sparring Rock Master | Permanent |  |
| 1638 | Hit and Run | Permanent |  |
| 1639 | Prospect Valley Crash Site Climber | Permanent |  |
| 1651 | Buried Treasure: Uplands | Permanent |  |
| 1652 | Chickenado Chaser | Permanent |  |
| 1653 | Coin Collector: Uplands | Permanent |  |
| 1654 | Ruler of Shinies | Permanent |  |
| 1655 | Learned Legendary Llama Locator | Permanent |  |
| 1692 | Buried Treasure: Challenger Cliffs | Permanent |  |
| 1693 | Licensed Learned Legendary Llama Locator | Permanent |  |
| 1694 | Coin Collector: Challenger Cliffs | Permanent |  |
| 1695 | Sand Shield | Permanent |  |
| 1696 | Heist Hinderer | Permanent |  |
| 1697 | Rock 'n' Roller | Permanent |  |

## The Silverwastes

[Official category: The Silverwastes](https://api.guildwars2.com/v2/achievements/categories/80) / [Wiki](https://wiki.guildwars2.com/wiki/The_Silverwastes_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 1797 | Iron | Permanent |  |
| 1798 | Copper | Permanent |  |
| 1799 | The Demolisher | Permanent |  |
| 1800 | Platinum | Permanent |  |
| 1801 | The Executioner | Permanent |  |
| 1802 | The Annihilator | Permanent |  |
| 1803 | The Tormentor | Permanent |  |
| 1804 | The Be-All and the End-All | Permanent |  |
| 1805 | Mercantile Mercenary | Permanent |  |
| 1806 | Silver and Gold | Permanent |  |
| 1807 | Silverwastes Shoveler | Permanent |  |
| 1808 | Defender: Indigo Cave | Permanent |  |
| 1809 | Defender: Blue Oasis | Permanent |  |
| 1810 | Lost Badges | Permanent |  |
| 1811 | Defender: Red Rock Bastion | Permanent |  |
| 1812 | Defender: Amber Sandfall | Permanent |  |
| 1824 | Fear No Evil | Permanent |  |
| 1834 | Retrospective Runaround | Permanent |  |
| 1835 | Go for the Gold | Permanent |  |
| 1836 | Ambassador's Aid | Permanent |  |
| 2063 | Golem Protector | Permanent |  |
| 2064 | Beekeeper Crusher | Permanent |  |
| 2065 | Mangler Wrangler | Permanent |  |
| 2066 | Dive Master: Drydock Scratch | Permanent |  |
| 2067 | Jump Up to Get Down | Permanent |  |
| 2068 | Vinewrath Vanquisher | Permanent |  |
| 2069 | Covered in Bees! | Permanent |  |
| 2070 | Don't Look Now | Permanent |  |
| 2071 | Arboreal Protector | Permanent |  |
| 2072 | Devourer Protector | Permanent |  |
| 2073 | Dark Wing Defoliator | Permanent |  |

## Arborstone

[Official category: Arborstone](https://api.guildwars2.com/v2/achievements/categories/314) / [Wiki](https://wiki.guildwars2.com/wiki/Arborstone_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 6074 | Tracing the Tapestry | RepairOnLogin, RequiresUnlock, Permanent |  |
| 6112 | Golem Behavior Analysis | RepairOnLogin, RequiresUnlock, Permanent |  |
| 6121 | Arborstone Vaulter Extraordinaire | Permanent |  |
| 6152 | A Sampling of Snargle | Permanent |  |
| 6161 | Arborstone Hide-and-Seek Master | Permanent |  |
| 6165 | A Blooming Errand | RepairOnLogin, RequiresUnlock, Permanent |  |
| 6175 | Looking Back | Permanent | 6326 |
| 6261 | A Guardian Once More | Pvp, RepairOnLogin, Permanent |  |
| 6270 | Winn's Favorite Patron | Permanent |  |
| 6290 | Pure Enmity | RepairOnLogin, RequiresUnlock, Permanent |  |
| 6319 | Brothers in Harms | RepairOnLogin, RequiresUnlock, Permanent |  |
| 6333 | Character Growth | Permanent |  |
| 6356 | Lost Lore | RepairOnLogin, Permanent |  |
| 6359 | Lucky Guess | Permanent | 6268 |
| 6381 | The End of the Celestial Ministry | RepairOnLogin, Permanent |  |
| 6387 | Arborstone Vaulter | Permanent |  |
| 6397 | Hide-and-Seek in Arborstone | Permanent |  |
| 6399 | Building a Better Bot | RepairOnLogin, Permanent |  |
| 6414 | Fan of the Band | Permanent |  |
| 6448 | The Fate of House zu Heltzer | RepairOnLogin, Permanent |  |
| 6455 | Albax, the Unlucky | RequiresUnlock, Permanent |  |
| 6490 | Mech Behavior Analysis | RepairOnLogin, RequiresUnlock, Permanent |  |
| 6518 | Arborstone Diver | Permanent |  |

## Dragon's End

[Official category: Dragon's End](https://api.guildwars2.com/v2/achievements/categories/320) / [Wiki](https://wiki.guildwars2.com/wiki/Dragon's_End_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 6082 | Ready Up: South | Permanent |  |
| 6127 | Shock-Wave Jumper | Permanent |  |
| 6131 | Ready Up: Central | Permanent |  |
| 6140 | A Strange Diet | Permanent |  |
| 6144 | The Last of Their Kind | Permanent |  |
| 6148 | Ready Up: North | Permanent |  |
| 6160 | Ultimate Dragon Champion | Permanent |  |
| 6164 | Simpleminded | Permanent |  |
| 6170 | Hold Out | Permanent |  |
| 6178 | Catch Me If You Can | Permanent |  |
| 6186 | Dead Play | Permanent |  |
| 6217 | Jade Sea Warfare | Permanent |  |
| 6228 | Survivors | Permanent |  |
| 6234 | Springer Ride: Kuan Jun Pavilion | Permanent |  |
| 6236 | Raptor Ride: Chantry of the Crab | Permanent |  |
| 6241 | Tower Diver | Permanent |  |
| 6256 | Not-So-Peaceful Shrine | Hidden, Permanent |  |
| 6260 | Tsunami Dodger | Permanent |  |
| 6266 | Dive Bar | Permanent |  |
| 6271 | Terror on the Jade Sea | Permanent |  |
| 6292 | Mysteries Deep Within | Permanent |  |
| 6300 | Fueled by Elder Dragons | Permanent |  |
| 6303 | Dragon's End Culture: The Luxon Armada | Permanent |  |
| 6320 | Respects Paid | Permanent |  |
| 6369 | Lighting Dragon's End | IgnoreNearlyComplete, Repeatable, Permanent |  |
| 6375 | Pocket Maw Crystals | Permanent |  |
| 6429 | Dragon's End (Corporate) Culture: Xunlai Jade | Permanent |  |
| 6453 | Dragon's End Mastery | CategoryDisplay, MoveToTop, Permanent |  |
| 6456 | Untarnished Spirit | Permanent |  |
| 6470 | The Floor Is Void | Permanent |  |
| 6496 | Dragon Pacifier | Permanent |  |
| 6511 | Weekly Dragon's End Jade Treasure Recovery | Weekly |  |
| 6514 | Savior of the Supply Chain | Permanent |  |
| 6516 | Sled Defender | Permanent |  |

## New Kaineng City

[Official category: New Kaineng City](https://api.guildwars2.com/v2/achievements/categories/315) / [Wiki](https://wiki.guildwars2.com/wiki/New_Kaineng_City_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 6083 | Light These Streets | IgnoreNearlyComplete, Repeatable, Permanent |  |
| 6107 | Read "The Secret of the Vault" | Permanent |  |
| 6117 | Abyssal Dive | Permanent |  |
| 6132 | Kaineng Blackout | Permanent |  |
| 6147 | Literary Thievery | Permanent |  |
| 6151 | Honorary Plumber | Permanent |  |
| 6180 | No-Fun Police | IgnoreNearlyComplete, Repeatable, Permanent | 6398 |
| 6188 | Weekly New Kaineng City Jade Treasure Recovery | Weekly |  |
| 6189 | Wind through the Walls | Permanent |  |
| 6195 | Repair Crew Royale | Permanent |  |
| 6196 | Cull the Corruption | Permanent |  |
| 6213 | Protector of Kaineng | IgnoreNearlyComplete, Repeatable, Permanent | 6196 |
| 6235 | Always in Working Order | IgnoreNearlyComplete, Repeatable, Permanent | 6195 |
| 6242 | Crow Catcher | Permanent |  |
| 6247 | Working as Intended | IgnoreNearlyComplete, Repeatable, Permanent | 6482 |
| 6282 | The Hidden Vault | Permanent |  |
| 6291 | Kappa Exterminator | IgnoreNearlyComplete, Repeatable, Permanent | 6432 |
| 6299 | Little Foxes in the Big City | Permanent |  |
| 6310 | Harbinger of Zhaitan | IgnoreNearlyComplete, Repeatable, Permanent | 6347 |
| 6347 | The Old City of Decay | Permanent |  |
| 6358 | Raptor Runner: New Kaineng City | Permanent |  |
| 6370 | Springer Fling: New Kaineng City | Permanent |  |
| 6385 | Hero of New Kaineng | IgnoreNearlyComplete, Repeatable, Permanent | 6132 |
| 6396 | Ocean-Fresh Sashimi | Permanent |  |
| 6398 | Cleanup Duty | Permanent |  |
| 6412 | Delivery Service Champion | IgnoreNearlyComplete, Repeatable, Permanent | 6396 |
| 6424 | Champion Plumber | IgnoreNearlyComplete, Repeatable, Permanent | 6151 |
| 6428 | New Kaineng City Mastery | CategoryDisplay, MoveToTop, Permanent |  |
| 6432 | Don't Pet the Kappa | Permanent |  |
| 6443 | Reliving the Tragedy | IgnoreNearlyComplete, Repeatable, Permanent | 6282 |
| 6461 | The History of New Kaineng | Permanent |  |
| 6482 | Clear the Canals | Permanent |  |
| 6487 | Soapbox Preacher | Permanent |  |
| 6508 | Not in This Neighborhood | IgnoreNearlyComplete, Repeatable, Permanent | 6487 |
| 6512 | Honorary Citizen of New Kaineng | Permanent |  |
| 6905 | New Kaineng Jade Bot Racer: Gold | Permanent |  |
| 6914 | New Kaineng Skiff Racer: Silver | Permanent |  |
| 6923 | New Kaineng Skiff Racer: Gold | Permanent |  |
| 6929 | New Kaineng Jade Bot Racer: Silver | Permanent |  |

## Seitung Province

[Official category: Seitung Province](https://api.guildwars2.com/v2/achievements/categories/323) / [Wiki](https://wiki.guildwars2.com/wiki/Seitung_Province_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 6069 | Authorial Intent | Permanent |  |
| 6088 | Aetherblade Shenanigans | Permanent |  |
| 6118 | Trials of the Tengu | Permanent |  |
| 6136 | Seitung Prison Springer Ride | Permanent |  |
| 6150 | Seitung Harbor Shenanigans | Permanent |  |
| 6185 | Eternal Aetherblade Shenanigans | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 6088 |
| 6198 | Misty Leap | Permanent |  |
| 6209 | Eternal Purist Shenanigans | IgnoreNearlyComplete, Repeatable, Permanent | 6388 |
| 6231 | Daigo Ward Raptor Ride | Permanent |  |
| 6239 | Illuminating Seitung Province | IgnoreNearlyComplete, Repeatable, Permanent |  |
| 6257 | Derelict Temple Raptor Ride | Permanent |  |
| 6265 | Eternal Seitung Harbor Shenanigans | IgnoreNearlyComplete, Repeatable, Permanent | 6150 |
| 6314 | Spiritual Childcare | Permanent |  |
| 6321 | Weekly Seitung Province Jade Treasure Recovery | Weekly |  |
| 6331 | Seitung Province Mastery | CategoryDisplay, MoveToTop, Permanent |  |
| 6352 | Fish Are Friends | Hidden, Permanent |  |
| 6366 | Aetherblade Cleanup | Permanent |  |
| 6377 | Dodger of Darkness | Permanent |  |
| 6388 | Purist Shenanigans | IgnoreNearlyComplete, Permanent |  |
| 6394 | Shing Jea Monastery Raptor Ride | Permanent |  |
| 6403 | Hatchery Helper | Permanent |  |
| 6409 | Eternal Seitung Province Meta-Event | IgnoreNearlyComplete, Repeatable, Permanent | 6468 |
| 6415 | Taxi! | Permanent |  |
| 6418 | Bian's World Tour | Permanent |  |
| 6447 | Eternal Troubles from the Deep | IgnoreNearlyComplete, Repeatable, Permanent | 6460 |
| 6460 | Troubles from the Deep | Permanent |  |
| 6464 | Jumping Training | Permanent |  |
| 6468 | Seitung Province Meta-Event | Permanent |  |
| 6494 | Renowned Adventurer: Seitung Province | Permanent |  |
| 6843 | Seitung Province Skiff Racer: Silver | Permanent |  |
| 6894 | Seitung Province Skiff Racer: Gold | Permanent |  |
| 6922 | Seitung Province Siege Turtle Ace: Silver | Permanent |  |
| 6925 | Seitung Province Siege Turtle Ace: Gold | Permanent |  |

## The Echovald Wilds

[Official category: The Echovald Wilds](https://api.guildwars2.com/v2/achievements/categories/318) / [Wiki](https://wiki.guildwars2.com/wiki/The_Echovald_Wilds_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 6072 | Well Armored | Permanent |  |
| 6078 | Slippery as a Fish | Permanent |  |
| 6097 | Saboteur in Our Midst | Permanent |  |
| 6137 | Friend to Testudines | Permanent |  |
| 6138 | Raptor Runner: Echovald Wilds | Permanent |  |
| 6154 | For the Living, Not the Dead | Permanent |  |
| 6159 | An Impostor Walks among Us | Permanent |  |
| 6162 | Echovald Wilds Mastery | CategoryDisplay, MoveToTop, Permanent |  |
| 6166 | Friends of a Feather | Permanent |  |
| 6183 | Avian Sharpshooter | Permanent |  |
| 6187 | Renowned Adventurer: Echovald Wilds | Permanent |  |
| 6193 | Not Too Worse for Wear | Permanent |  |
| 6194 | Cultures of Echovald: The Tengu | Permanent |  |
| 6203 | To Greater Heights | Pvp, RepairOnLogin, Permanent |  |
| 6207 | The Haunted Altar | Permanent |  |
| 6219 | Lighting the Echovald Wilds | IgnoreNearlyComplete, Repeatable, Permanent |  |
| 6221 | Resting Heart | Permanent |  |
| 6229 | For the Forest! | Permanent |  |
| 6269 | Cryptseeker | RequiresUnlock, Permanent |  |
| 6274 | What Did the Shrine Guardians Say? | Permanent |  |
| 6285 | Cultures of Echovald: The Kurzicks | Permanent |  |
| 6298 | Honorary Kestrel | Permanent |  |
| 6305 | Forest Warfare | Permanent |  |
| 6306 | The Haunted Perch | Permanent |  |
| 6309 | High-Score Archery | Permanent |  |
| 6312 | Head's Up! | Permanent |  |
| 6315 | Distant Ancestry | Permanent |  |
| 6325 | Vengeance Is Not Yours | Permanent |  |
| 6343 | Supernaturally Sneaky | Permanent |  |
| 6349 | Revealing Ritualists | Permanent |  |
| 6367 | Dance like Bei Fung Is Watching | Hidden, Permanent |  |
| 6372 | Lutgardis Maestro | Permanent |  |
| 6378 | Both Hale and Hearty | Permanent |  |
| 6380 | Weekly Echovald Wilds Jade Treasure Recovery | Weekly |  |
| 6383 | Theft Deterrence | Permanent |  |
| 6386 | Ward Nemesis | Permanent |  |
| 6421 | Sticky Fingers | Permanent |  |
| 6445 | The Haunted Court | Permanent |  |
| 6451 | Respect Your Elders | Permanent |  |
| 6458 | Valdhertz Victor | Permanent |  |
| 6472 | Cultures of Echovald: The Wardens | Permanent |  |
| 6498 | Springer Fling: Echovald Wilds | Permanent |  |
| 6502 | Echovald Wilds Diver | Permanent |  |
| 6515 | Dancing Barefoot | Hidden, Permanent |  |
| 6897 | Echovald Wilds Siege Turtle Ace: Gold | Permanent |  |
| 6913 | Echovald Wilds Jade Bot Racer: Gold | Permanent |  |
| 6917 | Echovald Wilds Jade Bot Racer: Silver | Permanent |  |
| 6918 | Echovald Wilds Siege Turtle Ace: Silver | Permanent |  |

## Auric Basin

[Official category: Auric Basin](https://api.guildwars2.com/v2/achievements/categories/111) / [Wiki](https://wiki.guildwars2.com/wiki/Auric_Basin_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 2188 | A Fungus Among Us: Silver | Pvp, Permanent |  |
| 2194 | Vinetooth Hunter | Permanent |  |
| 2200 | Fallen Masks: Silver | Pvp, Permanent |  |
| 2216 | Hidden Amphibian | Permanent |  |
| 2240 | "Vengeance Rising" Strongbox | Permanent |  |
| 2252 | On Wings of Gold: Silver | Pvp, Permanent |  |
| 2263 | Egg Bearer | Permanent |  |
| 2283 | The Golden Chicken | Permanent |  |
| 2292 | Highest Gear | Permanent |  |
| 2331 | The Floor Is Lava?: Gold | Pvp, Permanent |  |
| 2342 | Mushroom Power | Permanent |  |
| 2373 | A Study in Gold | Permanent |  |
| 2382 | Sanctum Scramble: Gold | Pvp, Permanent |  |
| 2406 | Fallen Masks: Gold | Pvp, Permanent |  |
| 2417 | Droppin' Bombs | Permanent |  |
| 2427 | Powered Up | Permanent |  |
| 2445 | On Wings of Gold: Gold | Pvp, Permanent |  |
| 2484 | The Floor Is Lava?: Silver | Pvp, Permanent |  |
| 2512 | "Obsidian Triumph" Strongbox | Permanent |  |
| 2516 | Where Exalted Dare | Permanent | 2373 |
| 2549 | Tarnished Traitor | Permanent |  |
| 2555 | Ultimate Challenge Winner | Permanent |  |
| 2565 | "Endurance" Strongbox | Permanent |  |
| 2568 | Forgotten City Arches | Permanent |  |
| 2574 | Treetop Retriever | Permanent |  |
| 2583 | "Slice of Sky" Strongbox | Permanent |  |
| 2594 | Mordrem Begone | Permanent |  |
| 2602 | No Mask Left Behind | Permanent |  |
| 2607 | A Fungus Among Us: Gold | Pvp, Permanent |  |
| 2614 | Invisible King | Permanent |  |
| 2617 | "Straight and Narrow" Strongbox | Permanent |  |
| 2618 | Ba-Boom | Permanent |  |
| 2622 | Saving the City of Gold | Permanent |  |
| 2633 | Sanctum Scramble: Silver | Pvp, Permanent |  |
| 2634 | Tarir Challenge Winner | Permanent |  |

## Dragon's Stand

[Official category: Dragon's Stand](https://api.guildwars2.com/v2/achievements/categories/109) / [Wiki](https://wiki.guildwars2.com/wiki/Dragon's_Stand_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 2160 | Pact Pilot Protector | Permanent |  |
| 2175 | Dragon Bombardier | Permanent |  |
| 2198 | Blademaster Diarmid Slayer | Permanent |  |
| 2214 | "Pride of Lion's Arch" Strongbox | Permanent |  |
| 2224 | Stavemaster Adryn Slayer | Permanent |  |
| 2243 | "Unsolved Conundrum" Strongbox | Permanent |  |
| 2256 | Prismatic Plunderer | Permanent |  |
| 2259 | Axemaster Hareth Slayer | Permanent |  |
| 2265 | Dragon's Stand Overviewer | Permanent |  |
| 2269 | Central Tower Taker | Permanent |  |
| 2275 | Enchanted Armor Wearer | Permanent |  |
| 2328 | Laser Lighter | Permanent |  |
| 2347 | Mushroom Musterer | Permanent |  |
| 2376 | Northern Tower Taker | Permanent |  |
| 2387 | Wallowing Whiz | Permanent |  |
| 2401 | Sum Viewer | Permanent |  |
| 2414 | Munition Re-Upper | Permanent |  |
| 2425 | Ley Line Glider | Permanent |  |
| 2439 | Shooting Star | Permanent |  |
| 2496 | Mouth of Mordremoth Master | Permanent |  |
| 2515 | "Legacy of Owl" Strongbox | Permanent |  |
| 2538 | "Dragonrender" Strongbox | Permanent |  |
| 2544 | "Scorchrazor II" Strongbox | Permanent |  |
| 2553 | Mouth of Mordremoth Slayer | Permanent |  |
| 2575 | Southern Tower Taker | Permanent |  |
| 2590 | Fire Jumper | Permanent |  |
| 2595 | Tamer of Wyverns | Permanent |  |
| 2601 | Prismatic Percher | Permanent |  |
| 2605 | Bat Wrangler | Permanent |  |

## Tangled Depths

[Official category: Tangled Depths](https://api.guildwars2.com/v2/achievements/categories/112) / [Wiki](https://wiki.guildwars2.com/wiki/Tangled_Depths_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 2151 | Gerent Slayer | Permanent |  |
| 2155 | Honorary Rata Novan | Permanent |  |
| 2172 | Cloak and Snagger | Permanent |  |
| 2173 | The Ley-Line Run: Gold | Pvp, Permanent |  |
| 2186 | Triple Mordrem Takedown | Permanent |  |
| 2207 | Disco Dancing Delver | Hidden, Permanent |  |
| 2210 | "Shard of Brilliance" Strongbox | Permanent |  |
| 2215 | Drone Race: Silver | Pvp, Permanent |  |
| 2230 | Scrap Rifle Field Test: Silver | Pvp, Permanent |  |
| 2233 | Chak Egg Scrambler | Permanent |  |
| 2237 | Regurgicidal | Permanent |  |
| 2251 | Roost Rouster | Permanent |  |
| 2261 | Ogre Lane Defender | Permanent |  |
| 2286 | Master Mushroom Spelunker | Permanent |  |
| 2293 | Nuhoch Lane Defender | Permanent |  |
| 2298 | The Ley-Line Run: Silver | Pvp, Permanent |  |
| 2299 | SCAR Supporter | Permanent |  |
| 2310 | Rata Novus Lane Defender | Permanent |  |
| 2321 | Pulse Room Glider | Permanent |  |
| 2323 | Ogre Airship Climber | Hidden, Permanent |  |
| 2326 | "Sword of Smodur" Strongbox | Permanent |  |
| 2334 | Drone Race: Gold | Pvp, Permanent |  |
| 2335 | Scrap Rifle Field Test: Gold | Pvp, Permanent |  |
| 2365 | "Cryptonym" Strongbox | Permanent |  |
| 2371 | Chak Crusher | Permanent |  |
| 2386 | Crystallized Cache Seeker | Permanent |  |
| 2430 | Haywire Punch-o-Matic Battle: Silver | Pvp, Permanent |  |
| 2436 | Dive Master: Chak Hive | Permanent |  |
| 2437 | "Whitebear's Pride II" Strongbox | Permanent |  |
| 2446 | "Plains of Golghein" Strongbox | Permanent |  |
| 2453 | Archeotech Adept | IgnoreNearlyComplete, Pvp, RepairOnLogin, RequiresUnlock, Permanent |  |
| 2459 | Elusive Elemental Eliminator | Hidden, Permanent |  |
| 2462 | The Longest Glide | Permanent |  |
| 2465 | Haywire Punch-o-Matic Battle: Gold | Pvp, Permanent |  |
| 2523 | SCAR Lane Defender | Permanent |  |
| 2526 | Beetle Feast: Silver | Pvp, Permanent |  |
| 2546 | Beetle Feast: Gold | Pvp, Permanent |  |
| 2554 | Champion Chak Hunter | Permanent |  |
| 2576 | Chak Bait | Permanent |  |
| 2579 | Lore Untangler | Permanent |  |
| 2603 | Lost Lab Locator | Hidden, Permanent |  |
| 2613 | Honorary Ogre | Permanent |  |
| 2615 | Potoni Masher | Permanent |  |
| 2625 | Friend of the Frogs | Permanent |  |

## Verdant Brink

[Official category: Verdant Brink](https://api.guildwars2.com/v2/achievements/categories/116) / [Wiki](https://wiki.guildwars2.com/wiki/Verdant_Brink_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 2157 | Tendril Torchers: Gold | Pvp, Permanent |  |
| 2165 | Raised the Bar | Permanent |  |
| 2203 | Honorary Jaka Itzel | Permanent |  |
| 2211 | Sky Stalker | Permanent |  |
| 2246 | Equitable Elector | Permanent |  |
| 2249 | "Glory of Tyria" Strongbox | Permanent |  |
| 2257 | Pact Camper | Permanent |  |
| 2276 | Shooting Gallery: Gold | Pvp, Permanent |  |
| 2281 | Ground Pounder | Permanent |  |
| 2294 | Tetrad Trouncer | Permanent |  |
| 2304 | Caught 'Em All | Permanent |  |
| 2307 | Pale Reaver Believer | Permanent |  |
| 2333 | Froglicker | Permanent |  |
| 2343 | Dive Master: Verdant Brink | Permanent |  |
| 2350 | Shooting Gallery: Silver | Pvp, Permanent |  |
| 2352 | Lord of the Jungle | Permanent |  |
| 2369 | Father of Wyverns | Permanent |  |
| 2423 | Mother of Wyverns | Permanent |  |
| 2424 | Tendril Torchers: Silver | Pvp, Permanent |  |
| 2429 | Diarmid Dropper | Permanent |  |
| 2431 | Ordnance Corps Auxiliary | Permanent |  |
| 2435 | Bugs in the Branches: Silver | Pvp, Permanent |  |
| 2460 | Bugs in the Branches: Gold | Pvp, Permanent |  |
| 2489 | Jungle Totem Hunter | Permanent | 2174 |
| 2494 | Salvage Pit: Silver | Pvp, Permanent |  |
| 2499 | Salvage Pit: Gold | Pvp, Permanent |  |
| 2505 | "Lethal Vantage" Strongbox | Permanent |  |
| 2510 | Excellent Judge of Character | Permanent |  |
| 2532 | Skritt Salvager | Permanent |  |
| 2540 | Flying Circus: Gold | Pvp, Permanent |  |
| 2541 | Patron of the Nobility | Permanent |  |
| 2543 | Ongoing Defense | Permanent |  |
| 2552 | "Mellaggan's Valor" Strongbox | Permanent |  |
| 2558 | Flying Circus: Silver | Pvp, Permanent |  |
| 2563 | Wartime Sommelier | Permanent |  |
| 2566 | Sky Commander | Permanent |  |
| 2570 | The Most Dangerous Game | Permanent |  |
| 2573 | Bronzer | Permanent |  |
| 2599 | Egg Run | Permanent |  |
| 2624 | "Thunderbreaker" Strongbox | Permanent |  |
| 2631 | "Faren's Flyer" Strongbox | Permanent |  |
| 2636 | Grassy Troll | Permanent |  |

## Bava Nisos

[Official category: Bava Nisos](https://api.guildwars2.com/v2/achievements/categories/455) / [Wiki](https://wiki.guildwars2.com/wiki/Bava_Nisos_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 8705 | Echo Evader | Permanent |  |
| 8708 | Two Birds | Permanent |  |
| 8709 | Ritualist Training—Part 2 | Permanent |  |
| 8713 | A Titanic Voyage | Permanent |  |
| 8718 | Demolition Expert | Permanent |  |
| 8721 | Sweet Relief | Permanent |  |
| 8724 | This Is Fine | Hidden, Permanent |  |
| 8735 | Vengeance Denied | Permanent |  |
| 8740 | Assorted Chaos | Permanent |  |
| 8747 | Spirit Nutritionist | Permanent |  |
| 8751 | Artillery Annihilator | Permanent |  |
| 8752 | Traversing the Titan | Permanent |  |
| 8755 | Close the Door | Permanent |  |
| 8756 | Mirror Memory Master | Permanent |  |
| 8767 | Separation Anxiety | Permanent |  |
| 8769 | Bava Nisos Mastery | CategoryDisplay, MoveToTop, Permanent |  |
| 8781 | Pure Soul | Permanent |  |
| 8785 | For Old Times' Sake | Permanent |  |
| 8809 | An Audible Voyage | Permanent |  |

## Janthir Syntri

[Official category: Janthir Syntri](https://api.guildwars2.com/v2/achievements/categories/430) / [Wiki](https://wiki.guildwars2.com/wiki/Janthir_Syntri_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 8155 | Janthir Syntri Adventure: Save Woodland Creatures | Permanent |  |
| 8157 | Fight Another Day | Permanent |  |
| 8164 | Sulfurous Springs: Titan Toppler | Permanent |  |
| 8172 | True Artist | Permanent |  |
| 8187 | Full Bloom | Permanent |  |
| 8193 | Hero of the Woods | Permanent |  |
| 8196 | Shard Scouter | Permanent |  |
| 8198 | Feed the Beast | Permanent |  |
| 8199 | Poetic Justice | Permanent |  |
| 8203 | Don't Drop That | Permanent |  |
| 8210 | Weather Conductor | Permanent |  |
| 8219 | Janthir Syntri Warclaw Run: Gold | Permanent |  |
| 8227 | Our Defenses Will Hold | Permanent |  |
| 8229 | Event Collection: Southeast Janthir Syntri | Permanent |  |
| 8234 | Janthir Syntri Adventure: River Mapping | Permanent |  |
| 8236 | Janthir Syntri Adventure: View From the Top | Permanent |  |
| 8237 | Janthir Syntri Warclaw Run: Silver | Permanent |  |
| 8241 | Event Collection: Central Janthir Syntri | Permanent |  |
| 8248 | Stronger as a Pack | Permanent |  |
| 8251 | Golden Rescue | Permanent |  |
| 8256 | Event Collection: Northeast Janthir Syntri | Permanent |  |
| 8270 | Janthir Syntri Adventure: Warclaw Run | Permanent |  |
| 8273 | Janthir Syntri Mastery | CategoryDisplay, MoveToTop, Permanent |  |
| 8280 | Squeaking to Safety | Permanent |  |
| 8281 | Island Adventurer | Permanent |  |
| 8289 | Janthir Cartographer | Permanent |  |
| 8299 | Close Call | Permanent |  |
| 8325 | Janthiri Smuggler | Permanent |  |
| 8334 | Firewatch | Permanent |  |
| 8335 | Master Forager: Meat | Permanent |  |
| 8337 | Mist Tide Turner | Permanent |  |
| 8348 | Event Collection: Southwest Janthir Syntri | Permanent |  |
| 8350 | Shield Trap | Permanent |  |
| 8356 | Struck Twice | Hidden, Permanent |  |
| 8357 | High Dive | Permanent |  |
| 8367 | Master Forager: Vegetables | Permanent |  |

## Lowland Shore

[Official category: Lowland Shore](https://api.guildwars2.com/v2/achievements/categories/431) / [Wiki](https://wiki.guildwars2.com/wiki/Lowland_Shore_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 8152 | Excrement Exterminator | Permanent |  |
| 8156 | What's That Sound? | Hidden, Permanent |  |
| 8158 | Buzzy Treetops | Permanent |  |
| 8159 | Scouting the Vale: Silver | Permanent |  |
| 8167 | Hide-and-Seek: Silver | Permanent |  |
| 8170 | Lowland Shore Diving Goggles | Permanent |  |
| 8173 | Life in the Lowlands | Permanent |  |
| 8177 | Feed the Flames | Hidden, Permanent |  |
| 8183 | Golden Mushroom Guru | Permanent |  |
| 8184 | Workplace Safety | Hidden, Permanent |  |
| 8188 | Moon Camp Covert Salmon Run: Silver | Permanent |  |
| 8192 | Very Enthusiastic about Wrestling | Permanent |  |
| 8194 | Hunting in the Grasslands | Permanent |  |
| 8197 | Salmon, Run! | Permanent |  |
| 8200 | Hide-and-Seek: Bronze | Permanent |  |
| 8202 | Warclaw Run Adventure: Bronze | Permanent |  |
| 8206 | Feeding Trolls | Permanent |  |
| 8207 | Social Distancing | Permanent |  |
| 8213 | Master Beekeeper | Permanent |  |
| 8218 | I Caught a HUGE Fish! | Permanent |  |
| 8222 | Relaxed and Rejuvenated | Permanent |  |
| 8230 | Lost in the Fight | Hidden, Permanent |  |
| 8242 | Competition Culture | Permanent |  |
| 8244 | Keeper of the Dance Floor | Hidden, Permanent |  |
| 8245 | Hive Hopper | Permanent |  |
| 8250 | Warclaw Run Adventure: Silver | Permanent |  |
| 8253 | Hide-and-Seek: Gold | Permanent |  |
| 8263 | Savant of Dance | Permanent |  |
| 8265 | Daily Buzzy Treetops | Daily | 8158 |
| 8275 | Lowland Shore Mastery | CategoryDisplay, MoveToTop, Permanent |  |
| 8282 | Friend of the Trolls | Permanent |  |
| 8286 | Pet the Wildlife | Permanent |  |
| 8288 | The Queen's Gambit | Permanent |  |
| 8291 | A Hard Day's Work | Permanent |  |
| 8293 | Hunting in the Wetlands | Permanent |  |
| 8294 | Troll Delicacy | Hidden, Permanent |  |
| 8297 | Pay Your Respects | Permanent |  |
| 8300 | Light Up the Vale | Permanent |  |
| 8301 | Moon Camp Covert Salmon Run: Gold | Permanent |  |
| 8302 | Feeding the Sharks | Permanent |  |
| 8303 | Harvest Shore Salmon Run: Silver | Permanent |  |
| 8304 | Daily Light Up the Vale | Daily | 8300 |
| 8306 | Friend of the Fish | Permanent |  |
| 8313 | Cultural Culinary Comprehension | Permanent |  |
| 8314 | Fungus Strikes Back | Permanent |  |
| 8318 | Mulch Master | Permanent |  |
| 8319 | Work with a Smile | Permanent |  |
| 8323 | Shore Creatures | Permanent |  |
| 8327 | Chasing Waterfalls: Lowland Shore | Permanent |  |
| 8332 | All the Queen's Men | Permanent |  |
| 8333 | Return to Nature | Permanent |  |
| 8338 | Moon Camp Covert Salmon Run: Bronze | Permanent |  |
| 8340 | Warclaw Run Adventure: Gold | Permanent |  |
| 8342 | Harvest Shore Salmon Run: Gold | Permanent |  |
| 8344 | Harvest Shore Salmon Run: Bronze | Permanent |  |
| 8354 | Scouting the Vale: Bronze | Permanent |  |
| 8358 | Something Fishy | Permanent |  |
| 8360 | Hunting in the Tundra | Permanent |  |
| 8361 | Rehearsal | Hidden, Permanent |  |
| 8362 | Scouting the Vale: Gold | Permanent |  |
| 8720 | That's What You Get | Hidden, Permanent |  |

## Mistburned Barrens

[Official category: Mistburned Barrens](https://api.guildwars2.com/v2/achievements/categories/446) / [Wiki](https://wiki.guildwars2.com/wiki/Mistburned_Barrens_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 8552 | Missing Scout | Permanent |  |
| 8555 | We Are the Champions | Permanent |  |
| 8560 | Flawless Crafter | Hidden, Permanent |  |
| 8562 | Hazardous Research: Gold | Permanent |  |
| 8566 | Thousandfold Mercy | Permanent |  |
| 8568 | Hazardous Research: Bronze | Permanent |  |
| 8569 | Down in the Valley | Permanent |  |
| 8572 | A Cappella | Hidden, Permanent |  |
| 8574 | Search and Destroy | Permanent |  |
| 8576 | Radioactive | Hidden, Permanent |  |
| 8577 | Demise of the Blood Phenom | Permanent |  |
| 8579 | Hazardous Research: Silver | Permanent |  |
| 8582 | Mistburned Barrens Mastery | RepairOnLogin, CategoryDisplay, MoveToTop, Permanent |  |
| 8585 | Scan and Soothe | Permanent |  |
| 8591 | Pro Scavenger | Permanent |  |
| 8592 | Into the Corridor | Permanent |  |
| 8593 | More Than a Little Bit | Permanent |  |
| 8595 | Boom! | Permanent |  |
| 8604 | Search-and-Rescue Challenge: Bronze | Permanent |  |
| 8606 | Be Free, Little Bot | Hidden, Permanent |  |
| 8620 | Silence the Screaming | Permanent |  |
| 8623 | Respectable Researcher | Permanent |  |
| 8624 | Restless No More | Permanent |  |
| 8634 | A Job for Warclaws | Permanent |  |
| 8637 | Search-and-Rescue Challenge: Gold | Permanent |  |
| 8638 | Hollow Shards | Permanent |  |
| 8640 | Search-and-Rescue Challenge: Silver | Permanent |  |

## Crystal Oasis

[Official category: Crystal Oasis](https://api.guildwars2.com/v2/achievements/categories/179) / [Wiki](https://wiki.guildwars2.com/wiki/Crystal_Oasis_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 3551 | Lost Pilgrims | Permanent |  |
| 3561 | Race to the Finish: Crystal Oasis | Permanent |  |
| 3570 | Reins of the Raptor | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent |  |
| 3574 | Crystal Oasis Griffon Master: Silver | Permanent | 3858 |
| 3599 | Up in Arms | Permanent |  |
| 3614 | Junkyard Weaponsmith | Permanent |  |
| 3615 | Crystal Oasis Griffon Expert: Silver | Permanent | 3709 |
| 3625 | Lost Lore of Crystal Oasis | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent |  |
| 3644 | A Trip Down Memory Lane | Permanent |  |
| 3718 | Refugee Supply Run: Silver | Permanent |  |
| 3729 | Crystal Oasis Griffon Expert: Gold | Permanent | 3709 |
| 3744 | Just a Sip | Permanent |  |
| 3747 | Refugee Supply Run: Gold | Permanent |  |
| 3764 | Crystal Oasis Legendary Bounties | Permanent |  |
| 3773 | Crystal Oasis Bounty Tour | Permanent |  |
| 3786 | Renowned Adventurer: Crystal Oasis | Permanent |  |
| 3832 | Crystal Oasis Griffon Master: Gold | Permanent | 3858 |
| 3850 | Crystal Oasis Champion Bounties | Permanent |  |
| 3862 | Bleached Bones | Permanent |  |

## Desert Highlands

[Official category: Desert Highlands](https://api.guildwars2.com/v2/achievements/categories/190) / [Wiki](https://wiki.guildwars2.com/wiki/Desert_Highlands_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 3550 | Desert Highlands Griffon Master: Silver | Permanent | 3858 |
| 3583 | Rune-locked Doors | Permanent |  |
| 3594 | Lost Lore of Desert Highlands | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent |  |
| 3596 | Dwarven Remnants | Permanent |  |
| 3609 | Freezing Leap | Permanent |  |
| 3654 | Night Lights | Permanent |  |
| 3678 | Highlands Bounty Tour | Permanent |  |
| 3680 | Desert Highlands Griffon Expert: Gold | Permanent | 3709 |
| 3687 | Cavalier Express: Silver | Permanent |  |
| 3689 | A Family Heirloom | Permanent |  |
| 3702 | Breaking the Bank: Vault 3 | Repeatable, Permanent | 3703 |
| 3703 | The Curious Bowl | Permanent |  |
| 3735 | Breaking the Bank: Vault 2 | Repeatable, Permanent | 3703 |
| 3739 | Renowned Adventurer: Desert Highlands | Permanent |  |
| 3741 | Race to the Finish: Desert Highlands | Permanent |  |
| 3742 | Breaking the Bank: Final Vault | Repeatable, Permanent | 3703 |
| 3743 | Desert Highlands Champion Bounties | Permanent |  |
| 3746 | Fire Dancer | Permanent |  |
| 3754 | Desert Highlands Legendary Bounties | Permanent |  |
| 3766 | Carrot Collector | Permanent |  |
| 3788 | Breaking the Bank: Vault 1 | Repeatable, Permanent | 3703 |
| 3789 | Cavalier Express: Gold | Permanent |  |
| 3794 | Nap Time | Permanent |  |
| 3823 | Smashing! | Permanent |  |
| 3827 | The Pied Piper | Permanent |  |
| 3831 | Speak in Riddles | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent |  |
| 3847 | Desert Highlands Griffon Master: Gold | Permanent | 3858 |
| 3860 | Bleeding Heart | Permanent |  |
| 3884 | Springer Backpacking | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent | 3567 |
| 3892 | Desert Highlands Griffon Expert: Silver | Permanent | 3709 |
| 3896 | Hidden Carrot Hunt | Permanent | 3766 |
| 3912 | The Lost Dolyak | Permanent |  |

## Domain of Vabbi

[Official category: Domain of Vabbi](https://api.guildwars2.com/v2/achievements/categories/174) / [Wiki](https://wiki.guildwars2.com/wiki/Domain_of_Vabbi_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 3555 | Lost Lore of the Domain of Vabbi | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent |  |
| 3556 | Domain of Vabbi Bounty Tour | Permanent |  |
| 3572 | Vehjin Supply Run: Gold | Permanent |  |
| 3617 | Vabbian Griffon Expert: Gold | Permanent | 3709 |
| 3628 | Kumaa the Feisty | Permanent |  |
| 3638 | Domain of Vabbi Legendary Bounties | Permanent |  |
| 3642 | Academy Supply Run: Silver | Permanent |  |
| 3643 | Kaadsseo the Wise | Permanent |  |
| 3646 | Necropolis Supply Run: Gold | Permanent |  |
| 3652 | Flying Finish | Permanent |  |
| 3653 | Ziadih the Fearless | Permanent |  |
| 3666 | Vabbian Griffon Master: Gold | Permanent | 3858 |
| 3667 | Zomi the Accomplished | Permanent |  |
| 3676 | Necropolis Supply Run: Silver | Permanent |  |
| 3690 | Garden Supply Run: Gold | Permanent |  |
| 3694 | Vabbian Griffon Expert: Silver | Permanent | 3709 |
| 3715 | Disrespect Your Elders | Permanent |  |
| 3732 | Scourge Buster | Permanent |  |
| 3752 | Renowned Adventurer: Domain of Vabbi | Permanent |  |
| 3765 | Vehjin Supply Run: Silver | Permanent |  |
| 3775 | Yoonam the Intrepid | Permanent |  |
| 3799 | Garden Supply Run: Silver | Permanent |  |
| 3809 | Dogs of War | Permanent |  |
| 3824 | Court Is Adjourned | Permanent |  |
| 3828 | Domain of Vabbi Champion Bounties | Permanent |  |
| 3836 | Yitfei the Light | Permanent |  |
| 3851 | Jilai the Radiant | Permanent |  |
| 3872 | Juaruadun the Flawless | Permanent |  |
| 3874 | Vabbian Griffon Master: Silver | Permanent | 3858 |
| 3883 | Junundu-Wurm Certified | Permanent |  |
| 3887 | Praise Joko! | Permanent |  |
| 3889 | Academy Supply Run: Gold | Permanent |  |
| 3891 | Junundu Master Certification | Permanent |  |
| 3924 | Serpent Slayer | Permanent |  |
| 3928 | Dispersed Energy | Permanent |  |

## Elon Riverlands

[Official category: Elon Riverlands](https://api.guildwars2.com/v2/achievements/categories/182) / [Wiki](https://wiki.guildwars2.com/wiki/Elon_Riverlands_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 3557 | Race to the Finish: Elon Riverlands | Permanent |  |
| 3571 | Doppel Dropper | Hidden, Permanent |  |
| 3578 | Renowned Adventurer: Elon Riverlands | Permanent |  |
| 3590 | Mysteries of the Exalted | Permanent |  |
| 3604 | Flameseeker Prophecies | Permanent |  |
| 3611 | Defector Protector | Permanent |  |
| 3629 | Forgotten Debris | Permanent |  |
| 3632 | Lost Lore of Elon Riverlands | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent |  |
| 3649 | Skimshallow Cove Supply Run: Gold | Permanent |  |
| 3658 | Elon River Dive Master | Permanent |  |
| 3669 | Magic Hunter | Hidden, Permanent |  |
| 3681 | Blood and Sand | Permanent |  |
| 3693 | Skimshallow Cove Supply Run: Silver | Permanent |  |
| 3699 | Ghostly Trio | Permanent |  |
| 3706 | Flowers for Jimoh | Permanent |  |
| 3707 | Skimmer Search | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent | 3627 |
| 3711 | Elon Riverlands Bounty Tour | Permanent |  |
| 3723 | Elon Riverlands Griffon Master: Gold | Permanent | 3858 |
| 3724 | Prison Breaker | Permanent |  |
| 3790 | Elon Riverlands Legendary Bounties | Permanent |  |
| 3801 | Augury Ascended | Permanent |  |
| 3817 | Elon Riverlands Griffon Expert: Gold | Permanent | 3709 |
| 3819 | Imposter Syndrome | Hidden, Permanent |  |
| 3826 | Frequent Forgotten Teleporter | Permanent |  |
| 3833 | Descension | Permanent |  |
| 3840 | Elon Riverlands Griffon Master: Silver | Permanent | 3858 |
| 3845 | Elon Riverlands Champion Bounties | Permanent |  |
| 3849 | Equipment Tracker | Hidden, Permanent |  |
| 3873 | Elon Riverlands Griffon Expert: Silver | Permanent | 3709 |

## The Desolation

[Official category: The Desolation](https://api.guildwars2.com/v2/achievements/categories/176) / [Wiki](https://wiki.guildwars2.com/wiki/The_Desolation_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 3552 | A Family's Sacrifice | Hidden, Permanent |  |
| 3558 | Desolation Griffon Expert: Gold | Permanent | 3709 |
| 3587 | Dance Till You Drop | Hidden, Permanent |  |
| 3593 | Path of the Gods | Permanent |  |
| 3618 | Shadow Sprinter | Permanent |  |
| 3633 | Lost Lore of the Desolation | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent |  |
| 3637 | Joko's Hidden Chamber | Permanent |  |
| 3663 | Shadow of a Shadow | Permanent |  |
| 3670 | A Soaring Stench | Permanent |  |
| 3677 | Shadow Patroller | Permanent |  |
| 3683 | Cleansing Tormented Remnants | Permanent | 3818 |
| 3691 | The Desolation Champion Bounties | Permanent |  |
| 3696 | Shadows Intel: Gold | Permanent |  |
| 3708 | Shadows Intel: Silver | Permanent |  |
| 3720 | The Throne of Bones | Permanent |  |
| 3728 | Honoring the Fallen | Permanent |  |
| 3731 | Full Rebel Assault | Permanent |  |
| 3737 | Shadows Provisions | Permanent |  |
| 3738 | Desolation Griffon Expert: Silver | Permanent | 3709 |
| 3740 | Race to the Finish: the Desolation | Permanent |  |
| 3759 | Acrid Springs Recovery | Permanent |  |
| 3771 | A Redeemer's Friend | Permanent | 3677 |
| 3774 | Junundu Whisperer | Permanent |  |
| 3781 | Desolation Griffon Master: Silver | Permanent | 3858 |
| 3782 | Realm-Portal Spiker | Permanent |  |
| 3804 | Bone Palace Pinnacle | Permanent |  |
| 3812 | The Desolation Bounty Tour | Permanent |  |
| 3825 | Renowned Adventurer: The Desolation | Permanent |  |
| 3837 | The Desolation Legendary Bounties | Permanent |  |
| 3857 | Sulfur Shooter | Permanent |  |
| 3859 | Desolation Griffon Master: Gold | Permanent | 3858 |
| 3871 | Jackal Reconnaissance | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent | 3818 |

## Amnytas

[Official category: Amnytas](https://api.guildwars2.com/v2/achievements/categories/366) / [Wiki](https://wiki.guildwars2.com/wiki/Amnytas_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 6972 | Bringing Balance | Permanent |  |
| 6974 | Nurture Knowledge | Permanent |  |
| 6981 | Continuous Cultivate Celestial | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7176 |
| 6983 | Never-Ending Nurture Knowledge | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 6974 |
| 6988 | Wrong Time, Wrong Place | Hidden, Permanent |  |
| 6990 | Knowledge of the Elders | Pvp, RepairOnLogin, Permanent |  |
| 6991 | Amnytas Mastery | CategoryDisplay, MoveToTop, Permanent |  |
| 7008 | Amnytas Diving Goggles | Permanent |  |
| 7025 | Sempiternal Solidifying Strength | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7208 |
| 7031 | Nonstop Nourish Natural | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7035 |
| 7034 | Fantastic Flying Foxes | Permanent |  |
| 7035 | Nourish Natural | Permanent |  |
| 7037 | The Waylit Lantern | RepairOnLogin, RequiresUnlock, Permanent |  |
| 7039 | Rank Doesn't Matter Here | Permanent |  |
| 7041 | Honorary Astral Ward | Pvp, RepairOnLogin, Permanent |  |
| 7049 | Scales of Dragrimmar | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent |  |
| 7053 | Illuminating Amnytas | IgnoreNearlyComplete, Repeatable, Permanent |  |
| 7068 | Stay Hydrated | Hidden, Permanent |  |
| 7102 | Tentacle Toppler | Permanent |  |
| 7106 | Chuck Out the Trash | Permanent |  |
| 7111 | Spire of the Forgotten | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent |  |
| 7131 | Astral Ward Research | Permanent |  |
| 7144 | Echoes of the Obscure | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent |  |
| 7152 | Omnipresent Oblige Obscure | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7222 |
| 7164 | No Rest for the Kryptis | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7195 |
| 7165 | Laugh Like Lyhr Is Watching | Hidden, Permanent |  |
| 7176 | Cultivate Celestial | Permanent |  |
| 7195 | The Healing of Amnytas | Permanent |  |
| 7205 | Boundless Bringing Balance | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 6972 |
| 7208 | Solidifying Strength | Permanent |  |
| 7210 | Jotun Skypiercer | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent |  |
| 7222 | Oblige Obscure | Permanent |  |
| 7224 | Bug-Zapped | Hidden, Permanent |  |
| 7229 | For a Rainy Day | Permanent |  |
| 7232 | Strength of the Unseen | IgnoreNearlyComplete, Pvp, RepairOnLogin, Permanent | 7089 |
| 7611 | Absolute Focus | Permanent |  |
| 7622 | Cruising Amnytas: Balance to Bastionmere | Permanent |  |
| 7624 | Bigger than You Remember... | Permanent |  |
| 7630 | Cruising Amnytas: Natural to Strength | Permanent |  |
| 7633 | Cruising Amnytas: Lyhr's Tower to Isgarren's Tower | Permanent |  |
| 8011 | Skyscale Target Practice in Amnytas: Silver | Permanent |  |
| 8046 | Amnytas Supply Run: Silver | Permanent |  |
| 8059 | Skyscale Target Practice in Amnytas: Master | Permanent |  |
| 8073 | Skyscale Target Practice in Amnytas: Gold | Permanent |  |
| 8099 | Amnytas Supply Run: Gold | Permanent |  |

## Inner Nayos

[Official category: Inner Nayos: Heitor's Territory](https://api.guildwars2.com/v2/achievements/categories/403) / [Wiki](https://wiki.guildwars2.com/wiki/Inner_Nayos:_Heitor's_Territory_(achievements))
[Official category: Inner Nayos: Nyedra Surrounds](https://api.guildwars2.com/v2/achievements/categories/409) / [Wiki](https://wiki.guildwars2.com/wiki/Inner_Nayos:_Nyedra_Surrounds_(achievements))
[Official category: Inner Nayos: Citadel of Zakiros](https://api.guildwars2.com/v2/achievements/categories/416) / [Wiki](https://wiki.guildwars2.com/wiki/Inner_Nayos:_Citadel_of_Zakiros_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 7653 | Looking Down from the Edge | Permanent |  |
| 7669 | Rift Bouncer | Permanent |  |
| 7687 | Follow the Leader | Permanent |  |
| 7689 | Frode's Journal | RepairOnLogin, Permanent |  |
| 7691 | Ignaxious Eradicator | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7711 |
| 7695 | Power Nap | Permanent |  |
| 7701 | Dead Air | Permanent |  |
| 7705 | Behind Demon Lines | Permanent |  |
| 7707 | Follow the Magic | Permanent |  |
| 7711 | Threat of Our Presence | Permanent |  |
| 7718 | No Chest Unopened | Permanent |  |
| 7719 | Snoren on the Job | Permanent |  |
| 7721 | Inner Nayos Mastery I | CategoryDisplay, MoveToTop, Permanent |  |
| 7722 | Rebuild and Destroy | Permanent |  |
| 7726 | Loyalist Harrier | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7705 |
| 7730 | Heitor Instigator | Permanent |  |
| 7732 | If It Ain't Broke | Permanent |  |
| 7774 | Inner Nayos: Nyedra, Dreamer's Sanctum Savior | Permanent |  |
| 7775 | Kryptis Veteran Vanquisher | Hidden, Permanent | 7825 |
| 7776 | Please Take a Seat | Permanent |  |
| 7777 | A Record of War: The Obscure | Permanent | 7825 |
| 7778 | Astral Express | Permanent |  |
| 7780 | Obstructor of Malice | Permanent |  |
| 7782 | Inner Nayos: Defiled Cradle Savior | Permanent |  |
| 7784 | A Record of War: The Celestial | Permanent | 7825 |
| 7787 | Emotional Barrier | Permanent |  |
| 7789 | Diving Goggles: Rock Top to Rock Bottom | Permanent |  |
| 7791 | Liberators and Subjugators | Permanent |  |
| 7793 | A Record of War: Strength | Permanent | 7825 |
| 7795 | Repeat Defanger | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7811 |
| 7797 | Better Consumer Than Consumed | Permanent |  |
| 7798 | (Repeatable) Inner Nayos: Nyedra Surrounds Savior | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7799 |
| 7799 | Inner Nayos: Nyedra Surrounds Savior | IgnoreNearlyComplete, Permanent |  |
| 7800 | Inner Nayos Mastery II | CategoryDisplay, MoveToTop, Permanent |  |
| 7801 | Defang the Fangs That Gnash | Permanent |  |
| 7803 | Turret Takedown | Permanent |  |
| 7806 | A Record of War: The Natural | Permanent | 7825 |
| 7807 | Follow the Magic II | Permanent |  |
| 7808 | Shrine Finder | Permanent |  |
| 7809 | Illuminating Inner Nayos | IgnoreNearlyComplete, Repeatable, Permanent |  |
| 7811 | The Fangs That Gnash | Permanent |  |
| 7812 | Told You So | Hidden, Permanent |  |
| 7816 | A Record of War: Balance | Permanent | 7825 |
| 7818 | Envious Reprieve | Permanent |  |
| 7821 | Sky Scorcher | Hidden, Permanent | 7825 |
| 7822 | Inner Nayos: The Old Settlement Savior | Permanent |  |
| 7824 | An Object in Motion | Permanent |  |
| 7827 | Bane of the Scorned | Permanent |  |
| 7830 | A Record of War | Permanent | 7825 |
| 7832 | A Record of War: Knowledge | Permanent | 7825 |
| 7834 | Inner Nayos: The Commons Savior | Permanent |  |
| 7835 | Tentacle Takedown | Permanent |  |
| 7837 | These Supplies Are Ours, Eparch. Ours! | Permanent |  |
| 7839 | Kryptis Champion Conqueror | Hidden, Permanent | 7825 |
| 7844 | A Gust of Clean Air | Permanent |  |
| 7845 | Skyscale Energizer | Hidden, Permanent | 7825 |
| 7846 | Not Like This Again | Permanent |  |
| 7847 | Quality Family Entertainment | Permanent |  |
| 7848 | Astral Miner | Hidden, RequiresUnlock, Permanent |  |
| 7852 | Inner Nayos: Stormcarved Hollows Savior | Permanent |  |
| 7853 | Itching for a Fight | Permanent |  |
| 7968 | Event Collection: Citadel of Zakiros | MoveToTop, Permanent |  |
| 7969 | (Repeatable) Event Collection: Citadel of Zakiros | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7968 |
| 7972 | Event Collection: Spire of Redemption | Permanent |  |
| 7973 | Missing Brood | RepairOnLogin, RequiresUnlock, Permanent | 8024 |
| 7979 | Who's a Good Kryptis? | Hidden, Permanent |  |
| 7980 | Kryptis Caretaker | Permanent |  |
| 7981 | First Journey into the Spider's Lair | Permanent |  |
| 7987 | Vialgos Vomit | Permanent |  |
| 7990 | Free Kryptis Essence: Gold | Permanent |  |
| 7995 | Nayos Recon Run: Silver | Permanent |  |
| 7996 | Skyscale Target Practice in Inner Nayos: Master | Permanent |  |
| 7998 | Reuniting Lost Kryptis: Gold | Permanent |  |
| 7999 | Amnytas Is Still Ours, Demons! | Permanent |  |
| 8001 | All the Feelings | Permanent |  |
| 8008 | No One Needs Another Nourys | Permanent |  |
| 8009 | Spellbombs Away | Permanent |  |
| 8022 | Threatened Consumer | Permanent |  |
| 8023 | Event Collection: The Midnight Abyss | Permanent |  |
| 8031 | Free Kryptis Essence: Silver | Permanent |  |
| 8034 | Nayos Recon Run: Gold | Permanent |  |
| 8036 | Skyscale Target Practice in Inner Nayos: Silver | Permanent |  |
| 8038 | Squad Interceptor | Permanent |  |
| 8041 | Event Collection: Spire of Creation | Permanent |  |
| 8045 | Jailbreak | Permanent |  |
| 8054 | Barely a Scratch | Permanent |  |
| 8069 | Big Mood | Permanent |  |
| 8071 | Inner Nayos Skirmish Squasher | Permanent |  |
| 8081 | Free Kryptis Essence: Master | Hidden, Permanent |  |
| 8082 | A Rift in Our Relationship | Permanent |  |
| 8090 | Reuniting Lost Kryptis: Silver | Permanent |  |
| 8091 | Inner Nayos Mastery III | CategoryDisplay, MoveToTop, Permanent |  |
| 8095 | Skyscale Target Practice in Inner Nayos: Gold | Permanent |  |
| 8096 | What Was Before | RepairOnLogin, RequiresUnlock, Permanent |  |
| 8098 | Extractor Eyesore | Permanent |  |

## Skywatch Archipelago

[Official category: Skywatch Archipelago](https://api.guildwars2.com/v2/achievements/categories/358) / [Wiki](https://wiki.guildwars2.com/wiki/Skywatch_Archipelago_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 6970 | Skyscale Target Practice in Skywatch Archipelago: Silver | Permanent |  |
| 6975 | Diving Goggles: Pillar Plunge | Permanent |  |
| 6987 | Let the Memory Live Again | Permanent |  |
| 6995 | Eternal Skywatch Archipelago: Unlocking the Wizard's Tower | IgnoreNearlyComplete, Pvp, Repeatable, Permanent | 7218 |
| 7001 | Knowing Is Half the Battle | Permanent |  |
| 7013 | Guided by Fate | Permanent |  |
| 7017 | Skywatch Archipelago Mastery | CategoryDisplay, MoveToTop, Permanent |  |
| 7021 | Skyscale Target Practice in Skywatch Archipelago: Master | Permanent |  |
| 7027 | Protector of Droknar's Light | Permanent |  |
| 7029 | Shelter In Place | Permanent |  |
| 7038 | Off to See the Wizard's Tower | Permanent |  |
| 7042 | Eternal Protector of the Skyward Marches | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7079 |
| 7055 | Rise and Shrine | Permanent |  |
| 7065 | Skyscale Target Practice in Skywatch Archipelago: Gold | Permanent |  |
| 7070 | Paper Trail | Permanent |  |
| 7079 | Protector of the Skyward Marches | Permanent |  |
| 7081 | Protector of the Beacon of Ages and Garenhoff | Permanent |  |
| 7090 | Island Discovery Tour | Permanent |  |
| 7092 | There and... | Permanent |  |
| 7095 | Protector of the Rata Novus Promenade and Primal Maguuma | Permanent |  |
| 7100 | Insect Incinerator | Permanent |  |
| 7119 | Eternal Off to See the Wizard's Tower | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7038 |
| 7126 | Illuminating Skywatch Archipelago | IgnoreNearlyComplete, Repeatable, Permanent |  |
| 7136 | Crate Keeper | Permanent |  |
| 7140 | Faith Is My Shield | Permanent |  |
| 7159 | Protector of Jade Mech Habitation Zone 03 | Permanent |  |
| 7179 | Eternal Protector of Jade Mech Habitation Zone 03 | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7159 |
| 7185 | Diving Goggles: Astral Dive | Permanent |  |
| 7191 | Eternal Protector of the Rata Novus Promenade and Primal Maguuma | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7095 |
| 7196 | Sleep Now in the Fire | Permanent |  |
| 7200 | Eternal Protector of Droknar's Light | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7027 |
| 7202 | ...Back Again | Permanent |  |
| 7204 | The Feeling Is Mutual | Permanent |  |
| 7218 | Skywatch Archipelago: Unlocking the Wizard's Tower | Permanent |  |
| 7220 | Ignorance Is Bliss | Permanent |  |
| 7230 | Diving Goggles: Free Fall of New Kaineng | Permanent |  |
| 7239 | Only the Strong Survive | Permanent |  |
| 7241 | Eternal Protector of the Beacon of Ages and Garenhoff | IgnoreNearlyComplete, Pvp, RepairOnLogin, Repeatable, Permanent | 7081 |
| 7248 | Stargaze Ridge Skyscale Ride | Permanent |  |
| 7379 | Don't Think Twice | Permanent |  |

## The Wizard's Tower

[Official category: The Wizard's Tower](https://api.guildwars2.com/v2/achievements/categories/357) / [Wiki](https://wiki.guildwars2.com/wiki/The_Wizard's_Tower_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 6960 | Wizard's Trial Race | Permanent |  |
| 6962 | Zojja's Journal: Skyward Marches | RequiresUnlock, Permanent |  |
| 6965 | Secrets Obscured | Pvp, RepairOnLogin, RequiresUnlock, Permanent | 7172 |
| 6969 | Zojja's Journal: Primal Maguuma | RequiresUnlock, Permanent |  |
| 6971 | Hide-and-Seek in the Wizard's Tower | Permanent |  |
| 6973 | Flashing into Focus | Hidden, Permanent |  |
| 6979 | Comrades in Arms | Pvp, RepairOnLogin, Permanent | 7089 |
| 6982 | Wizard's Tower: Skyscale Target Practice—Silver | Permanent |  |
| 6989 | Zojja's Journal: Devastated Garenhoff | RequiresUnlock, Permanent |  |
| 6994 | Wizard's Tower Diving Goggles | Permanent |  |
| 7009 | Wizard's Tower: Fly by Night—Gold | Permanent |  |
| 7019 | Wizard's Tower: Skyscale Target Practice—Master | Permanent |  |
| 7024 | Keep It Up | Permanent |  |
| 7048 | Sorrow's Lost | Pvp, RepairOnLogin, RequiresUnlock, Permanent |  |
| 7059 | A Promise Kept | Hidden, Permanent |  |
| 7066 | Wizard's Tower: Fly by Night—Silver | Permanent |  |
| 7083 | Zojja's Journal | RepairOnLogin, RequiresUnlock, Permanent |  |
| 7097 | Wizard's Tower: Skyscale Target Practice—Gold | Permanent |  |
| 7103 | Zojja's Journal: Droknar's Light | RequiresUnlock, Permanent |  |
| 7107 | Wizard's Tower Trial: Silver | Permanent |  |
| 7148 | Hide-and-Seek in the Wizard's Tower: Master | Permanent |  |
| 7151 | Secrets Unobscured | Hidden, Permanent |  |
| 7170 | Wizard's Tower Trial: Bronze | Permanent |  |
| 7173 | Wizard's Tower Trial: Gold | Permanent |  |
| 7192 | Wizard's Tower Trial | Permanent |  |
| 7199 | Zojja's Journal: Rata Novus Promenade | RequiresUnlock, Permanent |  |
| 7207 | Zojja's Journal: Jade Mech Habitation Zone 03 | RequiresUnlock, Permanent |  |
| 7664 | You Buy | Hidden, Permanent |  |
| 7948 | Tyrian Taste Testing | RequiresUnlock, Permanent | 8024 |
| 7958 | Salute the Shopkeeper | Hidden, Permanent |  |
| 7989 | Gape into the Abyss | Pvp, RequiresUnlock, Permanent |  |
| 8004 | Thornsprout Boom! | Hidden, Permanent |  |
| 8053 | Consternation with Conri | Hidden, Permanent |  |

## Eternity's Garden

[Official category: Eternity's Garden](https://api.guildwars2.com/v2/achievements/categories/482) / [Wiki](https://wiki.guildwars2.com/wiki/Eternity's_Garden_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 9245 | Into the Cellar | Hidden, Permanent |  |
| 9247 | The Folly of Hermitage | Permanent |  |
| 9248 | Master of Sacred Arms | Permanent |  |
| 9249 | Otter Snack Time | Hidden, Permanent |  |
| 9251 | Fits like a Glove | Permanent |  |
| 9252 | Eternal Watch | Permanent |  |
| 9254 | Skimmer Relic Scour Adventure: Gold | Permanent |  |
| 9255 | No Longer Alone | Hidden, Permanent |  |
| 9257 | Respect for the Ancients | Permanent |  |
| 9258 | Kitshark Entertainment | Permanent |  |
| 9259 | Unwavering | Permanent |  |
| 9264 | The Hard Choice | Permanent |  |
| 9265 | Eternity's Garden Mastery | CategoryDisplay, MoveToTop, Permanent |  |
| 9270 | Unexpected Allies | Permanent |  |
| 9273 | Arcane Preservation | Permanent |  |
| 9277 | Beetle Research | Permanent |  |
| 9280 | Kitshark Adventure: Master | Permanent |  |
| 9281 | Arcane Certification | Permanent |  |
| 9285 | Skimmer Relic Scour Adventure: Silver | Permanent |  |
| 9287 | Kitshark Adventure: Silver | Permanent |  |
| 9289 | Rage of the Forest | Permanent |  |
| 9290 | Artificer's Rise Jumping Puzzle | Permanent |  |
| 9291 | Daily Artificer's Rise Jumping Puzzle | Daily | 9290 |
| 9294 | Gregorios the Beautiful | Permanent |  |
| 9295 | Lost in Translation | Permanent |  |
| 9296 | Cruel Creations | Permanent |  |
| 9297 | A Crustacean Calamity | Permanent |  |
| 9298 | Castoran Overgrowth | Permanent |  |
| 9302 | Attentive Audience | Permanent |  |
| 9304 | Path of the Divine | Permanent |  |
| 9305 | Daily Munchin' Moths | Daily | 9327 |
| 9306 | Revitalizing the Forge | Permanent |  |
| 9307 | Bouncer | Hidden, Permanent |  |
| 9309 | Sacking the Inquest | Permanent |  |
| 9311 | Kitshark Adventure: Gold | Permanent |  |
| 9314 | A Brief Reprieve | Permanent |  |
| 9315 | Risky Research | Permanent |  |
| 9321 | Scholar of the Garden | Permanent |  |
| 9322 | Protector of the Mothmarsh | Permanent |  |
| 9324 | Shepherd of the Garden | Permanent |  |
| 9325 | Calculated Destruction | Permanent |  |
| 9327 | Munchin' Moths | Permanent |  |
| 9328 | These Cursed Halls | Permanent |  |
| 9329 | Inquest Instigator | Permanent |  |
| 9337 | Moth Enthusiast | Hidden, Permanent |  |
| 9338 | Divine Historian | Permanent |  |
| 9341 | Questionable Choices | Permanent |  |

## Leyspring Hollows

[Official category: Leyspring Hollows](https://api.guildwars2.com/v2/achievements/categories/486) / [Wiki](https://wiki.guildwars2.com/wiki/Leyspring_Hollows_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 9351 | Hobby Aquaculturist | Permanent |  |
| 9355 | Tribute to the Hungry | Permanent |  |
| 9356 | Artillery Disrupter | Permanent |  |
| 9360 | Fishy Barrage | Permanent |  |
| 9366 | Terminal Tampering | Permanent |  |
| 9367 | Steward of the Elders | Permanent |  |
| 9372 | Introspection | Permanent |  |
| 9374 | Wailer's Pulpit Usher | Permanent |  |
| 9377 | Historian of the Leyspring | Permanent |  |
| 9383 | Faithful Primo Uomo | Permanent |  |
| 9390 | Amateur Mycologist | Permanent |  |
| 9392 | Serpent Simulator: Silver | Permanent |  |
| 9393 | Speleologist | Permanent |  |
| 9399 | Forever Rooted | Hidden, Permanent |  |
| 9401 | Bane of Inquest | Permanent |  |
| 9407 | Captivated Audience | Hidden, Permanent |  |
| 9408 | Orb Diver | Permanent |  |
| 9410 | Daily Inquest Cache Jumping Puzzle | Daily |  |
| 9415 | Serpent Simulator: Gold | Permanent |  |
| 9417 | Leyspring Hollows Mastery | RepairOnLogin, CategoryDisplay, MoveToTop, Permanent |  |
| 9420 | Natural-Born Beetle | Permanent |  |
| 9424 | Specimen Savior | Permanent |  |
| 9425 | Influential Saboteur | Permanent |  |
| 9427 | Daily Ruins to Riches Minidungeon | Daily | 9466 |
| 9428 | Above and Beyond Security | Hidden, Permanent |  |
| 9430 | The Helmsmen of the Leyspring | Permanent |  |
| 9431 | Steward Chromotherapy | Permanent |  |
| 9434 | Hall of Assemblage Custodian | Permanent |  |
| 9438 | Protector of Meaning | Permanent |  |
| 9439 | No Teleportation Needed | Permanent |  |
| 9441 | Inquest Cache Jumping Puzzle | Permanent |  |
| 9442 | Spick-and-Span | Hidden, Permanent |  |
| 9443 | Coleopteran Cavern Completionist | Permanent |  |
| 9446 | Big Chak, Big Trap | Permanent |  |
| 9448 | Aetherlocation Detective: Gold | Permanent |  |
| 9452 | Slapdash Delivery | Permanent |  |
| 9455 | Steward Crash Course | Permanent |  |
| 9457 | Daughter of Misrule | Permanent |  |
| 9460 | The Tail End | Hidden, Permanent |  |
| 9462 | Expressive | Permanent |  |
| 9464 | Dexterous Courier | Permanent |  |
| 9465 | Aetherlocation Detective: Silver | Permanent |  |
| 9466 | A Thief Full of Pluck | Permanent |  |
| 9467 | Daily Coleopteran Cavern Jumping Puzzle | Daily | 9468 |
| 9468 | Coleopteran Cavern Jumping Puzzle | Permanent |  |
| 9470 | On Behalf of the Alliance | Permanent |  |
| 9473 | Son of Misrule | Hidden, Permanent |  |
| 9474 | Progeny of Misrule | Hidden, Permanent |  |

## Shipwreck Strand

[Official category: Shipwreck Strand](https://api.guildwars2.com/v2/achievements/categories/463) / [Wiki](https://wiki.guildwars2.com/wiki/Shipwreck_Strand_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 8860 | Skimmer-Net Scramble: Gold | Permanent |  |
| 8861 | The Lesser-Known Leaders of Shipwreck Strand | Permanent |  |
| 8865 | Daily Orb Cavern Jumping Puzzle | Daily | 8932 |
| 8873 | Grotto Aficionado | Hidden, Permanent |  |
| 8875 | Aquatic Prison Break | Permanent |  |
| 8880 | Shipwreck Strand Mastery | CategoryDisplay, MoveToTop, Permanent |  |
| 8882 | Freebooter Initiate | Permanent |  |
| 8893 | Hobbies of the Hullgardeners | Permanent |  |
| 8894 | Tropical Tomes | Permanent |  |
| 8898 | Juke Jessica | Permanent |  |
| 8903 | Bar Bouncer | Permanent |  |
| 8914 | Juke Jimmy | Permanent |  |
| 8921 | Glimmering Arches Grand Prix: Gold | Permanent |  |
| 8924 | Glimmering Arches Grand Prix: Silver | Permanent |  |
| 8926 | In Loving Memory | Permanent |  |
| 8930 | Daily Soaring Copse Jumping Puzzle | Daily | 8976 |
| 8932 | Orb Cavern Jumping Puzzle | Permanent |  |
| 8934 | In a Pinch | Permanent |  |
| 8935 | Give 'Em the Boot | Permanent |  |
| 8950 | Ponder the Pools | Permanent |  |
| 8951 | Attendant of the Month | Permanent |  |
| 8953 | Hidden Quiggles | Hidden, Permanent |  |
| 8957 | Do Feed the Wavehawks | Permanent |  |
| 8963 | Plague Doctor | Permanent |  |
| 8964 | Teleporting Isn't Sporting | Permanent |  |
| 8968 | Minimum Liability | Permanent |  |
| 8971 | Ghosts Need Friends Too | Permanent |  |
| 8976 | Soaring Copse Jumping Puzzle | Permanent |  |
| 8977 | Daily 'Booter's Path Jumping Puzzle | Daily | 8882 |
| 8981 | Wavehawk Scritcher | Permanent |  |
| 8983 | Skimmer-Net Scramble Master | Permanent |  |
| 8989 | Proper Mixologist | Permanent |  |
| 8991 | Feeling Loopy | Permanent |  |
| 8992 | Not Even a Scratch | Permanent |  |
| 8998 | King Crab of Castora | Permanent |  |
| 8999 | Soaring Sands Fireworks: Silver | Permanent |  |
| 9001 | Dog Trainer | Permanent |  |
| 9010 | Await the Offgoing! | RepairOnLogin, Permanent |  |
| 9011 | Inquest Pest | Permanent |  |
| 9016 | Swearing Off the Poison | Permanent |  |
| 9020 | Skimmer-Net Scramble: Silver | Permanent |  |
| 9026 | Salty Sous-Chef | Permanent |  |
| 9032 | Cover the Castaway Crew | Permanent |  |
| 9037 | Dedicated Diver | Permanent |  |
| 9046 | Brave Drinker | Hidden, Permanent |  |
| 9051 | Shipwreck Strand's Freshest Water | Permanent |  |
| 9052 | Paxx's Favorite Patron | Permanent |  |
| 9054 | Converse with Samantha | Permanent |  |
| 9058 | Soaring Sands Fireworks: Gold | Permanent |  |
| 9059 | Seafood Connoisseur | Permanent |  |
| 9071 | Hammered the Hammerharts | Permanent |  |
| 9081 | Help the Thirsty Old Captain | Hidden, Permanent |  |
| 9082 | As Above, So Below | Permanent |  |

## Starlit Weald

[Official category: Starlit Weald](https://api.guildwars2.com/v2/achievements/categories/472) / [Wiki](https://wiki.guildwars2.com/wiki/Starlit_Weald_(achievements))

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 8856 | Wavehawk Savior | Permanent |  |
| 8862 | Lost No Longer | Permanent |  |
| 8866 | Inquest Training Speed Runner | Permanent |  |
| 8867 | Read the Room | Permanent |  |
| 8881 | Sketch Artist | Permanent |  |
| 8884 | Starlit Weald Ley Line Adventure: Silver | Permanent |  |
| 8886 | Escape Artist: Defense Systems | Permanent |  |
| 8902 | Rampage Router | Permanent |  |
| 8904 | Great Choya Race: Bronze | Permanent |  |
| 8909 | Sylvan Shapeshifter | Permanent |  |
| 8911 | Daily Birdie Benefactor | Daily | 9028 |
| 8917 | Ancient Investigator | Permanent |  |
| 8918 | Secret Spelunker | Permanent |  |
| 8920 | Wavehawk Delivery | Permanent |  |
| 8922 | No-Hit Run | Permanent |  |
| 8933 | Leading from the Front | Permanent |  |
| 8937 | Starlit Tourist | Permanent |  |
| 8938 | Huntmaster of Castora | Permanent |  |
| 8941 | Tread Lightly | Hidden, Permanent |  |
| 8942 | Back to Sleep | Permanent |  |
| 8952 | Meandering Magic | Permanent |  |
| 8967 | Choya Language Expert | Permanent |  |
| 8982 | Dubious Exit | Hidden, Permanent |  |
| 8986 | Sebb Subverter | Permanent |  |
| 8996 | Treasures of the Last Vault | Permanent |  |
| 9000 | Choya Champion | Permanent |  |
| 9003 | Orb Hopper | Permanent |  |
| 9007 | Backdoor Exploit | Hidden, Permanent |  |
| 9008 | Inquest Hologram | Permanent |  |
| 9018 | Old Magic: Gold | Permanent |  |
| 9022 | Emergent Metamorphosis | Pvp, RepairOnLogin, Permanent |  |
| 9025 | Sidony's Revenge | Permanent |  |
| 9027 | Great Choya Race: Silver | Permanent |  |
| 9028 | Birdie Benefactor | Permanent |  |
| 9033 | Soup's On | Permanent |  |
| 9035 | Old Magic: Silver | Permanent |  |
| 9039 | Starlit Weald Ley Line Adventure: Gold | Permanent |  |
| 9040 | Starlit Weald Ley Line Adventure: Bronze | Permanent |  |
| 9041 | Daily Inquest Hologram | Daily |  |
| 9042 | Can't Fool Me | Permanent |  |
| 9045 | Grilling Buddies | Permanent |  |
| 9047 | Cuckoo Clock | Permanent |  |
| 9049 | Great Choya Race: Gold | Permanent |  |
| 9055 | Daily Meandering Magic | Hidden, Daily | 8952 |
| 9057 | Starlit Weald Mastery | CategoryDisplay, MoveToTop, Permanent |  |
| 9061 | Skimming off the Top | Permanent |  |
| 9062 | Choya Momentum | Permanent |  |
| 9069 | Dubious Dancing | Hidden, Permanent |  |
| 9072 | Forest Caretaker | Permanent |  |
| 9074 | Egg Protector | Permanent |  |
| 9077 | Project Bodyguard | Permanent |  |
| 9078 | On Second Thought... | Hidden, Permanent |  |
| 9083 | Inquest Saboteur | Permanent |  |

## Living World Season 1 — separate episode categories

These nine Story Journal categories are not map totals and never enter automatic map counts. They include side categories alongside the five rereleased main episodes. Category membership does not prove every legacy entry is currently obtainable; original and rereleased achievements may coexist. Festivals and historical-group categories are excluded.

| Category | API ID | Entries |
|---|---:|---:|
| Flame and Frost | 328 | 28 |
| Sky Pirates | 329 | 43 |
| Clockwork Chaos | 43 | 34 |
| Emissary Vorpp's Field Assistant | 44 | 6 |
| Tower of Nightmares | 53 | 32 |
| The Nightmares Within | 54 | 11 |
| The Nightmare Is Over | 56 | 12 |
| Escape from Lion's Arch | 62 | 23 |
| The Battle for Lion's Arch | 65 | 39 |

### Flame and Frost

[Official category](https://api.guildwars2.com/v2/achievements/categories/328)

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 460 | Refugee Volunteer | Permanent |  |
| 461 | The Gathering Storm | Permanent |  |
| 536 | Lost and Found | Permanent |  |
| 537 | Secret Contact | Permanent |  |
| 539 | Rox: Critical Mission | Permanent |  |
| 540 | Rox - The Hatchery | Permanent | 539 |
| 541 | Braham: Help from the Legions | Permanent |  |
| 542 | Braham - Retake Cragstead | Permanent | 543 |
| 543 | Braham - Eirsson | Permanent |  |
| 544 | Hero's Aid | Permanent |  |
| 569 | Rage Against the War Machine | Permanent |  |
| 570 | Avenger of the Dispossessed | Permanent |  |
| 571 | Alliance Breaker | RepairOnLogin, Permanent |  |
| 572 | A Rallying Flame | Permanent |  |
| 6524 | Fractal Recursion: Molten Boss | Permanent | 6536 |
| 6528 | Ready Ore Not | Permanent |  |
| 6529 | Molten Furnace | Permanent |  |
| 6531 | Fractal Recursion: Molten Furnace | Permanent | 6536 |
| 6533 | New Friends, New Enemies | Permanent |  |
| 6535 | Investigative Study 1 | Permanent |  |
| 6536 | A Quiet Celebration | Permanent |  |
| 6538 | Alliance Investigation | Permanent |  |
| 6539 | Flame and Frost Mastery | Pvp, RepairOnLogin, CategoryDisplay, Permanent |  |
| 6547 | Against the Alliance | Permanent |  |
| 6548 | Molten Memorial | Pvp, RepairOnLogin, Permanent |  |
| 6553 | The Battle for Cragstead | Permanent |  |
| 6554 | Guiding Sign | Permanent |  |
| 6780 | Against the Alliance 2 | Permanent | 6547 |

### Sky Pirates

[Official category](https://api.guildwars2.com/v2/achievements/categories/329)

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 662 | Case Closed (2013) | MoveToTop, Permanent |  |
| 663 | Hard Boiled (2013) | Permanent |  |
| 664 | Ceremony and Acrimony (2013) | Permanent |  |
| 665 | Every Piece Matters (2013) | Permanent |  |
| 666 | No More Secrets (2013) | Permanent |  |
| 667 | Against the Aetherblades | MoveToTop, Permanent |  |
| 668 | Caching Out | MoveToTop, Permanent |  |
| 669 | Mad Cache | Permanent |  |
| 670 | Cantle Cache | Permanent |  |
| 671 | Shipshape Cache | Permanent |  |
| 672 | Blackout Cache | Permanent |  |
| 673 | Vexing Cache | Permanent |  |
| 674 | Weeping Cache | Permanent |  |
| 675 | Troll Cache | Permanent |  |
| 676 | Aether Apprehender: Tyria | Permanent |  |
| 677 | Personal Space | Permanent |  |
| 678 | Unfriendly Skies | Permanent |  |
| 679 | Don't Be Rude to the Brute | Permanent |  |
| 681 | Questions for Mai | Permanent |  |
| 682 | Faster Than Light | Permanent |  |
| 683 | Equipment Failure | Permanent |  |
| 684 | Aether Apprehender: Kryta | Permanent |  |
| 685 | Aether Apprehender: Fractals of the Mists | Permanent |  |
| 686 | Aether Apprehender: The Aetherblade Retreat | Permanent |  |
| 688 | Cornered, Caught, Collared (2013) | Permanent |  |
| 689 | Aetherblade Assassin | Permanent |  |
| 6556 | Ceremony Survivor | Permanent |  |
| 6557 | Patrolling the Bloodtide Beat | Permanent |  |
| 6559 | The Aetherblade Retreat | Permanent |  |
| 6560 | Investigative Study 2 | Permanent |  |
| 6561 | Asset Recovery | Permanent |  |
| 6563 | Check, First Mate | Permanent |  |
| 6564 | Sky Pirates Mastery | Pvp, RepairOnLogin, CategoryDisplay, Permanent |  |
| 6565 | Plundering the Sky Pirates | Permanent | 6566 |
| 6566 | Case Closed | Permanent |  |
| 6567 | Tassi Master | Permanent |  |
| 6568 | Fractal Recursion: Aetherblade Retreat | Permanent | 6566 |
| 6569 | No More Secrets | Permanent |  |
| 6570 | Hard Boiled | Permanent |  |
| 6572 | Fractal Recursion: Captain Mai Trin | Permanent | 6566 |
| 6574 | Ceremony and Acrimony | Permanent |  |
| 6577 | Aether Investigation | Permanent |  |
| 6810 | Patrolling the Bloodtide Beat 2 | Permanent | 6557 |

### Clockwork Chaos

[Official category](https://api.guildwars2.com/v2/achievements/categories/43)

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 771 | Opening Ceremony Attendee | Hidden, Permanent |  |
| 815 | Defender of the Crown | Permanent |  |
| 816 | Soft Lander | Permanent |  |
| 817 | Playhouse Perfectionist | Permanent |  |
| 818 | Raced to the Rescue | Permanent |  |
| 819 | Clockwork Chaos Completionist | RepairOnLogin, Permanent |  |
| 820 | Closing Ceremony Attendee | Permanent |  |
| 827 | Portal Closer | Permanent |  |
| 828 | Swift Closer | Permanent |  |
| 829 | Watchwork Nightmare Wrecker | Permanent |  |
| 830 | Molten Invader Menace | Permanent |  |
| 831 | Scarlet Scrambler | Permanent |  |
| 832 | Indiscriminate Adversary | Permanent |  |
| 833 | Bane of Invading Captains | Permanent |  |
| 834 | Friend of Fire and Frost | Permanent |  |
| 835 | Worldwide Invasion Responder | Permanent |  |
| 836 | Invasion Canceler | Permanent |  |
| 837 | Was a Watchknight | Permanent |  |
| 6682 | Clockwork Chaos Mastery | Pvp, RepairOnLogin, CategoryDisplay, Permanent |  |
| 6683 | Daily Portal Closer | Daily |  |
| 6684 | Clockwork Invasion | Permanent |  |
| 6685 | Investigative Record 1 | Permanent |  |
| 6686 | Scarlet's Playhouse | Permanent |  |
| 6687 | Spoils of Chaos | Permanent |  |
| 6688 | Picking Up the Pieces | Permanent |  |
| 6689 | The Opening Ceremony | Permanent |  |
| 6690 | Investigative Study 3 | Permanent |  |
| 6691 | Deft Defusing | Permanent |  |
| 6692 | Seeking Scarlet: Twilight Arbor Aetherpath | Permanent | 6688 |
| 6693 | The Higher Road | Permanent |  |
| 6694 | The Queen's Address | Permanent |  |
| 6695 | Kryta's Finest | Permanent |  |
| 6696 | Guarding the Fields | Permanent |  |
| 6809 | Guarding the Fields 2 | Permanent | 6696 |

### Emissary Vorpp's Field Assistant

[Official category](https://api.guildwars2.com/v2/achievements/categories/44)

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 821 | Teleportation Facilitator | Permanent |  |
| 822 | First Portal Invasion Responder | Permanent |  |
| 823 | Invasion Witness Interviewer | Permanent |  |
| 824 | Portal Invasion Closer | Permanent |  |
| 825 | Portal Component Procurer | Permanent |  |
| 826 | Emissary Vorpp's Field Assistant | RepairOnLogin, Permanent |  |

### Tower of Nightmares

[Official category](https://api.guildwars2.com/v2/achievements/categories/53)

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 1089 | Toxic Spore Sampler | Permanent |  |
| 1090 | Toxic Global Gardener | Permanent |  |
| 1092 | Toxic Krait Historian | Permanent | 6763 |
| 1093 | Toxic Weed Whacker | Permanent |  |
| 1094 | Toxic Demolitionist Gardener | Permanent |  |
| 1095 | Toxic Siege Gardener | Permanent |  |
| 1096 | Toxic Golem Gardener | Permanent |  |
| 1097 | Toxic Spore Cleanser | Permanent |  |
| 1098 | Krait Bane | Permanent |  |
| 1099 | The Nightmare Unveiled Mastery | RepairOnLogin, Permanent |  |
| 1101 | Toxic Alliance Slayer | Permanent |  |
| 1102 | The Nightmare Unveiled (Historical) | Permanent |  |
| 6747 | Kraitmare Averted, Again | Permanent |  |
| 6748 | Fight at the Finish | Permanent |  |
| 6749 | The Nightmare Incarnate | Permanent |  |
| 6750 | The Tower of Nightmares | Permanent |  |
| 6751 | Making the Antitoxin | Permanent |  |
| 6752 | The Nightmare Ends | Permanent |  |
| 6753 | Tower Purifier | Permanent |  |
| 6754 | Tower of Nightmares Mastery | Pvp, RepairOnLogin, CategoryDisplay, Permanent |  |
| 6755 | The Nightmare Unveiled | Permanent |  |
| 6756 | Investigative Study 4 | Permanent |  |
| 6757 | Seeking Scarlet: Twisted Marionette | Permanent | 6758 |
| 6758 | Awake and Allied | Permanent |  |
| 6759 | Nightmare Climber | Permanent |  |
| 6760 | Investigative Record 2 | Permanent |  |
| 6761 | Kraitmare Averted | Permanent |  |
| 6762 | Tower of Treasures | Permanent |  |
| 6763 | Toxic Krait Transcriber | Permanent |  |
| 6764 | Environmental Protection | Permanent |  |
| 6779 | Seeking Scarlet: Thaumanova Reactor | Permanent | 6758 |
| 6806 | Tower Purifier 2 | Permanent | 6753 |

### The Nightmares Within

[Official category](https://api.guildwars2.com/v2/achievements/categories/54)

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 1131 | Tower Antitoxin Injector | Permanent |  |
| 1132 | The Nightmares Within Mastery | RepairOnLogin, CategoryDisplay, Permanent |  |
| 1133 | The Nightmares Within | Permanent |  |
| 1134 | Tower of Nightmares Survivor | Permanent |  |
| 1135 | Tower Hybrid Slayer | Permanent | 1131 |
| 1136 | Tower Explorer | Permanent |  |
| 1137 | Tower Nemesis | Permanent |  |
| 1138 | Tower Hybrid Master | Permanent | 1131 |
| 1139 | Tower of Nightmares High Diver | Permanent |  |
| 1140 | Tower of Nightmares Diver | Permanent |  |
| 1141 | Tower Treasure Hunter | Permanent |  |

### The Nightmare Is Over

[Official category](https://api.guildwars2.com/v2/achievements/categories/56)

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 1100 | Nightmare Ender | Permanent |  |
| 1199 | Aftermath Treasure Hunter | Permanent |  |
| 1200 | Aftermath Viathan Cleaner | Permanent |  |
| 1201 | Aftermath Arachnicide | Permanent |  |
| 1202 | Nightmare's Aftermath Mastery | Pvp, RepairOnLogin, CategoryDisplay, Permanent |  |
| 1203 | Aftermath Cobweb Cleaner | Permanent |  |
| 1204 | Aftermath Vermicide | Permanent |  |
| 1205 | Aftermath Shock Wave Jumper | Permanent |  |
| 1206 | Aftermath Toxic Counteragent | Permanent |  |
| 1207 | Aftermath Detoxifier | Permanent |  |
| 1208 | Nightmare Euthanizer | Permanent |  |
| 1209 | Nightmare Terminator | Permanent |  |

### Escape from Lion's Arch

[Official category](https://api.guildwars2.com/v2/achievements/categories/62)

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 1344 | Live on the Edge | Permanent |  |
| 1345 | Delaqua Investigator | Permanent |  |
| 1346 | Raiders of the Lost Parts | Permanent |  |
| 1384 | Group Effort II | Pvp, Repeatable, Permanent |  |
| 1385 | All Bets Are Off | Pvp, Permanent |  |
| 1386 | Group Effort I | Pvp, Repeatable, Permanent |  |
| 1387 | Group Effort IV | Pvp, Repeatable, Permanent |  |
| 1388 | Group Effort V | Pvp, Repeatable, Permanent |  |
| 1389 | Melted and Muted | Pvp, Permanent |  |
| 1390 | Aetherblade Broken | Pvp, Permanent |  |
| 1391 | Breach From the Beach | Pvp, Permanent |  |
| 1392 | Please Follow Me to the Exit | Pvp, Permanent |  |
| 1393 | Three Fronts | Pvp, Permanent |  |
| 1394 | Postern Ward Protector | Pvp, Permanent |  |
| 1395 | Extraction Complete | Pvp, RepairOnLogin, CategoryDisplay, Permanent |  |
| 1396 | Memories in Your Hand | Pvp, Permanent |  |
| 1397 | Antitoxin | Pvp, Permanent |  |
| 1398 | The Northern Gambit | Pvp, Permanent |  |
| 1399 | Cold Comfort | Pvp, Permanent |  |
| 1400 | Trader's Forum Triumphant | Pvp, Permanent |  |
| 1401 | Fort Marriner Fighter | Pvp, Permanent |  |
| 1402 | Triple Play | Pvp, Permanent |  |
| 1421 | Group Effort III | Pvp, Repeatable, Permanent |  |

### The Battle for Lion's Arch

[Official category](https://api.guildwars2.com/v2/achievements/categories/65)

| Achievement ID | Name | Flags | Prerequisite IDs |
|---:|---|---|---|
| 1506 | Commanding Heights | Pvp, Permanent |  |
| 1507 | No More Tricks, Scarlet | Pvp, Permanent | 1510 |
| 1508 | In a Cage Made of Steel and Lunacy | Pvp, Permanent |  |
| 1509 | In Tune | Pvp, Permanent | 1510 |
| 1510 | One Step Closer... | Pvp, Permanent |  |
| 1511 | No Free Lunch | Pvp, Permanent |  |
| 1512 | Light Show | Pvp, Permanent |  |
| 1513 | Keep Your Distance | Pvp, Permanent |  |
| 1514 | Putting Out the Fire | Pvp, Permanent |  |
| 1515 | Out with a Bang | Pvp, Permanent |  |
| 1516 | No More Magic; No More Poison | Pvp, Permanent |  |
| 1517 | This Is My City! | Pvp, RepairOnLogin, Permanent |  |
| 1518 | Build Your Own Backbone | Pvp, Permanent |  |
| 1519 | Six Minutes to Knightfall | Pvp, Permanent |  |
| 1520 | Bigger, But Not Faster | Pvp, Permanent |  |
| 1521 | He'll Never Live This Down | Pvp, Permanent |  |
| 1522 | Nowhere to Hide | Pvp, Permanent |  |
| 6777 | Six More Minutes to Knightfall | Pvp, Permanent |  |
| 6781 | The Battle for Lion's Arch | Permanent |  |
| 6782 | Battle on the Breachmaker | Permanent |  |
| 6783 | After the Battle | Permanent |  |
| 6784 | Battle for Lion's Arch Mastery | Pvp, RepairOnLogin, CategoryDisplay, Permanent |  |
| 6785 | Connecting the Pieces | Permanent |  |
| 6786 | Scarlet's End | Permanent |  |
| 6787 | Speed over Size | Pvp, Permanent |  |
| 6789 | I've Lived Things | Permanent |  |
| 6791 | The People's Champion | Permanent |  |
| 6792 | All Bets Are Still Off | Pvp, Permanent |  |
| 6793 | Dawn of the Next Journey | Permanent |  |
| 6794 | Please Follow Me to the Exit Again | Pvp, Permanent |  |
| 6795 | Assault Breaker | Permanent |  |
| 6796 | Seeking Scarlet: Old Lion's Court | Permanent | 6793 |
| 6799 | Investigative Record 3 | Permanent |  |
| 6800 | Lions Rampant | Permanent |  |
| 6801 | Lions Rampant 2 | Permanent | 6800 |
| 6802 | Raiders of the Lost Parts II | Permanent |  |
| 6805 | The Twisted Marionette | Permanent |  |
| 6808 | Escape from Lion's Arch | Permanent |  |
| 6812 | Investigative Study 5 | Permanent |  |
