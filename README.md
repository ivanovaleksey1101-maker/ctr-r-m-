# Game "Classic Text RPG - Retro (Music)"

## Offical Languages

- Russian (Русский)
- English

### How to switch language?

Edit the `language` parameter when creating the `Game` object in `main.py`:

```python
game = Game(language="en")   # English
game = Game(language="ru")   # Русский
```

English by default.

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
