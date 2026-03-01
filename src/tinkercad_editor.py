"""
Tinkercad Editor - 3D Character Designer
Allows creating custom 3D characters and enemies that convert to 2D sprites
"""

import pygame
import json
import math
import os
from typing import List, Dict, Tuple
from config.settings import *


class Box3D:
    """Represents a 3D box/cube in the editor"""

    def __init__(self, x: float, y: float, z: float, width: float, height: float, depth: float, color: Tuple[int, int, int]):
        """
        Initialize 3D box

        Args:
            x, y, z: Position in 3D space
            width, height, depth: Dimensions
            color: RGB color
        """
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth
        self.color = color
        self.visible = True

    def rotate_x(self, angle: float):
        """Rotate around X axis"""
        rad = math.radians(angle)
        new_y = self.y * math.cos(rad) - self.z * math.sin(rad)
        new_z = self.y * math.sin(rad) + self.z * math.cos(rad)
        self.y = new_y
        self.z = new_z

    def rotate_y(self, angle: float):
        """Rotate around Y axis"""
        rad = math.radians(angle)
        new_x = self.x * math.cos(rad) - self.z * math.sin(rad)
        new_z = self.x * math.sin(rad) + self.z * math.cos(rad)
        self.x = new_x
        self.z = new_z

    def rotate_z(self, angle: float):
        """Rotate around Z axis"""
        rad = math.radians(angle)
        new_x = self.x * math.cos(rad) - self.y * math.sin(rad)
        new_y = self.x * math.sin(rad) + self.y * math.cos(rad)
        self.x = new_x
        self.y = new_y

    def project_2d(self, camera_distance: float = 500) -> List[Tuple[float, float]]:
        """
        Project 3D box corners to 2D screen space

        Args:
            camera_distance: Distance from camera

        Returns:
            List of 2D projected points
        """
        # Box corners in 3D
        corners = [
            (self.x - self.width/2, self.y - self.height/2, self.z - self.depth/2),
            (self.x + self.width/2, self.y - self.height/2, self.z - self.depth/2),
            (self.x + self.width/2, self.y + self.height/2, self.z - self.depth/2),
            (self.x - self.width/2, self.y + self.height/2, self.z - self.depth/2),
            (self.x - self.width/2, self.y - self.height/2, self.z + self.depth/2),
            (self.x + self.width/2, self.y - self.height/2, self.z + self.depth/2),
            (self.x + self.width/2, self.y + self.height/2, self.z + self.depth/2),
            (self.x - self.width/2, self.y + self.height/2, self.z + self.depth/2),
        ]

        # Project to 2D
        projected = []
        for cx, cy, cz in corners:
            scale = camera_distance / (camera_distance - cz)
            px = int(640 + cx * scale)
            py = int(360 + cy * scale)
            projected.append((px, py))

        return projected

    def to_dict(self) -> Dict:
        """Serialize to dictionary"""
        return {
            'x': self.x, 'y': self.y, 'z': self.z,
            'width': self.width, 'height': self.height, 'depth': self.depth,
            'color': self.color, 'visible': self.visible
        }

    @staticmethod
    def from_dict(data: Dict) -> 'Box3D':
        """Deserialize from dictionary"""
        box = Box3D(data['x'], data['y'], data['z'],
                    data['width'], data['height'], data['depth'],
                    tuple(data['color']))
        box.visible = data.get('visible', True)
        return box


class CharacterDesigner:
    """3D Character designer interface"""

    def __init__(self, screen_width: int = SCREEN_WIDTH, screen_height: int = SCREEN_HEIGHT):
        """
        Initialize character designer

        Args:
            screen_width: Screen width
            screen_height: Screen height
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.boxes: List[Box3D] = []
        self.selected_box = None
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        self.camera_distance = 500
        self.current_design_name = "Custom Character"
        self.mode = 'view'  # 'view' or 'edit'
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

        # Default starter design
        self.create_default_character()

    def create_default_character(self):
        """Create a simple default character"""
        self.boxes = [
            Box3D(0, -30, 0, 30, 40, 20, (100, 150, 255)),  # Head
            Box3D(0, 20, 0, 40, 60, 20, (100, 200, 255)),   # Body
            Box3D(-20, 50, 0, 20, 40, 20, (150, 150, 200)), # Left leg
            Box3D(20, 50, 0, 20, 40, 20, (150, 150, 200)),  # Right leg
        ]

    def add_box(self, x: float = 0, y: float = 0, z: float = 0,
                width: float = 30, height: float = 30, depth: float = 20,
                color: Tuple[int, int, int] = (100, 200, 100)):
        """
        Add a new box to the design

        Args:
            x, y, z: Position
            width, height, depth: Dimensions
            color: RGB color
        """
        self.boxes.append(Box3D(x, y, z, width, height, depth, color))
        self.selected_box = self.boxes[-1]

    def remove_selected(self):
        """Remove selected box"""
        if self.selected_box and self.selected_box in self.boxes:
            self.boxes.remove(self.selected_box)
            self.selected_box = self.boxes[0] if self.boxes else None

    def handle_input(self, keys, events):
        """
        Handle input for character designer

        Args:
            keys: Pygame keys tuple
            events: List of pygame events
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.add_box()
                elif event.key == pygame.K_d:
                    self.remove_selected()
                elif event.key == pygame.K_c:
                    self.create_default_character()
                elif event.key == pygame.K_s:
                    self.save_design()

        # Rotation controls
        if keys[pygame.K_LEFT]:
            self.rotation_y -= 2
        if keys[pygame.K_RIGHT]:
            self.rotation_y += 2
        if keys[pygame.K_UP]:
            self.rotation_x -= 2
        if keys[pygame.K_DOWN]:
            self.rotation_x += 2

        # Box manipulation
        if self.selected_box:
            if keys[pygame.K_w]:
                self.selected_box.y -= 2
            if keys[pygame.K_s]:
                self.selected_box.y += 2
            if keys[pygame.K_e]:
                self.selected_box.width += 2
            if keys[pygame.K_q]:
                self.selected_box.width = max(5, self.selected_box.width - 2)

    def draw(self, surface: pygame.Surface):
        """
        Draw the character designer

        Args:
            surface: Pygame surface to draw on
        """
        surface.fill(COLOR_DARK_GRAY)

        # Draw title
        title = self.font_large.render("3D CHARACTER DESIGNER", True, COLOR_CYAN)
        surface.blit(title, (50, 20))

        # Draw design area background
        pygame.draw.rect(surface, COLOR_BLACK, (50, 100, 800, 500))
        pygame.draw.rect(surface, COLOR_LIGHT_GRAY, (50, 100, 800, 500), 2)

        # Apply rotations to all boxes
        for box in self.boxes:
            box.rotate_x(self.rotation_x / 100)
            box.rotate_y(self.rotation_y / 100)
            box.rotate_z(self.rotation_z / 100)

        # Draw boxes (sorted by depth for proper rendering)
        boxes_sorted = sorted(self.boxes, key=lambda b: b.z)
        for box in boxes_sorted:
            if box.visible:
                self.draw_3d_box(surface, box)

        # Draw controls
        self.draw_controls(surface)

    def draw_3d_box(self, surface: pygame.Surface, box: Box3D):
        """
        Draw a 3D box on screen

        Args:
            surface: Pygame surface
            box: Box3D object to draw
        """
        # Get 2D projection
        points = box.project_2d(self.camera_distance)

        # Draw box edges
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Front face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Back face
            (0, 4), (1, 5), (2, 6), (3, 7),  # Connecting edges
        ]

        line_color = COLOR_YELLOW if box == self.selected_box else box.color
        for edge in edges:
            p1 = points[edge[0]]
            p2 = points[edge[1]]
            pygame.draw.line(surface, line_color, p1, p2, 2)

        # Draw filled face (front)
        front_face = [points[0], points[1], points[2], points[3]]
        face_color = box.color
        pygame.draw.polygon(surface, face_color, front_face)

    def draw_controls(self, surface: pygame.Surface):
        """Draw control instructions"""
        controls = [
            "CONTROLS:",
            "Arrow Keys - Rotate model",
            "A - Add box  |  D - Remove box  |  C - Reset",
            "W/S - Move box  |  E/Q - Resize",
            "SPACEBAR - Export to sprite  |  ESC - Exit",
        ]

        y = 620
        for control in controls:
            text = self.font_small.render(control, True, COLOR_WHITE)
            surface.blit(text, (50, y))
            y += 30

    def export_to_sprite(self, width: int = 64, height: int = 64) -> pygame.Surface:
        """
        Export the 3D design as a 2D sprite

        Args:
            width: Sprite width
            height: Sprite height

        Returns:
            pygame.Surface with the rendered sprite
        """
        # Create a temporary surface for rendering
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)

        # Render from current angle
        scale_x = width / 800
        scale_y = height / 500

        for box in self.boxes:
            if box.visible:
                points = box.project_2d(self.camera_distance)
                # Scale points to sprite size
                scaled_points = [
                    (int((p[0] - 50) * scale_x), int((p[1] - 100) * scale_y))
                    for p in points
                ]

                # Draw on sprite
                if any(0 <= p[0] < width and 0 <= p[1] < height for p in scaled_points):
                    front_face = [scaled_points[0], scaled_points[1], scaled_points[2], scaled_points[3]]
                    try:
                        pygame.draw.polygon(sprite, box.color, front_face)
                    except:
                        pass

        return sprite

    def save_design(self, filename: str = None):
        """
        Save design as JSON

        Args:
            filename: Name of design to save
        """
        if filename is None:
            filename = self.current_design_name

        designs_dir = "assets/designs"
        os.makedirs(designs_dir, exist_ok=True)

        data = {
            'name': filename,
            'boxes': [box.to_dict() for box in self.boxes],
            'rotation': {
                'x': self.rotation_x,
                'y': self.rotation_y,
                'z': self.rotation_z
            }
        }

        filepath = os.path.join(designs_dir, f"{filename}.json")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Design saved: {filepath}")

    def load_design(self, filename: str):
        """
        Load design from JSON

        Args:
            filename: Name of design to load
        """
        designs_dir = "assets/designs"
        filepath = os.path.join(designs_dir, f"{filename}.json")

        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)

            self.current_design_name = data['name']
            self.boxes = [Box3D.from_dict(box_data) for box_data in data['boxes']]
            rot = data.get('rotation', {})
            self.rotation_x = rot.get('x', 0)
            self.rotation_y = rot.get('y', 0)
            self.rotation_z = rot.get('z', 0)
            self.selected_box = self.boxes[0] if self.boxes else None

            print(f"Design loaded: {filepath}")

    def get_list_of_designs(self) -> List[str]:
        """Get list of saved designs"""
        designs_dir = "assets/designs"
        if os.path.exists(designs_dir):
            return [f[:-5] for f in os.listdir(designs_dir) if f.endswith('.json')]
        return []
