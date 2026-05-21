<div align="center">

# Rundan

**Svenskt partykortspel · Python & Flet**

*[▶ Spela](https://linneaegner.github.io/rundan/)*

</div>

Turordnat partykortspel för vänner på **en delad skärm**. Lägg till spelare, välj kategorier, dra kort i turordning. Körs i webbläsaren — ingen installation.

## Spela

**https://linneaegner.github.io/rundan/**

## Lokalt

```bash
git clone https://github.com/linneaegner/rundan.git
cd rundan
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./run.sh    # http://127.0.0.1:8550
```

Tester: `pip install -r requirements-dev.txt && pytest`

## Screenshots

<p align="center">
  <img src="docs/screenshots/lobby-empty.png" width="300" alt="Lobby" /><br/>
  <img src="docs/screenshots/lobby-players.png" width="300" alt="Spelare tillagda" /><br/>
  <img src="docs/screenshots/game-turn.png" width="300" alt="Spel" />
</p>

---

Programming 2, GU 2023 · refaktorerat 2026
