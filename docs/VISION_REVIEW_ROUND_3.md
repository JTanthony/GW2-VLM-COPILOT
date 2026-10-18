# Vision review: focused background extraction

The hour-long Crystal Oasis recording exposed repeated invented names, numeric
progress inferred from bars, vendor currencies mislabeled as gold, unnecessary
combat fields and long repeated text. Median analysis was about 50.5 seconds.

## Implemented changes

- Background observation uses a shorter extraction task and a separate schema:
  at most eight visible-text entries of 120 characters, no warnings, null player
  status and one short summary. Its answer allowance is 384 instead of 512 tokens.
- The task distinguishes current events, story, hearts and watched achievements.
  Unlabeled bars must not become numeric counts; currency denominations must be
  identified or left unknown. Decorative scenery, chat and combat details are
  excluded from the background task.
- Validation normalizes literal null/unknown placeholders, removes duplicate
  entries and omits empty map/episode labels. This does not correct invented names
  or guarantee that a numeric reading matches the image.
- Explicit player screen questions retain the full-frame/manual observation path
  and its existing 512-token allowance. No live cropping is enabled yet.
- Standard captured images remain in RAM; source development recording remains
  optional. No additional notification types or automatic model training added.

## Developer comparison tool

`tools/compare_vision_inputs.py` compares an already-saved frame with a native-pixel
crop for map title/counters, the right-side tracker, or the central panel. It calls
an already-running loopback model; it never starts another engine or captures the
screen. Run only when that engine is idle to avoid contention with the app/tester.

Example from the source project, using a previously recorded private frame:

```powershell
.venv\Scripts\python.exe tools\compare_vision_inputs.py --frame "<saved-frame.png>" --region map --repeats 2
```

Choose `tracker` for event objectives or `panel` for a central vendor/tooltip or
achievement panel. Fixed crop rectangles are benchmark candidates, not a robust
detector of custom layouts. Both input types use the same task and output budget;
order alternates between repetitions. Crop pixels are not resized or written to
disk. Observations/timing are saved privately under `local-data/vision-benchmarks`.
The comparison tool and testing module stay excluded from the Windows package.

## Validation and next measurements

184 automated tests and the source GUI smoke check passed. Added checks cover
placeholder/repetition cleanup, separate background/manual budgets and schemas,
and native-pixel crop fidelity. No live-model comparison was run in this change;
there is no measured speed or accuracy improvement yet.

Use the recorded Crystal Oasis map, jackal notice, Amnoon event-counter and vendor
screens as a fixed evaluation set. Score exact names, labeled counts, denomination
accuracy, unknowns and latency. Check that smaller output limits do not introduce
truncated responses. Vendor karma/Trade Contract amounts must never become gold;
Forged Remaining bars must stay nonnumeric when no digits are visible. Repeat on
a different UI scale and moved panels before choosing a live crop policy.

Only enable a crop strategy after it improves factual accuracy and latency on
both repeated and held-out frames. Do not reward a fast but confidently incorrect
answer. Capturing more gameplay alone does not train model weights. Windows
packages need a separate rebuild to receive these edits.
