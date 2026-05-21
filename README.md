<div align="center">

# Rundan

**Svenskt partykortspel · Python & Flet**

*[▶ Spela](https://linneaegner.github.io/rundan/)* · Programming 2, GU 2023 · refaktorerat 2026

</div>

Turn-based card game for friends on **one shared screen**: lobby, five categories, 100 text cards, turn order. Play in the browser — no install. Push to `main` auto-deploys to GitHub Pages (reload the page after updates).

## Spela

**https://linneaegner.github.io/rundan/**

Första laddning ~10–20 s. En skärm, turordning — inte online-multiplayer.

## Kör lokalt

Python 3.11+, Flet 0.85, pytest.

```bash
git clone https://github.com/linneaegner/rundan.git
cd rundan
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flet run main.py          # desktop
./run.sh                  # webbläsare på localhost:8550
pip install -r requirements-dev.txt && pytest
```

## Kod

| Fil | Roll |
|-----|------|
| `main.py` | UI, lobby/spel, turordning |
| `questions.py` | 100 kort, kategorier, `QuestionDeck` |
| `models.py` | `Person` |
| `theme.py` / `constants.py` | UI och design tokens |

Solo coursework (GU 2023). GitHub only — not on [linnea.egner.se](https://linnea.egner.se).

## Screenshots

| Lobby | Spelare tillagda | Spel |
|:-----:|:----------------:|:----:|
| ![Lobby – tom](docs/screenshots/lobby-empty.png) | ![Lobby – spelare](docs/screenshots/lobby-players.png) | ![Spel](docs/screenshots/game.png) |
