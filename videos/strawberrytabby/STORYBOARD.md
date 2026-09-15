# Storyboard

**Format:** 1920×1080
**Audio:** neutral TTS voiceover; no underscore required
**VO direction:** calm, factual, restrained; pauses are intentional
**Style basis:** DESIGN.md and the captured X profile-status screen

## Asset Audit

| Asset | Type | Assign to Beat | Role |
|---|---|---|---|
| `capture/screenshots/scroll-000.png` | Screenshot | 1, 2, 3 | Factual source frame, cropped and framed |
| `capture/assets/svgs/logo-2226fa10.svg` | SVG logo candidate | 1 | X mark if compatible |
| `capture/assets/fonts/Chirp-Regular.c88864db.latin.woff2` | Font | 1, 2, 3 | Primary interface type |
| `capture/assets/fonts/Chirp-Light.190dbce4.latin.woff2` | Font | 1, 2, 3 | Secondary copy |

## Beat 1 — STATUS (0:00–0:03.4s)

**VO:** “The profile is currently unavailable.”

**Concept:** A clean reveal of the captured state. The viewer first sees the X mark and Profile rail, then the status message settles into focus.

**Visual:** White field; thin vertical rails draw in from the top and bottom; a cropped screenshot panel eases into the center. “ACCOUNT SUSPENDED” appears as the dominant title, with a small blue underline pulse.

**Animation choreography:** rails DRAW; screenshot SLIDES upward 18px and settles; title TYPES in by word; blue underline PULSES once.

**Transition:** blur-through, 0.25s into the next beat.

**Depth layers:** BG white; MG screenshot crop and dividers; FG status title and blue accent.

## Beat 2 — REASON SHOWN (0:03.4–0:08.4s)

**VO:** “X says this account has been suspended for violating the X Rules.”

**Concept:** Focus on the exact public explanation, without adding speculation. The sentence becomes a precise callout over the source UI.

**Visual:** The profile-status crop enlarges slightly. The phrase “X suspends accounts” tracks in from the left; the “X Rules” link glows in `#1D9BF0`. A thin bracket traces around the status block while the rest of the page remains quiet.

**Animation choreography:** crop ZOOMS 1.00→1.03; bracket DRAWS clockwise; copy SLIDES in; blue link SHIMMERS once; background rail FLOATS 2px.

**Transition:** velocity-matched upward, 0.33s out / 0.45s in.

**Depth layers:** BG white; MG enlarged source crop; FG bracket, copy, and link accent.

## Beat 3 — NEXT STEP (0:08.4–0:14.5s)

**VO:** “The public page offers one next step: sign in or sign up to continue the conversation.”

**Concept:** Resolve on the captured login panel, making the available action obvious while keeping the tone neutral.

**Visual:** The right-side sign-in card slides into a clean centered presentation. The black phone button lands first, followed by Apple and Google outlines. The “or” divider draws across the card, then “Log in with username or email” appears. The X mark returns in the upper-left as a final anchor.

**Animation choreography:** card SLIDES 32px from right with a soft rise; buttons CASCADE at 0.12s intervals; divider DRAWS; final X mark FADES in with a small scale settle.

**Transition:** final hold, then a gentle 0.35s fade on the last second only.

**Depth layers:** BG white; MG login card and shadow; FG buttons, divider, and X mark.

## Production Architecture

```text
videos/strawberrytabby/
├── index.html
├── DESIGN.md
├── SCRIPT.md
├── STORYBOARD.md
├── narration.txt
├── narration.wav
├── transcript.json
├── capture/
└── compositions/
    ├── beat-1-status.html
    ├── beat-2-reason.html
    └── beat-3-next-step.html
```
