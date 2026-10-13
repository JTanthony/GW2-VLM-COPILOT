# First vision review: achievement and event focus

The first local recording revealed that vision often treated a story title as
the current map and summarized progress without preserving checklist states.
Background vision now prioritizes exact achievement names, checked versus
unchecked objectives, and current event counters. Watch-list entries and
browsed maps do not establish player proximity. Combat coaching and reminders
for other maps are outside this scope.

## Efficiency

- Capture still keeps only the newest frame in memory at up to 2 FPS.
- Background analysis refreshes its frame after acquiring the inference lock.
- An in-memory grayscale comparison checks the standard GW2 event-tracker and
  achievement-panel regions. Nearly unchanged regions skip another inference.
- A 60-second refresh prevents custom layouts or small changes from being
  ignored indefinitely. A five-second pause follows each background analysis.
- Full frames still reach the model. This first step does not implement OCR,
  cropping, or a second reasoning call. Scene motion may still trigger analysis;
  the comparison is a heuristic, not semantic detection of completed objectives.

Automatic chat notifications remain disabled. This update improves evidence
for player-requested advice; it does not add proactive achievement alerts.
No screenshots are saved in the normal app. Explicit source-only development
recording remains available and excluded from Windows packaging.

## Validation and next test

157 automated tests and the source GUI smoke check passed. Regression checks
cover unchanged frames, periodic refresh, tracker changes, combat-HUD changes,
and invalid image handling. No live model speed improvement has been measured.
The next gameplay test should compare map identification, checklist accuracy,
analysis frequency, and whether useful small progress changes are missed.
