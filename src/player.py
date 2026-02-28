"""
Player - Player character class with movement, jumping, and animation
"""

import pygame
from config.settings import *
from src.sprite_manager import AnimatedSprite, SpriteManager


class Player(pygame.sprite.Sprite):
    """Player character with movement and physics"""

    def __init__(self, x: float, y: float, sprite_manager: SpriteManager):
        """
        Initialize player

        Args:
            x: Starting X position
            y: Starting Y position
            sprite_manager: SpriteManager instance
        """
        super().__init__()
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False
        self.is_falling = False
        self.can_double_jump = True
        self.on_ground = False
        self.on_wall = False
        self.wall_slide = False
        self.health = PLAYER_HEALTH
        self.score = 0
        self.facing_right = True
        self.move_speed = MOVE_SPEED
        self.jump_power = JUMP_POWER
        self.sprite_manager = sprite_manager
        self.animation_frame = 0
        self.animation_counter = 0

        # Create player animation frames
        self.idle_frames = sprite_manager.create_animated_sprite(self.width, self.height, 4, (100, 150, 255))
        self.run_frames = sprite_manager.create_animated_sprite(self.width, self.height, 6, (100, 200, 255))
        self.jump_frame = sprite_manager.create_placeholder_sprite(self.width, self.height, (150, 150, 255))
        self.fall_frame = sprite_manager.create_placeholder_sprite(self.width, self.height, (100, 100, 200))

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.current_animation = 'idle'

    def handle_input(self, keys: pygame.key.ScalarKeyType):
        """
        Handle keyboard input for player movement

        Args:
            keys: Pygame keys dict
        """
        self.velocity_x = 0

        # Left movement
        if any(keys.get_pressed()[pygame.K_LEFT] for _ in [1]) or any(k in ['a', 'A'] for k in [chr(k) for k in range(256) if keys.get_pressed()[k]]):
            self.velocity_x = -self.move_speed
            self.facing_right = False

        # Right movement
        if any(keys.get_pressed()[pygame.K_RIGHT] for _ in [1]) or any(k in ['d', 'D'] for k in [chr(k) for k in range(256) if keys.get_pressed()[k]]):
            self.velocity_x = self.move_speed
            self.facing_right = True

        # Jump
        if keys.get_pressed()[pygame.K_SPACE] or keys.get_pressed()[pygame.K_UP] or keys.get_pressed()[pygame.K_w]:
            if self.on_ground and not self.is_jumping:
                self.jump()
            elif self.can_double_jump and not self.on_ground and not self.on_wall:
                self.double_jump()

    def jump(self):
        """Execute jump"""
        self.velocity_y = -self.jump_power
        self.is_jumping = True
        self.on_ground = False
        self.can_double_jump = True

    def double_jump(self):
        """Execute double jump"""
        self.velocity_y = -self.jump_power
        self.can_double_jump = False

    def apply_gravity(self):
        """Apply gravity to player"""
        if not self.on_ground:
            self.velocity_y += GRAVITY
            if self.velocity_y > MAX_FALL_SPEED:
                self.velocity_y = MAX_FALL_SPEED

        # Wall slide
        if self.on_wall and self.velocity_y > 0 and not self.on_ground:
            self.velocity_y *= 0.9  # Slow fall speed on wall
            self.wall_slide = True
        else:
            self.wall_slide = False

    def update(self, gravity=True):
        """
        Update player state

        Args:
            gravity: Whether to apply gravity
        """
        if gravity:
            self.apply_gravity()

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Update rect
        self.rect.topleft = (self.x, self.y)

        # Update animation
        self.update_animation()

        # Reset collision state
        self.on_ground = False
        self.on_wall = False

    def update_animation(self):
        """Update player animation"""
        if self.on_ground:
            if self.velocity_x != 0:
                self.current_animation = 'run'
                frames = self.run_frames
            else:
                self.current_animation = 'idle'
                frames = self.idle_frames
        elif self.velocity_y < 0:
            self.current_animation = 'jump'
            frames = [self.jump_frame]
        else:
            self.current_animation = 'fall'
            frames = [self.fall_frame]

        # Animate frames
        self.animation_counter += 0.2
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.animation_frame = (self.animation_frame + 1) % len(frames)

        self.image = frames[self.animation_frame]

        # Flip sprite if facing left
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def check_collision_with_platform(self, platform):
        """
        Check collision with platform and handle it

        Args:
            platform: Platform object
        """
        if self.rect.colliderect(platform.rect):
            # Landing on top
            if self.velocity_y > 0 and self.rect.bottom > platform.rect.top:
                self.y = platform.rect.top - self.height
                self.rect.y = self.y
                self.velocity_y = 0
                self.on_ground = True
                self.is_jumping = False
            # Hitting bottom
            elif self.velocity_y < 0 and self.rect.top < platform.rect.bottom:
                self.y = platform.rect.bottom
                self.rect.y = self.y
                self.velocity_y = 0

            # Wall collision (left/right)
            if self.velocity_x > 0 and self.rect.right > platform.rect.left:
                self.x = platform.rect.left - self.width
                self.rect.x = self.x
                self.velocity_x = 0
                self.on_wall = True
            elif self.velocity_x < 0 and self.rect.left < platform.rect.right:
                self.x = platform.rect.right
                self.rect.x = self.x
                self.velocity_x = 0
                self.on_wall = True

    def take_damage(self):
        """Reduce health"""
        self.health -= 1

    def heal(self):
        """Increase health"""
        if self.health < PLAYER_HEALTH:
            self.health += 1

    def add_score(self, points: int):
        """Add points to score"""
        self.score += points

    def reset_position(self, x: float, y: float):
        """Reset player position"""
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.rect.topleft = (self.x, self.y)
        self.on_ground = False
        self.is_jumping = False
