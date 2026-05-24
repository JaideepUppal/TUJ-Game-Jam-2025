# TUJ Game Jam 2025 - Life Is a Lie

**1st Place Winner - TUJ Game Jam 2025**

This project is a Python/Pygame boss-battle game built for the TUJ Game Jam 2025 theme: **"Life is a lie"**.

The game begins like a conventional impossible boss fight, then subverts that expectation with an unconventional empathy-based win condition. Instead of simply defeating the boss through combat, players are pushed to question the rules, pay attention to misleading instructions, and find a more compassionate way to finish the encounter.

## Tech Stack

- Python
- Pygame 2.6.1

## Team

Team Golem:

- Jaideep Uppal
- Sushant Bharadwaj Kagolanu
- Riju Pant
- Bettina Marksteiner

## Getting Started

Clone the repository:

```bash
git clone https://github.com/JaideepUppal/TUJ-Game-Jam-2025.git
cd TUJ-Game-Jam-2025
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the game:

```bash
python3 main-game-file.py
```

## Controls

- `ENTER`: Start the game or return to the menu after winning/losing
- `W`, `A`, `S`, `D`: Move
- `LEFT SHIFT` + direction: Dash
- `K`: Shoot
- `E`: Interact with roses during the later phase
- Close the Pygame window to quit

## Project Structure

```text
TUJ-Game-Jam-2025/
|-- assets/
|   `-- images/
|       |-- background.webp
|       |-- backgroundTemple.webp
|       |-- boss.png
|       |-- boss_projectile.png
|       |-- lava.jpg
|       |-- player.png
|       |-- projectile.png
|       |-- rock.png
|       |-- rose.webp
|       |-- roseBW.png
|       |-- stomp.png
|       `-- worm.png
|-- game/
|   |-- boss.py
|   |-- constants.py
|   |-- game_state.py
|   |-- init-file.py
|   |-- player.py
|   `-- projectile.py
|-- intro_music.mp3
|-- main_music.mp3
|-- main-game-file.py
|-- PokemonGb-RAeo.ttf
|-- README.md
`-- requirements.txt
```

## Skills Demonstrated

- Gameplay programming with Python and Pygame
- Real-time input handling and movement
- Boss phase/state management
- Collision detection and projectile behavior
- Asset integration for sprites, fonts, backgrounds, and music
- Audio fallback handling for demo robustness
- Rapid prototyping under game jam constraints
- Designing a theme-driven gameplay twist around empathy instead of combat victory

## Screenshots / Demo

Add project media here when available:

- Screenshot: TODO
- Gameplay video: TODO

## Notes

This game was created during TUJ Game Jam 2025 and won 1st place. The current version keeps the original gameplay concept while making startup, asset loading, and setup instructions cleaner for demos and code review.
