"""
Sprite Manager - Handles sprite loading, caching, and animation
"""

import os
import pygame
from typing import Dict, List, Tuple, Optional
from PIL import Image, ImageDraw
import io

class SpriteManager:
    """Manages sprite loading, caching, and animation"""

    def __init__(self):
        """Initialize sprite manager"""
        self.sprite_cache: Dict[str, pygame.Surface] = {}
        self.animation_cache: Dict[str, List[pygame.Surface]] = {}
        self.sprites_dir = "assets/sprites"

        # Ensure sprites directory exists
        os.makedirs(self.sprites_dir, exist_ok=True)

    def load_sprite(self, filename: str, width: int = None, height: int = None) -> pygame.Surface:
        """
        Load a sprite from file with caching

        Args:
            filename: Path to sprite file
            width: Optional width to scale to
            height: Optional height to scale to

        Returns:
            Loaded pygame.Surface
        """
        # Check cache first
        cache_key = f"{filename}_{width}_{height}"
        if cache_key in self.sprite_cache:
            return self.sprite_cache[cache_key]

        # Try to load from file
        filepath = os.path.join(self.sprites_dir, filename)
        if os.path.exists(filepath):
            sprite = pygame.image.load(filepath).convert_alpha()
            if width and height:
                sprite = pygame.transform.scale(sprite, (width, height))
            self.sprite_cache[cache_key] = sprite
            return sprite
        else:
            # Return a placeholder if file not found
            return self.create_placeholder_sprite(width or 32, height or 32)

    def create_placeholder_sprite(self, width: int, height: int, color: Tuple[int, int, int] = (200, 200, 200)) -> pygame.Surface:
        """
        Create a placeholder colored rectangle sprite

        Args:
            width: Width of sprite
            height: Height of sprite
            color: RGB color tuple

        Returns:
            pygame.Surface with colored rectangle
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, (0, 0, width, height))
        pygame.draw.rect(surface, (100, 100, 100), (0, 0, width, height), 2)
        return surface

    def create_animated_sprite(self, width: int, height: int, frames: int = 4, color: Tuple[int, int, int] = (100, 150, 255)) -> List[pygame.Surface]:
        """
        Create an animated sprite (for testing/placeholder)

        Args:
            width: Width of each frame
            height: Height of each frame
            frames: Number of animation frames
            color: RGB color tuple

        Returns:
            List of pygame.Surface frames
        """
        frame_list = []
        for i in range(frames):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            # Create simple animation by varying shading
            shade = 100 + int((i / frames) * 100)
            color_frame = (shade, shade + 50, 255)
            pygame.draw.rect(surface, color_frame, (0, 0, width, height))
            pygame.draw.rect(surface, (100, 100, 100), (0, 0, width, height), 2)
            # Add simple animation indicator
            pygame.draw.circle(surface, (255, 255, 0), (width // 2, height // 4 + i), 4)
            frame_list.append(surface)

        return frame_list

    def load_animation(self, name: str, frames: int = 4) -> List[pygame.Surface]:
        """
        Load or create an animation

        Args:
            name: Name of animation
            frames: Number of frames

        Returns:
            List of pygame.Surface frames
        """
        if name in self.animation_cache:
            return self.animation_cache[name]

        # Try to load from file first
        frame_list = []
        for i in range(frames):
            filename = f"{name}_{i}.png"
            filepath = os.path.join(self.sprites_dir, filename)
            if os.path.exists(filepath):
                surface = pygame.image.load(filepath).convert_alpha()
                frame_list.append(surface)

        # If no files found, create placeholder
        if not frame_list:
            frame_list = self.create_animated_sprite(32, 32, frames)

        self.animation_cache[name] = frame_list
        return frame_list


class AnimatedSprite(pygame.sprite.Sprite):
    """Base class for animated sprites"""

    def __init__(self, x: float, y: float, frames: List[pygame.Surface], animation_speed: float = 0.1):
        """
        Initialize animated sprite

        Args:
            x: X position
            y: Y position
            frames: List of animation frames
            animation_speed: Speed of animation (change per frame)
        """
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.animation_speed = animation_speed
        self.animation_counter = 0
        self.image = frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y

    def update(self):
        """Update animation frame"""
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def set_position(self, x: float, y: float):
        """Update position"""
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)
