"""
Transitions - Screen transition effects
Provides smooth fading between game states
"""

import pygame
from config.settings import *


class ScreenTransition:
    """Manages screen transitions with fade effects"""

    def __init__(self, duration_ms: int = 500):
        """
        Initialize transition

        Args:
            duration_ms: Duration of transition in milliseconds
        """
        self.duration_ms = duration_ms
        self.elapsed_ms = 0
        self.is_active = False
        self.fade_out = False  # True for fade out, False for fade in
        self.overlay_color = COLOR_BLACK

    def start(self, fade_out: bool = True, color=None):
        """
        Start a transition

        Args:
            fade_out: True to fade to black, False to fade in from black
            color: Color to fade to (default black)
        """
        self.is_active = True
        self.elapsed_ms = 0
        self.fade_out = fade_out
        if color:
            self.overlay_color = color

    def update(self, delta_ms: int):
        """
        Update transition state

        Args:
            delta_ms: Time since last update in milliseconds

        Returns:
            True if transition is complete
        """
        if not self.is_active:
            return False

        self.elapsed_ms += delta_ms

        if self.elapsed_ms >= self.duration_ms:
            self.is_active = False
            return True

        return False

    def get_alpha(self) -> int:
        """
        Get current overlay alpha value (0-255)

        Returns:
            Alpha value for overlay
        """
        if not self.is_active:
            return 0 if not self.fade_out else 255

        progress = self.elapsed_ms / self.duration_ms

        if self.fade_out:
            # Fading to black: alpha goes 0 -> 255
            return int(255 * progress)
        else:
            # Fading from black: alpha goes 255 -> 0
            return int(255 * (1 - progress))

    def draw(self, surface: pygame.Surface):
        """
        Draw transition overlay

        Args:
            surface: Surface to draw on
        """
        if self.elapsed_ms == 0 and not self.fade_out:
            # Full black at start of fade in
            surface.fill(self.overlay_color)
        elif self.is_active or (not self.fade_out and self.elapsed_ms < self.duration_ms):
            overlay = pygame.Surface((surface.get_width(), surface.get_height()))
            overlay.fill(self.overlay_color)
            overlay.set_alpha(self.get_alpha())
            surface.blit(overlay, (0, 0))


class TransitionManager:
    """Manages multiple screen transitions"""

    def __init__(self):
        """Initialize transition manager"""
        self.transitions = []
        self.delta_clock = pygame.time.Clock()

    def create_level_transition(self, duration_ms: int = 800) -> ScreenTransition:
        """
        Create a fade transition between levels

        Args:
            duration_ms: Duration in milliseconds

        Returns:
            ScreenTransition object for chaining
        """
        transition = ScreenTransition(duration_ms)
        self.transitions.append(transition)
        return transition

    def update(self):
        """Update all active transitions"""
        completed = []

        for transition in self.transitions:
            if transition.is_active:
                delta_ms = 16  # ~60 FPS
                if transition.update(delta_ms):
                    completed.append(transition)

        # Remove completed transitions
        for transition in completed:
            self.transitions.remove(transition)

    def draw(self, surface: pygame.Surface):
        """
        Draw all active transitions

        Args:
            surface: Surface to draw on
        """
        for transition in self.transitions:
            transition.draw(surface)

    def has_active_transitions(self) -> bool:
        """Check if any transitions are active"""
        return len(self.transitions) > 0 and any(t.is_active for t in self.transitions)
