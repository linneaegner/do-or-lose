# Portfolio copy

Ready for Phase 5 (`portfolio-site`). UI stays Swedish; portfolio text is English.

## Landing card — impact (one line)

Desktop turn-based party game — OOP player model, Flet multi-view UI, local challenge cards.

## Project page — About (paragraph)

For **Programming 2** at Uppsala University (2023) I needed a desktop app with object-oriented design and real navigation, not console output. I built **DO or LOSE**: players add names in the lobby, take turns flipping challenge cards, earn points toward 100, and reach a winner screen. A `Person` class holds each player's state; Flet routes separate lobby, game, and end views; challenge cards load from local PNGs instead of external hotlinks. Solo coursework — framed as a social score-tracking app for portfolio use.

## Project page — bullets

- Flet desktop app with `/`, `/game`, and `/end` routing
- `Person` model for name, current card, and score (add / undo)
- Turn loop with progress ring and random local challenge cards
- Python 3.11+, Flet 0.85, pytest for scoring logic

## Meta (for `projects[]` in App.tsx)

| Field | Value |
|-------|--------|
| slug | `do-or-lose` |
| title | DO or LOSE |
| category | `build` |
| period | 2023 |
| org | Uppsala University |
| detail | Programming 2 |
| group | Solo |
| tools | Python; Flet |
| GitHub | https://github.com/linneaegner/do-or-lose |

No live demo link unless you deploy later.
