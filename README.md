<div align="center">

# Förfest

**Desktop party card game · Python & Flet**

*Programming 2 · Göteborgs universitet · 2023 · Solo project · refaktorerat 2026*

[Features](#features) · [Quick start](#quick-start) · [Architecture](#architecture) · [Context](#context)

</div>

---

## Overview

**Förfest** is a Swedish turn-based pre-party card game for friends: add players in a lobby, pick categories, draw text challenge cards, and pass turns until the deck runs out. Built with **Python 3.11+** and **Flet 0.85** as coursework for *Programming 2* at the University of Gothenburg (2023), refactored in 2026 with a text-card deck, category filters, and pytest.

## Features

| Area | What it does |
|------|----------------|
| **Lobby** | Add players (min. 2), validation, removable player chips |
| **Categories** | Toggle five card types: Sanning, Utmaning, Drick, Rösta, Vild |
| **Game** | Turn order, tap-to-draw cards, deck counter, reshuffle when empty |
| **Cards** | 100 Swedish text prompts across five categories |
| **UI** | Dark pre-party theme, responsive layout, Swedish copy |

## Screenshots

| Lobby | Card draw | Game |
|:-----:|:---------:|:----:|
| ![Lobby](docs/screenshots/lobby.png) | ![Card draw](docs/screenshots/game.png) | ![Home](docs/screenshots/home.png) |

> To refresh screenshots after UI changes: run the app, capture lobby (with players + categories), an active card draw, and the game screen. Save as `docs/screenshots/lobby.png`, `game.png`, and optionally `home.png`.

## Quick start

**Requirements:** Python 3.11+, macOS or Linux (desktop tested on macOS)

```bash
git clone https://github.com/linneaegner/do-or-lose.git
cd do-or-lose
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flet run main.py
```

Or use the helper script (kills stale port, runs in web mode on `127.0.0.1:8550`):

```bash
chmod +x run.sh
./run.sh
```

**Tests** (optional):

```bash
pip install -r requirements-dev.txt
pytest
```

> **Flet 0.85:** Run inside the project `.venv` if a global Flet install conflicts.

## Architecture

```mermaid
flowchart LR
  subgraph ui [Flet UI]
    L[Lobby]
    G[Game]
  end
  L -->|start| G
  G --> QuestionDeck
  G --> Person
  QuestionDeck --> QUESTIONS["100 text cards"]
```

| File | Role |
|------|------|
| `main.py` | App entry, lobby/game flow, turn loop |
| `models.py` | `Person` — player name and state |
| `questions.py` | `Category`, `Question`, `QuestionDeck` — 100 cards |
| `theme.py` | Shared UI components and layout |
| `constants.py` | Design tokens and game rules |
| `run.sh` | Convenience launcher (web mode, fixed port) |

## Context

- **Original (2023):** University coursework — OOP desktop app with Flet instead of console I/O. Early version used image cards and Swedish UI.
- **This repo (2026):** Refactored **Förfest** — text-card deck, category filters, updated Flet 0.85 API, pytest. Public on GitHub; not listed on [linneaegner.se](https://linneaegner.se).

## License

University coursework — see repository for usage.
