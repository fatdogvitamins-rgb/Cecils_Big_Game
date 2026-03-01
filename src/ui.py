"""
UI - User interface and HUD system
"""

import pygame
from config.settings import *


class HUD:
    """Head-Up Display showing game information"""

    def __init__(self, screen_width: int = SCREEN_WIDTH, screen_height: int = SCREEN_HEIGHT):
        """
        Initialize HUD

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.padding = 20

    def draw(self, surface: pygame.Surface, player, level_number: int = 0, fps: float = 0):
        """
        Draw HUD elements

        Args:
            surface: Pygame surface to draw on
            player: Player object
            level_number: Current level number
            fps: Current FPS
        """
        # Draw health bar
        self.draw_health_bar(surface, player)

        # Draw score
        self.draw_score(surface, player)

        # Draw level
        self.draw_level(surface, level_number)

        # Draw FPS
        if fps > 0:
            self.draw_fps(surface, fps)

    def draw_health_bar(self, surface: pygame.Surface, player):
        """
        Draw player health bar

        Args:
            surface: Pygame surface
            player: Player object
        """
        bar_x = self.padding
        bar_y = self.padding
        bar_width = HEALTH_BAR_WIDTH
        bar_height = HEALTH_BAR_HEIGHT
        max_health = PLAYER_HEALTH

        # Background (dark red)
        pygame.draw.rect(surface, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Health fill (green)
        health_fill = (player.health / max_health) * bar_width
        if player.health > 0:
            pygame.draw.rect(surface, (0, 200, 0), (bar_x, bar_y, health_fill, bar_height))

        # Border
        pygame.draw.rect(surface, COLOR_WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

        # Health text
        health_text = self.font_small.render(f"Health: {player.health}/{max_health}", True, COLOR_WHITE)
        surface.blit(health_text, (bar_x + bar_width + 10, bar_y + 5))

    def draw_score(self, surface: pygame.Surface, player):
        """
        Draw player score

        Args:
            surface: Pygame surface
            player: Player object
        """
        score_text = self.font_medium.render(f"Score: {player.score}", True, COLOR_YELLOW)
        score_rect = score_text.get_rect()
        score_rect.topright = (self.screen_width - self.padding, self.padding)
        surface.blit(score_text, score_rect)

    def draw_level(self, surface: pygame.Surface, level_number: int):
        """
        Draw current level

        Args:
            surface: Pygame surface
            level_number: Level number
        """
        level_text = self.font_small.render(f"Level: {level_number + 1}", True, COLOR_CYAN)
        level_rect = level_text.get_rect()
        level_rect.topright = (self.screen_width - self.padding, self.padding + 40)
        surface.blit(level_text, level_rect)

    def draw_fps(self, surface: pygame.Surface, fps: float):
        """
        Draw FPS counter

        Args:
            surface: Pygame surface
            fps: Current FPS
        """
        fps_text = self.font_small.render(f"FPS: {int(fps)}", True, COLOR_WHITE)
        fps_rect = fps_text.get_rect()
        fps_rect.bottomright = (self.screen_width - self.padding, self.screen_height - self.padding)
        surface.blit(fps_text, fps_rect)


class Menu:
    """Main menu screen"""

    def __init__(self, screen_width: int = SCREEN_WIDTH, screen_height: int = SCREEN_HEIGHT):
        """
        Initialize menu

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.Font(None, 96)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.buttons = []
        self.selected_button = 0
        self.setup_buttons()

    def setup_buttons(self):
        """Setup menu buttons"""
        button_width = 300
        button_height = 60
        button_y_start = self.screen_height // 2 + 50

        self.buttons = [
            {
                'text': 'Start Game',
                'rect': pygame.Rect(self.screen_width // 2 - button_width // 2, button_y_start, button_width, button_height),
                'action': 'start'
            },
            {
                'text': 'Character Designer',
                'rect': pygame.Rect(self.screen_width // 2 - button_width // 2, button_y_start + 100, button_width, button_height),
                'action': 'designer'
            },
            {
                'text': 'Block Editor',
                'rect': pygame.Rect(self.screen_width // 2 - button_width // 2, button_y_start + 200, button_width, button_height),
                'action': 'editor'
            },
            {
                'text': 'Quit',
                'rect': pygame.Rect(self.screen_width // 2 - button_width // 2, button_y_start + 300, button_width, button_height),
                'action': 'quit'
            }
        ]

    def draw(self, surface: pygame.Surface):
        """
        Draw menu

        Args:
            surface: Pygame surface to draw on
        """
        # Draw background with gradient-like effect
        surface.fill(COLOR_DARK_GRAY)

        # Add decorative top bar
        pygame.draw.rect(surface, COLOR_CYAN, (0, 0, self.screen_width, 80))

        # Draw title in the bar
        title_text = self.font_large.render("CECIL'S BIG GAME", True, COLOR_BLACK)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 40))
        surface.blit(title_text, title_rect)

        # Draw subtitle below title
        subtitle_text = self.font_small.render("Press UP/DOWN to select, ENTER to choose", True, COLOR_LIGHT_GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 250))
        surface.blit(subtitle_text, subtitle_rect)

        # Draw buttons with better spacing
        button_width = 350
        button_height = 70
        button_x = self.screen_width // 2 - button_width // 2
        button_y_start = 350

        for i, button in enumerate(self.buttons):
            button_y = button_y_start + (i * 100)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button['rect'] = button_rect

            button_color = COLOR_YELLOW if i == self.selected_button else COLOR_WHITE
            button_bg_color = (100, 100, 0) if i == self.selected_button else (50, 50, 50)

            # Button background
            pygame.draw.rect(surface, button_bg_color, button_rect)
            pygame.draw.rect(surface, button_color, button_rect, 3)

            # Button text
            button_text = self.font_medium.render(button['text'], True, button_color)
            button_text_rect = button_text.get_rect(center=button_rect.center)
            surface.blit(button_text, button_text_rect)

    def handle_input(self, keys):
        """
        Handle menu input

        Args:
            keys: Pygame keys tuple from pygame.key.get_pressed()

        Returns:
            Action string or None
        """
        # Up/Down navigation
        if keys[pygame.K_UP]:
            self.selected_button = (self.selected_button - 1) % len(self.buttons)
        elif keys[pygame.K_DOWN]:
            self.selected_button = (self.selected_button + 1) % len(self.buttons)

        # Select button
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            return self.buttons[self.selected_button]['action']

        return None

    def get_button_at(self, pos):
        """
        Get button at position

        Args:
            pos: (x, y) position tuple

        Returns:
            Button action or None
        """
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                return button['action']
        return None


class PauseMenu:
    """Pause menu overlay"""

    def __init__(self, screen_width: int = SCREEN_WIDTH, screen_height: int = SCREEN_HEIGHT):
        """
        Initialize pause menu

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)

    def draw(self, surface: pygame.Surface):
        """
        Draw pause menu

        Args:
            surface: Pygame surface to draw on
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(COLOR_BLACK)
        surface.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.font_large.render("PAUSED", True, COLOR_YELLOW)
        pause_rect = pause_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
        surface.blit(pause_text, pause_rect)

        # Resume instructions
        resume_text = self.font_medium.render("Press P or ESC to Resume", True, COLOR_WHITE)
        resume_rect = resume_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        surface.blit(resume_text, resume_rect)
