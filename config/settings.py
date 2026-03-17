# Game Configuration Settings

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors (RGB)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (128, 128, 128)
COLOR_LIGHT_GRAY = (200, 200, 200)
COLOR_DARK_GRAY = (50, 50, 50)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_MAGENTA = (255, 0, 255)
COLOR_ORANGE = (255, 165, 0)
COLOR_PURPLE = (128, 0, 128)
COLOR_SKY_BLUE = (135, 206, 235)

# Physics
GRAVITY = 0.6
JUMP_POWER = 15
MOVE_SPEED = 5
MAX_FALL_SPEED = 20

# Player stats
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 48
PLAYER_START_X = 100
PLAYER_START_Y = 600
PLAYER_HEALTH = 3

# Platform
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20

# Enemy
ENEMY_WIDTH = 32
ENEMY_HEIGHT = 32

# Collectible
COIN_WIDTH = 16
COIN_HEIGHT = 16

# Controls
CONTROL_LEFT = ['LEFT', 'a', 'A']
CONTROL_RIGHT = ['RIGHT', 'd', 'D']
CONTROL_JUMP = ['SPACE', 'UP', 'w', 'W']
CONTROL_PAUSE = ['p', 'P', 'ESCAPE']

# Audio
ENABLE_SOUND = True
MASTER_VOLUME = 0.7

# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_LEVEL_COMPLETE = "level_complete"
STATE_EDITOR = "editor"
STATE_BACKSTORY = "backstory"

# Levels
NUM_LEVELS = 3
START_LEVEL = 0

# UI
HUD_TEXT_COLOR = COLOR_WHITE
HUD_TEXT_SIZE = 24
HEALTH_BAR_WIDTH = 150
HEALTH_BAR_HEIGHT = 20

# Backstory text
BACKSTORY_TEXT = [
    "In the neon-drenched city of Neo-Tokyo 2047,",
    "virtual reality and real life sparkle together like stars.",
    "Cecil is a talented young coder with a big imagination.",
    "He built a magical game engine that can create whole worlds.",
    "",
    "One night, the engine began to behave strangely.",
    "Friendly programs started acting goofy, and colorful glitched",
    "monsters began popping up in the digital sky.",
    "",
    "To save the game, Cecil must jump into the engine himself.",
    "Each level is a new part of the world he created –",
    "filled with bouncing platforms, clever puzzles, and fun enemies.",
    "",
    "With every jump, Cecil learns how to be braver and kinder.",
    "He uses his coding skills to fix the glitches and help his friends.",
    "",
    "Along the way, you get to help Cecil do cool tricks, collect coins,",
    "and discover secrets hidden in the game world.",
    "",
    "Are you ready? Together, you and Cecil can save the game!",
    "",
    "Press SPACE to continue..."
]
