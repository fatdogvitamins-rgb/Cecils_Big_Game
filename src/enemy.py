"""
Enemy - Enemy class with AI behavior
"""

import pygame
import math
from config.settings import *
from src.sprite_manager import SpriteManager


class Enemy(pygame.sprite.Sprite):
    """Enemy with basic AI and patrol behavior"""

    def __init__(self, x: float, y: float, width: int, height: int, sprite_manager: SpriteManager = None, ai_type: str = "patrol"):
        """
        Initialize enemy

        Args:
            x: X position
            y: Y position
            width: Width
            height: Height
            sprite_manager: SpriteManager instance
            ai_type: Type of AI ("patrol", "chase", "patrol_vertical")
        """
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 2
        self.ai_type = ai_type
        self.start_x = x
        self.start_y = y
        self.patrol_range = 150
        self.patrol_direction = 1
        self.health = 1
        self.is_alive = True
        self.on_ground = True
        self.ai_engine = None  # Will be set later
        self.animation_frame = 0
        self.animation_counter = 0

        # Create enemy sprite
        if sprite_manager:
            self.image = sprite_manager.create_placeholder_sprite(width, height, (255, 100, 100))
        else:
            self.image = pygame.Surface((width, height))
            pygame.draw.rect(self.image, (255, 100, 100), (0, 0, width, height))
            pygame.draw.rect(self.image, (200, 50, 50), (0, 0, width, height), 2)
            # Draw simple eyes
            pygame.draw.circle(self.image, (0, 0, 0), (width // 3, height // 3), 3)
            pygame.draw.circle(self.image, (0, 0, 0), (2 * width // 3, height // 3), 3)

        self.rect = self.image.get_rect(topleft=(x, y))
        self._last_player = None  # For AIEngine callbacks
        self._last_platforms = None  # For AIEngine callbacks

    def update(self, player=None, platforms=None):
        """
        Update enemy

        Args:
            player: Player object (for chase AI)
            platforms: Platform group (for collision)
        """
        if not self.is_alive:
            return

        # Store player reference for use in AIEngine callbacks
        self._last_player = player
        self._last_platforms = platforms

        # Use AIEngine if available
        if self.ai_engine:
            self.ai_engine.update(player, platforms)
        else:
            # Fallback to legacy AI system
            if self.ai_type == "patrol":
                self.patrol_horizontal()
            elif self.ai_type == "chase" and player:
                self.chase_player(player)
            elif self.ai_type == "patrol_vertical":
                self.patrol_vertical()

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.topleft = (self.x, self.y)

        self.animation_counter += 0.1
        if self.animation_counter >= 1:
            self.animation_counter = 0

    def patrol_horizontal(self):
        """Patrol back and forth horizontally"""
        self.velocity_x = self.speed * self.patrol_direction

        # Reverse direction at patrol range limits
        if abs(self.x - self.start_x) > self.patrol_range:
            self.patrol_direction *= -1
            self.velocity_x = self.speed * self.patrol_direction

    def patrol_vertical(self):
        """Patrol up and down vertically"""
        self.velocity_y = self.speed * self.patrol_direction

        # Reverse direction at patrol range limits
        if abs(self.y - self.start_y) > self.patrol_range:
            self.patrol_direction *= -1
            self.velocity_y = self.speed * self.patrol_direction

    def chase_player(self, player):
        """Chase the player when spotted"""
        # Calculate distance to player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # Only chase if player is in range (200 pixels)
        if distance < 200:
            # Normalize and apply speed
            if distance > 0:
                self.velocity_x = (dx / distance) * self.speed
                self.velocity_y = (dy / distance) * (self.speed * 0.5)
        else:
            # Return to patrol
            self.ai_type = "patrol"
            self.velocity_x = 0
            self.velocity_y = 0

    def patrol(self):
        """Patrol back and forth (alias for patrol_horizontal)"""
        self.patrol_horizontal()

    def chase_mode(self):
        """Enter chase mode - used by AIEngine"""
        # Directly chase the stored player reference
        if hasattr(self, '_last_player') and self._last_player:
            self.chase_player(self._last_player)

    def can_see_player(self, player=None, range=200):
        """
        Check if enemy can see player

        Args:
            player: Player object (optional, will be passed by AIEngine)
            range: Visibility range in pixels

        Returns:
            True if player is visible and within range
        """
        # This is called by AIEngine which passes player in update()
        # But we need to handle the case where player isn't passed
        # For now, store player reference when update is called
        if not hasattr(self, '_last_player'):
            return False

        player = self._last_player
        if not player:
            return False

        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # Can see if within range and not blocked
        return distance < range

    def jump(self):
        """Make enemy jump"""
        if self.on_ground:
            self.velocity_y = -10
            self.on_ground = False

    def attack(self):
        """Enemy attack action"""
        # TODO: Implement attack behavior (e.g., projectile, damage, animation)
        pass

    def take_damage(self):
        """Take damage and die if health <= 0"""
        self.health -= 1
        if self.health <= 0:
            self.is_alive = False

    def check_collision_with_player(self, player):
        """
        Check collision with player

        Args:
            player: Player object

        Returns:
            True if colliding
        """
        return self.rect.colliderect(player.rect)

    def is_defeated(self):
        """Check if enemy is defeated"""
        return not self.is_alive

    def set_patrol_range(self, patrol_range: int):
        """Set patrol range"""
        self.patrol_range = patrol_range

    def set_speed(self, speed: float):
        """Set movement speed"""
        self.speed = speed


class EnemyGroup(pygame.sprite.Group):
    """Group of enemies for easy management"""

    def __init__(self):
        """Initialize enemy group"""
        super().__init__()

    def create_enemy(self, x: float, y: float, width: int = ENEMY_WIDTH, height: int = ENEMY_HEIGHT, sprite_manager: SpriteManager = None, ai_type: str = "patrol"):
        """
        Create and add an enemy

        Args:
            x: X position
            y: Y position
            width: Width
            height: Height
            sprite_manager: SpriteManager instance
            ai_type: Type of AI

        Returns:
            Created Enemy object
        """
        enemy = Enemy(x, y, width, height, sprite_manager, ai_type)
        self.add(enemy)
        return enemy

    def update_all(self, player=None, platforms=None):
        """
        Update all enemies

        Args:
            player: Player object
            platforms: Platform group
        """
        for enemy in self:
            enemy.update(player, platforms)

    def check_collisions(self, player):
        """
        Check player collision with all enemies

        Args:
            player: Player object

        Returns:
            List of collided enemies
        """
        collided = []
        for enemy in self:
            if enemy.check_collision_with_player(player):
                collided.append(enemy)
        return collided

    def get_alive_count(self):
        """Get count of alive enemies"""
        return sum(1 for enemy in self if enemy.is_alive)
