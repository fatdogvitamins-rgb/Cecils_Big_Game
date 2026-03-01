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
        Create a true 3D-style isometric cube sprite

        Args:
            width: Width of sprite
            height: Height of sprite
            color: RGB color tuple

        Returns:
            pygame.Surface with 3D isometric cube
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Create an isometric 3D box effect using 3 visible faces

        # Main face (front-right) - the main colored side
        front_color = color
        front_points = [
            (width * 0.3, height * 0.7),      # bottom-left
            (width * 0.3, height * 0.2),      # top-left
            (width * 0.85, height * 0.2),     # top-right
            (width * 0.85, height * 0.7),     # bottom-right
        ]
        pygame.draw.polygon(surface, front_color, front_points)
        pygame.draw.polygon(surface, (0, 0, 0), front_points, 3)

        # Top face (darker - isometric top) - creates 3D depth
        top_color = tuple(min(255, c + 60) for c in color)
        top_points = [
            (width * 0.3, height * 0.2),      # left
            (width * 0.15, height * 0.05),    # top (receding)
            (width * 0.7, height * 0.05),     # right
            (width * 0.85, height * 0.2),     # bottom
        ]
        pygame.draw.polygon(surface, top_color, top_points)
        pygame.draw.polygon(surface, (0, 0, 0), top_points, 2)

        # Left side face (darker for shadow)
        left_color = tuple(max(0, c - 60) for c in color)
        left_points = [
            (width * 0.3, height * 0.2),      # top
            (width * 0.15, height * 0.05),    # back-top
            (width * 0.15, height * 0.5),     # back-bottom
            (width * 0.3, height * 0.7),      # front-bottom
        ]
        pygame.draw.polygon(surface, left_color, left_points)
        pygame.draw.polygon(surface, (0, 0, 0), left_points, 2)

        # Add highlight/shine on top for reflective effect
        shine_color = tuple(min(255, c + 100) for c in top_color)
        pygame.draw.line(surface, shine_color, (width * 0.2, height * 0.1), (width * 0.6, height * 0.08), 2)

        return surface

    def create_animated_sprite(self, width: int, height: int, frames: int = 4, color: Tuple[int, int, int] = (100, 150, 255)) -> List[pygame.Surface]:
        """
        Create an animated 3D isometric cube sprite with animation frames

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

            # Vary color brightness for animation effect
            brightness_factor = 0.8 + (i / frames) * 0.4  # Range from 0.8 to 1.2
            color_frame = tuple(int(c * brightness_factor) for c in color)
            color_frame = tuple(min(255, max(0, c)) for c in color_frame)

            # Draw 3D isometric cube with varying brightness
            # Front face
            front_color = color_frame
            front_points = [
                (width * 0.3, height * 0.7),
                (width * 0.3, height * 0.2),
                (width * 0.85, height * 0.2),
                (width * 0.85, height * 0.7),
            ]
            pygame.draw.polygon(surface, front_color, front_points)
            pygame.draw.polygon(surface, (0, 0, 0), front_points, 3)

            # Top face
            top_color = tuple(min(255, c + 70) for c in color_frame)
            top_points = [
                (width * 0.3, height * 0.2),
                (width * 0.15, height * 0.05),
                (width * 0.7, height * 0.05),
                (width * 0.85, height * 0.2),
            ]
            pygame.draw.polygon(surface, top_color, top_points)
            pygame.draw.polygon(surface, (0, 0, 0), top_points, 2)

            # Left side face
            left_color = tuple(max(0, c - 70) for c in color_frame)
            left_points = [
                (width * 0.3, height * 0.2),
                (width * 0.15, height * 0.05),
                (width * 0.15, height * 0.5),
                (width * 0.3, height * 0.7),
            ]
            pygame.draw.polygon(surface, left_color, left_points)
            pygame.draw.polygon(surface, (0, 0, 0), left_points, 2)

            # Highlight on top
            shine_color = tuple(min(255, c + 100) for c in top_color)
            pygame.draw.line(surface, shine_color, (width * 0.2, height * 0.1), (width * 0.6, height * 0.08), 2)

            # Add animation indicator - multiple dots showing motion
            indicator_color = (255, 100 + int(i * 20), 50)
            for dot_i in range(3):
                dot_x = width * 0.4 + (dot_i * 8)
                dot_y = height * 0.85 + int((i / frames) * 15) % 15
                pygame.draw.circle(surface, indicator_color, (int(dot_x), int(dot_y)), 2)

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
