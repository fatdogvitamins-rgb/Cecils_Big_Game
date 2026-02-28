"""
Level - Level management and loading
"""

import json
import os
from config.settings import *
from src.platform import PlatformGroup
from src.enemy import EnemyGroup, Enemy
from src.sprite_manager import SpriteManager


class Level:
    """Represents a single game level"""

    def __init__(self, level_number: int, sprite_manager: SpriteManager):
        """
        Initialize level

        Args:
            level_number: Level number
            sprite_manager: SpriteManager instance
        """
        self.level_number = level_number
        self.sprite_manager = sprite_manager
        self.platforms = PlatformGroup()
        self.enemies = EnemyGroup()
        self.collectibles = pygame.sprite.Group()
        self.goal = None
        self.player_start_x = PLAYER_START_X
        self.player_start_y = PLAYER_START_Y
        self.level_complete = False

        # Load level data
        self.load_level()

    def load_level(self):
        """Load level from data"""
        # Try to load from JSON file first
        level_file = f"assets/levels/level_{self.level_number}.json"
        if os.path.exists(level_file):
            self.load_from_json(level_file)
        else:
            # Use built-in level definitions
            self.load_built_in_level()

    def load_from_json(self, filename: str):
        """
        Load level from JSON file

        Args:
            filename: Path to JSON file
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            # Load platforms
            for platform_data in data.get('platforms', []):
                platform = self.platforms.create_platform(
                    platform_data['x'], platform_data['y'],
                    platform_data['width'], platform_data['height'],
                    self.sprite_manager,
                    platform_data.get('is_moving', False)
                )
                if platform_data.get('is_moving'):
                    platform.set_movement(
                        platform_data.get('movement_type', 'horizontal'),
                        platform_data.get('move_range', 100),
                        platform_data.get('move_speed', 2)
                    )

            # Load enemies
            for enemy_data in data.get('enemies', []):
                self.enemies.create_enemy(
                    enemy_data['x'], enemy_data['y'],
                    enemy_data.get('width', ENEMY_WIDTH),
                    enemy_data.get('height', ENEMY_HEIGHT),
                    self.sprite_manager,
                    enemy_data.get('ai_type', 'patrol')
                )

            # Load goal
            goal_data = data.get('goal', {})
            self.goal = pygame.Rect(goal_data['x'], goal_data['y'], goal_data['width'], goal_data['height'])

            # Load player start position
            player_data = data.get('player_start', {})
            self.player_start_x = player_data.get('x', PLAYER_START_X)
            self.player_start_y = player_data.get('y', PLAYER_START_Y)

        except Exception as e:
            print(f"Error loading level from JSON: {e}. Using built-in level.")
            self.load_built_in_level()

    def load_built_in_level(self):
        """Load built-in level definition"""
        if self.level_number == 0:
            self.load_level_0()
        elif self.level_number == 1:
            self.load_level_1()
        elif self.level_number == 2:
            self.load_level_2()
        else:
            self.load_level_0()  # Default fallback

    def load_level_0(self):
        """Load level 0 - Introduction level"""
        # Ground
        self.platforms.create_platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40, self.sprite_manager)

        # Starting platform
        self.platforms.create_platform(50, 600, 150, 20, self.sprite_manager)

        # Jump platforms
        self.platforms.create_platform(300, 500, 100, 20, self.sprite_manager)
        self.platforms.create_platform(550, 400, 100, 20, self.sprite_manager)
        self.platforms.create_platform(800, 500, 100, 20, self.sprite_manager)

        # Goal platform
        self.platforms.create_platform(1100, 300, 120, 20, self.sprite_manager)

        # Simple enemy
        self.enemies.create_enemy(400, 550, ENEMY_WIDTH, ENEMY_HEIGHT, self.sprite_manager, "patrol")

        # Goal
        self.goal = pygame.Rect(1100, 250, 120, 50)

    def load_level_1(self):
        """Load level 1 - Platform jumping"""
        # Ground
        self.platforms.create_platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40, self.sprite_manager)

        # Starting platform
        self.platforms.create_platform(50, 600, 120, 20, self.sprite_manager)

        # Ascending platforms
        for i in range(5):
            x = 200 + i * 180
            y = 550 - i * 80
            self.platforms.create_platform(x, y, 120, 20, self.sprite_manager)

        # Moving platform
        moving_plat = self.platforms.create_platform(700, 300, 150, 20, self.sprite_manager, True)
        moving_plat.set_movement("horizontal", 200, 2)

        # Final platform
        self.platforms.create_platform(1100, 200, 120, 20, self.sprite_manager)

        # Enemies
        self.enemies.create_enemy(300, 550, ENEMY_WIDTH, ENEMY_HEIGHT, self.sprite_manager, "patrol")
        self.enemies.create_enemy(900, 400, ENEMY_WIDTH, ENEMY_HEIGHT, self.sprite_manager, "chase")

        # Goal
        self.goal = pygame.Rect(1100, 150, 120, 50)

    def load_level_2(self):
        """Load level 2 - Advanced challenge"""
        # Ground
        self.platforms.create_platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40, self.sprite_manager)

        # Section 1 - Jumping challenge
        self.platforms.create_platform(50, 600, 100, 20, self.sprite_manager)
        for i in range(4):
            self.platforms.create_platform(200 + i * 100, 550 - i * 50, 80, 20, self.sprite_manager)

        # Section 2 - Moving platforms
        for i in range(3):
            plat = self.platforms.create_platform(600 + i * 200, 400, 120, 20, self.sprite_manager, True)
            plat.set_movement("vertical", 150, 1.5)

        # Section 3 - Final challenge
        self.platforms.create_platform(1000, 280, 100, 20, self.sprite_manager)
        self.platforms.create_platform(1100, 220, 100, 20, self.sprite_manager)

        # Enemies - Multiple and varied
        for i in range(3):
            self.enemies.create_enemy(300 + i * 200, 540, ENEMY_WIDTH, ENEMY_HEIGHT, self.sprite_manager, "patrol")
        self.enemies.create_enemy(750, 350, ENEMY_WIDTH, ENEMY_HEIGHT, self.sprite_manager, "chase")

        # Goal
        self.goal = pygame.Rect(1100, 170, 100, 50)

    def update(self, player):
        """
        Update level

        Args:
            player: Player object
        """
        # Update platforms
        for platform in self.platforms:
            platform.update()

        # Check goal collision
        if self.goal and player.rect.colliderect(self.goal):
            self.level_complete = True

        # Update enemies
        self.enemies.update_all(player, self.platforms)

    def draw(self, surface: pygame.Surface):
        """
        Draw level

        Args:
            surface: Pygame surface to draw on
        """
        # Draw platforms
        surface.blit(self.platforms, surface)
        for platform in self.platforms:
            surface.blit(platform.image, platform.rect)

        # Draw goal
        if self.goal:
            pygame.draw.rect(surface, COLOR_YELLOW, self.goal, 3)
            pygame.draw.rect(surface, COLOR_YELLOW, (self.goal.x + 10, self.goal.y + 10, self.goal.width - 20, self.goal.height - 20))

        # Draw enemies
        for enemy in self.enemies:
            if enemy.is_alive:
                surface.blit(enemy.image, enemy.rect)

    def is_complete(self):
        """Check if level is complete"""
        return self.level_complete

    def reset(self):
        """Reset level state"""
        self.level_complete = False
