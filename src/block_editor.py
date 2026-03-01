"""
Block Editor - Visual block-based programming for enemy AI
Scratch-style programming interface for creating enemy behaviors
"""

import pygame
import json
import os
from typing import List, Dict, Tuple, Optional
from config.settings import *


class AIBlock:
    """Represents a single AI behavior block"""

    BLOCK_WIDTH = 150
    BLOCK_HEIGHT = 50
    BLOCK_COLORS = {
        'movement': (100, 200, 100),
        'sensing': (100, 150, 255),
        'logic': (255, 200, 100),
        'action': (255, 100, 150),
        'control': (200, 100, 255),
    }

    def __init__(self, x: float, y: float, block_type: str, command: str, params: Dict = None):
        """
        Initialize AI block

        Args:
            x, y: Position on screen
            block_type: Type of block (movement, sensing, logic, action, control)
            command: Command name
            params: Optional parameters dictionary
        """
        self.x = x
        self.y = y
        self.block_type = block_type
        self.command = command
        self.params = params or {}
        self.rect = pygame.Rect(x, y, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.selected = False
        self.next_block = None  # Block that comes after this one
        self.input_block = None  # Block that feeds input to this one

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        """
        Draw the block

        Args:
            surface: Pygame surface to draw on
            font: Font for text
        """
        # Draw block background
        color = self.BLOCK_COLORS.get(self.block_type, (150, 150, 150))
        if self.selected:
            color = tuple(min(c + 50, 255) for c in color)

        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, COLOR_WHITE if self.selected else COLOR_DARK_GRAY, self.rect, 2)

        # Draw command text
        text = font.render(self.command, True, COLOR_WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

        # Draw connection points
        # Input connector (top)
        pygame.draw.circle(surface, COLOR_YELLOW, (self.rect.centerx, self.rect.top), 5)
        # Output connector (bottom)
        pygame.draw.circle(surface, COLOR_YELLOW, (self.rect.centerx, self.rect.bottom), 5)

    def contains_point(self, x: float, y: float) -> bool:
        """Check if point is inside block"""
        return self.rect.collidepoint(x, y)

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            'x': self.x,
            'y': self.y,
            'type': self.block_type,
            'command': self.command,
            'params': self.params
        }

    @staticmethod
    def from_dict(data: Dict) -> 'AIBlock':
        """Deserialize from dictionary"""
        block = AIBlock(data['x'], data['y'], data['type'], data['command'], data.get('params', {}))
        return block


class BlockEditor:
    """Visual block editor interface for AI programming"""

    # Predefined block templates
    BLOCK_TEMPLATES = {
        'movement': [
            {'command': 'Patrol', 'params': {'speed': 2, 'range': 100}},
            {'command': 'Chase Player', 'params': {'speed': 3}},
            {'command': 'Jump', 'params': {'power': 10}},
            {'command': 'Move Left', 'params': {'speed': 2}},
            {'command': 'Move Right', 'params': {'speed': 2}},
        ],
        'sensing': [
            {'command': 'See Player', 'params': {'range': 200}},
            {'command': 'On Ground', 'params': {}},
            {'command': 'Near Platform', 'params': {'range': 50}},
            {'command': 'Health Low', 'params': {'threshold': 1}},
        ],
        'logic': [
            {'command': 'If-Then', 'params': {}},
            {'command': 'While Loop', 'params': {}},
            {'command': 'Compare', 'params': {}},
        ],
        'action': [
            {'command': 'Attack', 'params': {}},
            {'command': 'Die', 'params': {}},
            {'command': 'Wait', 'params': {'duration': 1}},
            {'command': 'Animate', 'params': {'animation': 'attack'}},
        ],
    }

    def __init__(self, screen_width: int = SCREEN_WIDTH, screen_height: int = SCREEN_HEIGHT):
        """
        Initialize block editor

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.blocks: List[AIBlock] = []
        self.selected_block = None
        self.dragging = False
        self.drag_offset = (0, 0)
        self.current_ai_name = "Custom AI"
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

    def add_block(self, block_type: str, command: str, x: float = 100, y: float = 100) -> AIBlock:
        """
        Add a new block to the editor

        Args:
            block_type: Type of block
            command: Command name
            x, y: Position
        """
        block = AIBlock(x, y, block_type, command)
        self.blocks.append(block)
        return block

    def remove_block(self, block: AIBlock):
        """Remove a block"""
        if block in self.blocks:
            self.blocks.remove(block)
            if self.selected_block == block:
                self.selected_block = None

    def handle_input(self, mouse_pos: Tuple[int, int], mouse_buttons: Tuple[bool, bool, bool], events: List):
        """
        Handle input for block editor

        Args:
            mouse_pos: Current mouse position
            mouse_buttons: Mouse button states
            events: List of pygame events
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    if self.selected_block:
                        self.remove_block(self.selected_block)
                elif event.key == pygame.K_1:
                    self.add_block('movement', 'Patrol', mouse_pos[0], mouse_pos[1])
                elif event.key == pygame.K_2:
                    self.add_block('sensing', 'See Player', mouse_pos[0], mouse_pos[1])
                elif event.key == pygame.K_3:
                    self.add_block('logic', 'If-Then', mouse_pos[0], mouse_pos[1])
                elif event.key == pygame.K_4:
                    self.add_block('action', 'Attack', mouse_pos[0], mouse_pos[1])

        # Mouse dragging
        if mouse_buttons[0]:  # Left click
            if not self.dragging:
                # Check if clicking on a block
                for block in self.blocks:
                    if block.contains_point(mouse_pos[0], mouse_pos[1]):
                        self.selected_block = block
                        self.dragging = True
                        self.drag_offset = (mouse_pos[0] - block.x, mouse_pos[1] - block.y)
                        break
            else:
                # Drag the selected block
                if self.selected_block:
                    self.selected_block.x = mouse_pos[0] - self.drag_offset[0]
                    self.selected_block.y = mouse_pos[1] - self.drag_offset[1]
                    self.selected_block.rect.topleft = (self.selected_block.x, self.selected_block.y)
        else:
            self.dragging = False

    def draw(self, surface: pygame.Surface):
        """
        Draw the block editor interface

        Args:
            surface: Pygame surface to draw on
        """
        surface.fill(COLOR_DARK_GRAY)

        # Draw title
        title = self.font_large.render("BLOCK EDITOR - Design Enemy AI", True, COLOR_CYAN)
        surface.blit(title, (50, 20))

        # Draw work area
        pygame.draw.rect(surface, COLOR_BLACK, (50, 100, 900, 500))
        pygame.draw.rect(surface, COLOR_LIGHT_GRAY, (50, 100, 900, 500), 2)

        # Draw blocks
        for block in self.blocks:
            block.draw(surface, self.font_small)

            # Draw connection lines
            if block.next_block:
                start = (block.rect.centerx, block.rect.bottom)
                end = (block.next_block.rect.centerx, block.next_block.rect.top)
                pygame.draw.line(surface, COLOR_YELLOW, start, end, 2)

        # Draw block palette on the right
        self.draw_palette(surface)

        # Draw instructions
        self.draw_instructions(surface)

    def draw_palette(self, surface: pygame.Surface):
        """Draw palette of available blocks"""
        palette_x = 1000
        palette_y = 120

        title = self.font_medium.render("Block Types", True, COLOR_WHITE)
        surface.blit(title, (palette_x, palette_y))

        y = palette_y + 40
        for block_type, blocks in self.BLOCK_TEMPLATES.items():
            # Type header
            color = AIBlock.BLOCK_COLORS.get(block_type, (150, 150, 150))
            type_text = self.font_small.render(block_type.upper(), True, color)
            surface.blit(type_text, (palette_x, y))
            y += 28

            # Show 2 example blocks
            for i, block_data in enumerate(blocks[:2]):
                block_text = self.font_small.render(f"• {block_data['command']}", True, COLOR_LIGHT_GRAY)
                surface.blit(block_text, (palette_x + 10, y))
                y += 24

    def draw_instructions(self, surface: pygame.Surface):
        """Draw control instructions"""
        instructions = [
            "CONTROLS:",
            "1-4 Keys: Add block types",
            "Drag blocks to arrange",
            "DELETE key: Remove block",
            "Connect with lines",
            "S - Save  |  ESC - Exit",
        ]

        y = 620
        for instruction in instructions:
            text = self.font_small.render(instruction, True, COLOR_WHITE)
            surface.blit(text, (50, y))
            y += 25

    def compile_to_python(self) -> str:
        """
        Compile blocks to Python code

        Returns:
            Python code string
        """
        code = "# Auto-generated AI behavior code\n"
        code += "def enemy_behavior(enemy, player, level):\n"
        code += "    \"\"\"\n"
        code += "    Generated enemy AI behavior\n"
        code += "    \"\"\"\n"

        for i, block in enumerate(self.blocks):
            indent = "    "

            if block.command == "Patrol":
                code += f"{indent}enemy.patrol(speed={block.params.get('speed', 2)}, range={block.params.get('range', 100)})\n"
            elif block.command == "Chase Player":
                code += f"{indent}if enemy.can_see_player(player, range=200):\n"
                code += f"{indent}    enemy.chase(player, speed={block.params.get('speed', 3)})\n"
            elif block.command == "See Player":
                code += f"{indent}can_see = enemy.can_see_player(player, range={block.params.get('range', 200)})\n"
            elif block.command == "Jump":
                code += f"{indent}enemy.jump(power={block.params.get('power', 10)})\n"
            elif block.command == "Attack":
                code += f"{indent}enemy.attack()\n"
            elif block.command == "Die":
                code += f"{indent}enemy.die()\n"
            elif block.command == "If-Then":
                code += f"{indent}if can_see:\n"
                code += f"{indent}    pass  # Add conditions here\n"
            elif block.command == "Wait":
                code += f"{indent}enemy.wait({block.params.get('duration', 1)})\n"

        code += "    return True\n"
        return code

    def save_ai(self, filename: str = None):
        """
        Save AI design as JSON

        Args:
            filename: Name of AI to save
        """
        if filename is None:
            filename = self.current_ai_name

        ai_dir = "assets/ai"
        os.makedirs(ai_dir, exist_ok=True)

        data = {
            'name': filename,
            'blocks': [block.to_dict() for block in self.blocks],
            'code': self.compile_to_python()
        }

        filepath = os.path.join(ai_dir, f"{filename}.json")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"AI saved: {filepath}")

    def load_ai(self, filename: str):
        """
        Load AI from JSON

        Args:
            filename: Name of AI to load
        """
        ai_dir = "assets/ai"
        filepath = os.path.join(ai_dir, f"{filename}.json")

        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)

            self.current_ai_name = data['name']
            self.blocks = [AIBlock.from_dict(block_data) for block_data in data['blocks']]
            print(f"AI loaded: {filepath}")

    def get_list_of_ais(self) -> List[str]:
        """Get list of saved AIs"""
        ai_dir = "assets/ai"
        if os.path.exists(ai_dir):
            return [f[:-5] for f in os.listdir(ai_dir) if f.endswith('.json')]
        return []

    def create_example_ai(self):
        """Create an example patrol + chase AI"""
        self.blocks.clear()
        self.add_block('movement', 'Patrol', 150, 150)
        self.add_block('sensing', 'See Player', 150, 250)
        self.add_block('movement', 'Chase Player', 150, 350)
        self.add_block('action', 'Attack', 150, 450)
