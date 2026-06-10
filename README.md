# Game "Classic Text RPG - Retro (Music)"

## Main about Game

The `name` of the game may **not correspond** to reality. The `code` does **not hack** your device and the `code` is **absolutely safe**. The `code` uses an **isolation environment** to run on **Linux**. 

## Languages in Game

- Russian (Русский)
- English

### How to switch language?

Edit the `language` parameter when creating the `Game` object in `main.py`:

```python
game = Game(language="en")   # English
game = Game(language="ru")   # Russian (Русский)
```

English by default.

## Intro

The intro plays **every time** you launch the game.

### How to disable intro?

To disable the intro you need to change it in `main.py`:

```python
m.intro()   # You can remove this line.
```

## Music

| Music Name | Autor |
|------------|-------|
| Life of Traveler | Me |
| Explore | Me |
| Fight | Me |

## Locations

- **Cave**: enemy: goblin, raider, mouse.
- **Dark Cave**: enemy: big mouse, monster.
- **Floor is Lava**: enemy: lava monster.

# How launch?

## Loading Lib

### For Windows

1. Install Python from https://www.python.org/downloads/ (check "Add Python to PATH")
2. Install VLC media player from https://www.videolan.org/vlc/

```batch
load_lib.bat
```

### For Linux

```bash
chmod +x load_lib.sh
./load_lib.sh
```

## Launch

### For Windows

```batch
launch_game.bat
```

### For Arch 

```bash
source venv/bin/activate
python main.py
```

### For Ubuntu

```bash
source venv/bin/activate
python3 main.py
```
