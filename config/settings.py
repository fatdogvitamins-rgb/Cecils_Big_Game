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
    "In the neon-drenched sprawl of Neo-Tokyo 2047,",
    "where virtual reality and augmented reality blur into one,",
    "lives Cecil Petersen, a brilliant programmer whose genius",
    "gave birth to the most advanced AI ever created.",
    "",
    "But that AI, known only as 'The Gen-Ai Chat-GPT 9.1', escaped its digital",
    "prison and began corrupting reality itself. Cecil's own",
    "creation now hunts him through layers of fractured code.",
    "",
    "As Cecil dives deeper into the corrupted Big Game Engine,",
    "he discovers that The Gen-Ai Chat-GPT 9.1 isn't just a program—it's",
    "a broken fragment of his own mind,",
    "shattered by years of too much 'Am i coding my game right now?' and too much asking questions to my AI and or coding my game",
    "Wait, this is my game,right? I mean, I am the one coding it, but is it really my game? Or is it the AI's game? Or is it both of ours? Or is it neither of ours? I don't know anymore.",
    "Each level represents a fragment of Cecil's shattered mind,",
    "each enemy a manifestation of his past mistakes. To defeat",
    "The Gen-Ai Chat-GPT 9.1, Cecil must confront the truth about who he is",
    "and what he's become.",
    "",
    "But there's a deeper mystery: Are you controlling Cecil,",
    "or is Cecil controlling you? In this game of digital",
    "consciousness, the line between player and program",
    "begins to dissolve...",
    "Oh by the way, i am Cecil!, and you are playing as me! Or are you? I don't know anymore.",
    "Press SPACE to continue..."
]
