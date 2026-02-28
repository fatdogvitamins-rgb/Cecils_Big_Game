"""
Platform - Platform class for level design
"""

import pygame
from config.settings import *
from src.sprite_manager import SpriteManager


class Platform(pygame.sprite.Sprite):
    """Static or moving platform"""

    def __init__(self, x: float, y: float, width: int, height: int, sprite_manager: SpriteManager = None, is_moving: bool = False, move_range: int = 0, move_speed: float = 2):
        """
        Initialize platform

        Args:
            x: X position
            y: Y position
            width: Width of platform
            height: Height of platform
            sprite_manager: SpriteManager instance
            is_moving: Whether platform moves
            move_range: Range of movement
            move_speed: Speed of movement
        """
        super().__init__()
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.width = width
        self.height = height
        self.is_moving = is_moving
        self.move_range = move_range
        self.move_speed = move_speed
        self.move_direction = 1  # 1 for right/down, -1 for left/up
        self.movement_type = "horizontal"  # or "vertical"

        # Create platform sprite
        if sprite_manager:
            self.image = sprite_manager.create_placeholder_sprite(width, height, (100, 200, 100))
        else:
            self.image = pygame.Surface((width, height))
            pygame.draw.rect(self.image, (100, 200, 100), (0, 0, width, height))
            pygame.draw.rect(self.image, (50, 150, 50), (0, 0, width, height), 2)

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        """Update platform position if moving"""
        if self.is_moving:
            if self.movement_type == "horizontal":
                self.x += self.move_speed * self.move_direction
                # Check bounds
                if abs(self.x - self.start_x) > self.move_range:
                    self.move_direction *= -1
                    self.x = self.start_x + self.move_range * self.move_direction
            elif self.movement_type == "vertical":
                self.y += self.move_speed * self.move_direction
                # Check bounds
                if abs(self.y - self.start_y) > self.move_range:
                    self.move_direction *= -1
                    self.y = self.start_y + self.move_range * self.move_direction

            self.rect.topleft = (self.x, self.y)

    def get_position(self):
        """Get platform position"""
        return (self.x, self.y)

    def set_movement(self, movement_type: str = "horizontal", move_range: int = 100, move_speed: float = 2):
        """
        Set platform movement

        Args:
            movement_type: "horizontal" or "vertical"
            move_range: Range of movement
            move_speed: Speed of movement
        """
        self.movement_type = movement_type
        self.move_range = move_range
        self.move_speed = move_speed
        self.is_moving = True


class PlatformGroup(pygame.sprite.Group):
    """Group of platforms for easy management"""

    def __init__(self):
        """Initialize platform group"""
        super().__init__()

    def create_platform(self, x: float, y: float, width: int, height: int, sprite_manager: SpriteManager = None, is_moving: bool = False):
        """
        Create and add a platform

        Args:
            x: X position
            y: Y position
            width: Width
            height: Height
            sprite_manager: SpriteManager instance
            is_moving: Whether platform moves

        Returns:
            Created Platform object
        """
        platform = Platform(x, y, width, height, sprite_manager, is_moving)
        self.add(platform)
        return platform

    def check_collisions(self, player):
        """
        Check player collision with all platforms

        Args:
            player: Player object
        """
        for platform in self:
            player.check_collision_with_platform(platform)
