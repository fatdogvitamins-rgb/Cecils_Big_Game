# Cecil's Big Game

A ultra-playable 2D platform game built with Pygame featuring:
- Advanced player physics (jumping, double-jump, wall-slide)
- Multiple challenging levels
- AI-controlled enemies with different behaviors
- In-game Tinkercad 3D character designer
- Visual block editor for custom enemy AI
- Advanced AI system (rule-based, machine learning, smart behaviors)
- Full audio and polish

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (if applicable):
```bash
cd Cecils_Big_Game
```

2. **Create a virtual environment**:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running the Game

```bash
python main.py
```

## Controls

### Game Controls
- **Left Arrow / A**: Move left
- **Right Arrow / D**: Move right
- **Spacebar / Up Arrow / W**: Jump (press again while in air for double jump)
- **P / ESC**: Pause game

### Menu Controls
- **Up/Down Arrows**: Navigate menu
- **Enter/Spacebar**: Select option
- **Escape**: Back/Quit

## Game Features

### Core Game
- **3 Progressive Levels**: From tutorial to expert challenges
- **Player Mechanics**: Smooth movement, gravity, jumping, double-jump, wall-slide
- **Platforms**: Static and moving platforms with smooth collision
- **Enemies**: AI-controlled enemies with patrol and chase behaviors
- **Collectibles**: Coins to gather for score
- **Health System**: 3 hearts, lose health on enemy contact
- **Score System**: Earn points by collecting coins and completing levels
- **Camera**: Smooth following camera system

### Creative Tools (Coming Soon)
- **Tinkercad Editor**: Design custom 3D characters and enemies
- **Block Visual Editor**: Drag-and-drop programming for enemy behavior
- **AI System**: Rule-based, machine learning, and behavior tree AI

### UI/Polish
- Main menu with options
- Pause screen
- Level complete screen
- Game over screen with score
- HUD showing health, score, level, FPS

## File Structure

```
Cecils_Big_Game/
├── main.py                 # Game entry point
├── requirements.txt        # Python dependencies
├── config/
│   └── settings.py        # Game configuration
├── src/
│   ├── game.py            # Main game loop
│   ├── player.py          # Player class
│   ├── platform.py        # Platform class
│   ├── enemy.py           # Enemy class
│   ├── level.py           # Level management
│   ├── ui.py              # UI and HUD
│   ├── sprite_manager.py  # Sprite handling
│   ├── block_editor.py    # (Coming soon)
│   ├── tinkercad_editor.py # (Coming soon)
│   ├── block_compiler.py  # (Coming soon)
│   ├── ai_engine.py       # (Coming soon)
│   └── behavior_trees.py  # (Coming soon)
├── assets/
│   ├── sprites/           # Game sprites
│   ├── audio/             # Music and sound effects
│   ├── levels/            # Level data (JSON)
│   └── ui/                # UI elements
└── docs/                  # Documentation
```

## Level Progression

### Level 0: Introduction
A simple tutorial level to learn the controls and basic mechanics.

### Level 1: Platforming
Harder jumping challenges with moving platforms and more enemies.

### Level 2: Expert Challenge
Advanced level with complex obstacle courses, multiple enemy types, and tricky jumps.

## Configuration

Edit `config/settings.py` to customize:
- Screen resolution
- Colors
- Physics parameters (gravity, jump power, etc.)
- Controls
- Audio settings

## Known Limitations (Beta)

- Tinkercad editor not yet integrated
- Block visual editor not yet implemented
- No custom level support yet
- Limited sprite customization (using placeholder graphics)
- No advanced AI training system yet

## Future Additions

- Full Tinkercad integration for character design
- Visual block editor for programming enemies
- Machine learning AI trainer
- Custom level editor
- More levels and enemies
- Boss encounters
- Leaderboard/high scores
- Mobile/console ports

## Credits

Created with Pygame - A cross-platform set of Python modules designed for writing video games.

## License

(Add your license here)

## Support

For issues, questions, or feature requests, please check the project documentation or contact the development team.

---

**Good luck! Have fun playing Cecil's Big Game! 🎮**
