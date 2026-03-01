"""
Game - Main game engine and loop
"""

import pygame
import sys
from config.settings import *
from src.player import Player
from src.platform import PlatformGroup
from src.enemy import EnemyGroup
from src.level import Level
from src.ui import HUD, Menu, PauseMenu
from src.sprite_manager import SpriteManager
from src.tinkercad_editor import CharacterDesigner
from src.block_editor import BlockEditor
from src.audio_manager import AudioManager
from src.transitions import TransitionManager


class Game:
    """Main game class"""

    def __init__(self):
        """Initialize game"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cecil's Big Game - Platform Adventure")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = STATE_MENU
        self.current_level_number = START_LEVEL
        self.fullscreen = False

        # Initialize audio manager
        self.audio_manager = AudioManager()

        # Initialize transition manager
        self.transition_manager = TransitionManager()

        # Initialize sprite manager
        self.sprite_manager = SpriteManager()

        # Initialize game components
        self.player = None
        self.level = None
        self.hud = HUD(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.pause_menu = PauseMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.character_designer = CharacterDesigner(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.block_editor = BlockEditor(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.block_editor.create_example_ai()
        self.fps_clock = pygame.time.Clock()
        self.current_events = []  # Store events for passing to editors

    def start_new_game(self):
        """Start a new game"""
        self.current_level_number = START_LEVEL
        self.load_level(self.current_level_number)
        self.state = STATE_PLAYING

    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cecil's Big Game - Platform Adventure")

    def load_level(self, level_number: int):
        """
        Load a level

        Args:
            level_number: Level number to load
        """
        if level_number >= NUM_LEVELS:
            self.end_game()
            return

        # Start fade in transition
        transition = self.transition_manager.create_level_transition(600)
        transition.start(fade_out=False)  # Fade in from black

        self.level = Level(level_number, self.sprite_manager)
        self.player = Player(self.level.player_start_x, self.level.player_start_y, self.sprite_manager)

    def handle_events(self):
        """Handle game events"""
        self.current_events = []  # Reset events each frame

        for event in pygame.event.get():
            self.current_events.append(event)  # Store for editors

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                # Fullscreen toggle (F key)
                if event.key == pygame.K_f:
                    self.toggle_fullscreen()

                if self.state == STATE_MENU:
                    if event.key == pygame.K_UP:
                        self.menu.selected_button = (self.menu.selected_button - 1) % len(self.menu.buttons)
                        self.audio_manager.play_menu_select()
                    elif event.key == pygame.K_DOWN:
                        self.menu.selected_button = (self.menu.selected_button + 1) % len(self.menu.buttons)
                        self.audio_manager.play_menu_select()
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        action = self.menu.buttons[self.menu.selected_button]['action']
                        self.audio_manager.play_menu_select()
                        if action == 'start':
                            self.start_new_game()
                        elif action == 'designer':
                            self.state = STATE_EDITOR
                        elif action == 'editor':
                            self.state = 'block_editor'
                        elif action == 'quit':
                            self.running = False

                elif self.state == STATE_EDITOR:
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_MENU
                        self.menu.selected_button = 0
                    elif event.key == pygame.K_s:
                        self.character_designer.save_design()

                elif self.state == 'block_editor':
                    if event.key == pygame.K_ESCAPE:
                        self.state = STATE_MENU
                        self.menu.selected_button = 0
                    elif event.key == pygame.K_s:
                        self.block_editor.save_ai()

                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.state = STATE_PAUSED

                elif self.state == STATE_PAUSED:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.state = STATE_PLAYING

    def update(self):
        """Update game logic"""
        # Update transitions
        self.transition_manager.update()

        if self.state == STATE_MENU:
            # Menu input handled in draw
            pass

        elif self.state == STATE_EDITOR:
            # Character designer update
            keys = pygame.key.get_pressed()
            self.character_designer.handle_input(keys, self.current_events)

        elif self.state == 'block_editor':
            # Block editor update
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            self.block_editor.handle_input(mouse_pos, mouse_buttons, self.current_events)

        elif self.state == STATE_PLAYING:
            # Get input
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)

            # Update player
            self.player.update(gravity=True)

            # Play jump sound if jump just happened
            if self.player.is_jumping and not self.player.jump_sound_played:
                self.audio_manager.play_jump()
                self.player.jump_sound_played = True

            # Check platform collisions
            self.level.platforms.check_collisions(self.player)

            # Play land sound when landing (transition from not on ground to on ground)
            if self.player.on_ground and not self.player.land_sound_played:
                self.audio_manager.play_land()
                self.player.land_sound_played = True

            # Update level
            self.level.update(self.player)

            # Check level complete
            if self.level.is_complete():
                self.audio_manager.play_level_complete()
                self.state = STATE_LEVEL_COMPLETE
                return

            # Check game over (fall off map)
            if self.player.y > SCREEN_HEIGHT:
                self.player.take_damage()
                if self.player.health <= 0:
                    self.audio_manager.play_game_over()
                    self.state = STATE_GAME_OVER
                else:
                    # Reset to level start
                    self.player.reset_position(self.level.player_start_x, self.level.player_start_y)

            # Check enemy collisions
            collided_enemies = self.level.enemies.check_collisions(self.player)
            for enemy in collided_enemies:
                self.player.take_damage()
                self.audio_manager.play_enemy_defeat()
                if self.player.health <= 0:
                    self.audio_manager.play_game_over()
                    self.state = STATE_GAME_OVER

        elif self.state == STATE_LEVEL_COMPLETE:
            # Wait for input, then load next level
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                # Start fade out transition
                transition = self.transition_manager.create_level_transition(500)
                transition.start(fade_out=True)  # Fade to black

                self.current_level_number += 1
                if self.current_level_number >= NUM_LEVELS:
                    # Game complete - go to menu
                    self.end_game()
                else:
                    # Give transition time to complete, then load level
                    pygame.time.wait(300)  # Wait 300ms before loading
                    self.load_level(self.current_level_number)
                    self.state = STATE_PLAYING

        elif self.state == STATE_GAME_OVER:
            # Wait for input to restart or go to menu
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.load_level(self.current_level_number)
                self.state = STATE_PLAYING
            elif keys[pygame.K_RETURN]:
                self.state = STATE_MENU
                self.menu.selected_button = 0

    def draw(self):
        """Draw everything"""
        self.screen.fill(COLOR_SKY_BLUE)

        if self.state == STATE_MENU:
            self.menu.draw(self.screen)

        elif self.state == STATE_EDITOR:
            self.character_designer.draw(self.screen)

        elif self.state == 'block_editor':
            self.block_editor.draw(self.screen)

        elif self.state == STATE_PLAYING:
            # Draw level
            self.level.draw(self.screen)

            # Draw player
            self.screen.blit(self.player.image, self.player.rect)

            # Draw HUD
            self.hud.draw(self.screen, self.player, self.current_level_number, self.fps_clock.get_fps())

        elif self.state == STATE_PAUSED:
            # Draw game behind pause menu
            self.level.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            self.pause_menu.draw(self.screen)

        elif self.state == STATE_LEVEL_COMPLETE:
            # Draw completion screen
            self.level.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)

            # Overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(COLOR_BLACK)
            self.screen.blit(overlay, (0, 0))

            # Level complete message
            font_large = pygame.font.Font(None, 72)
            font_medium = pygame.font.Font(None, 48)

            level_complete_text = font_large.render("LEVEL COMPLETE!", True, COLOR_YELLOW)
            level_complete_rect = level_complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(level_complete_text, level_complete_rect)

            next_text = font_medium.render("Press SPACE for next level", True, COLOR_WHITE)
            next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(next_text, next_rect)

        elif self.state == STATE_GAME_OVER:
            # Draw game over screen
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(COLOR_BLACK)
            self.screen.blit(overlay, (0, 0))

            # Game over message
            font_large = pygame.font.Font(None, 96)
            font_medium = pygame.font.Font(None, 48)

            gameover_text = font_large.render("GAME OVER", True, COLOR_RED)
            gameover_rect = gameover_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
            self.screen.blit(gameover_text, gameover_rect)

            score_text = font_medium.render(f"Final Score: {self.player.score}", True, COLOR_WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(score_text, score_rect)

            restart_text = font_medium.render("Press SPACE to retry or ENTER for menu", True, COLOR_CYAN)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(restart_text, restart_rect)

        # Draw any active transitions (on top of everything)
        self.transition_manager.draw(self.screen)

        pygame.display.flip()

    def end_game(self):
        """End the game"""
        self.state = STATE_MENU
        self.menu.selected_button = 0

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def quit(self):
        """Quit the game"""
        self.running = False
