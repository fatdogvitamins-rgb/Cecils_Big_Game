"""
AI Engine - Advanced enemy AI system
Implements rule-based logic, machine learning, and behavior trees
"""

import math
import random
from typing import Dict, List, Tuple, Optional
from enum import Enum
from numpy import array as np_array
import numpy as np


class AIType(Enum):
    """Types of AI behavior"""
    RULE_BASED = "rule_based"
    MACHINE_LEARNING = "machine_learning"
    BEHAVIOR_TREE = "behavior_tree"
    SCRIPTED = "scripted"


class RuleBasedAI:
    """Rule-based AI using simple if-then logic"""

    def __init__(self, enemy):
        """
        Initialize rule-based AI

        Args:
            enemy: Enemy object to control
        """
        self.enemy = enemy
        self.rules = []
        self.priorities = {}

    def add_rule(self, condition_func, action_func, priority: int = 5):
        """
        Add a rule to the AI

        Args:
            condition_func: Function that returns True/False
            action_func: Function to execute if condition is True
            priority: Higher priority rules execute first (0-10)
        """
        rule_id = len(self.rules)
        self.rules.append({
            'id': rule_id,
            'condition': condition_func,
            'action': action_func,
            'priority': priority
        })
        self.priorities[rule_id] = priority

    def add_default_patrol_ai(self):
        """Create default patrol AI"""
        # Rule 1: If player visible, chase
        self.add_rule(
            lambda: self.enemy.can_see_player(range=200),
            lambda: self.enemy.chase_mode(),
            priority=10
        )

        # Rule 2: If not seeing player, patrol
        self.add_rule(
            lambda: not self.enemy.can_see_player(range=200),
            lambda: self.enemy.patrol(),
            priority=5
        )

    def update(self, player, level) -> bool:
        """
        Update AI and return if action was taken

        Args:
            player: Player object
            level: Level object

        Returns:
            True if any action was executed
        """
        # Sort rules by priority
        sorted_rules = sorted(self.rules, key=lambda r: r['priority'], reverse=True)

        # Execute first rule that matches
        for rule in sorted_rules:
            try:
                if rule['condition']():
                    rule['action']()
                    return True
            except Exception as e:
                print(f"Rule error: {e}")
                continue

        return False


class BehaviorTree:
    """Behavior tree implementation for complex AI"""

    class NodeType(Enum):
        SEQUENCE = "sequence"      # All children must succeed
        SELECTOR = "selector"      # First successful child wins
        ACTION = "action"           # Performs an action
        CONDITION = "condition"     # Checks a condition

    def __init__(self, enemy):
        """
        Initialize behavior tree

        Args:
            enemy: Enemy object to control
        """
        self.enemy = enemy
        self.root = None

    def create_patrol_and_chase_tree(self):
        """Create a simple patrol -> chase behavior tree"""
        # Root is a selector (try approaches in order)
        self.root = {
            'type': self.NodeType.SELECTOR,
            'children': [
                # Try chase first if player visible
                {
                    'type': self.NodeType.SEQUENCE,
                    'children': [
                        {
                            'type': self.NodeType.CONDITION,
                            'condition': lambda: self.enemy.can_see_player(range=200)
                        },
                        {
                            'type': self.NodeType.ACTION,
                            'action': lambda: self.enemy.chase_mode()
                        }
                    ]
                },
                # Otherwise patrol
                {
                    'type': self.NodeType.ACTION,
                    'action': lambda: self.enemy.patrol()
                }
            ]
        }

    def execute(self):
        """Execute the behavior tree"""
        if self.root:
            return self._execute_node(self.root)
        return False

    def _execute_node(self, node):
        """Execute a single tree node"""
        try:
            if node['type'] == self.NodeType.SEQUENCE:
                # All children must succeed
                for child in node.get('children', []):
                    if not self._execute_node(child):
                        return False
                return True

            elif node['type'] == self.NodeType.SELECTOR:
                # First successful child wins
                for child in node.get('children', []):
                    if self._execute_node(child):
                        return True
                return False

            elif node['type'] == self.NodeType.CONDITION:
                return node.get('condition', lambda: False)()

            elif node['type'] == self.NodeType.ACTION:
                node.get('action', lambda: None)()
                return True

        except Exception as e:
            print(f"Tree execution error: {e}")
            return False

        return False


class SimpleNeuralNet:
    """Simple neural network for ML-based AI"""

    def __init__(self, input_size: int, hidden_size: int = 8, output_size: int = 4):
        """
        Initialize simple neural network

        Args:
            input_size: Number of input features
            hidden_size: Number of hidden neurons
            output_size: Number of output actions
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Initialize weights randomly
        self.w1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.w2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))

        self.learning_rate = 0.01

    def forward(self, x):
        """Forward pass through network"""
        self.z1 = np.dot(x, self.w1) + self.b1
        self.a1 = np.tanh(self.z1)  # Tanh activation
        self.z2 = np.dot(self.a1, self.w2) + self.b2
        self.a2 = 1 / (1 + np.exp(-self.z2))  # Sigmoid activation
        return self.a2

    def backward(self, x, y, output):
        """Simple backpropagation"""
        m = x.shape[0]

        # Output layer error
        dz2 = output * (1 - output)
        dw2 = np.dot(self.a1.T, dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m

        # Hidden layer error
        da1 = np.dot(dz2, self.w2.T)
        dz1 = da1 * (1 - self.a1 * self.a1)
        dw1 = np.dot(x.T, dz1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m

        # Update weights
        self.w1 -= self.learning_rate * dw1
        self.b1 -= self.learning_rate * db1
        self.w2 -= self.learning_rate * dw2
        self.b2 -= self.learning_rate * db2

    def predict(self, x):
        """Get prediction"""
        return np.argmax(self.forward(x), axis=1)


class MachineLearningAI:
    """Machine learning based AI that learns from experience"""

    def __init__(self, enemy):
        """
        Initialize ML AI

        Args:
            enemy: Enemy object to control
        """
        self.enemy = enemy
        self.net = SimpleNeuralNet(input_size=6, hidden_size=8, output_size=4)
        # Actions: 0=patrol, 1=chase, 2=jump, 3=attack
        self.experience_buffer = []
        self.training_sessions = 0

    def get_state(self, player, level) -> np_array:
        """
        Get current game state as features

        Args:
            player: Player object
            level: Level object

        Returns:
            Feature vector
        """
        # Features: player_distance, player_visible, health, on_ground, player_above, player_below
        features = [
            min(abs(self.enemy.x - player.x), 500) / 500,  # Normalized distance
            float(self.enemy.can_see_player(range=200)),   # Visibility
            self.enemy.health / 3.0,                        # Normalized health
            float(self.enemy.on_ground) if hasattr(self.enemy, 'on_ground') else 0.5,  # On ground
            float(player.y < self.enemy.y),                 # Player above
            float(player.y > self.enemy.y),                 # Player below
        ]
        return np_array([features])

    def choose_action(self, player, level):
        """
        Choose action based on current state

        Args:
            player: Player object
            level: Level object

        Returns:
            Action index
        """
        state = self.get_state(player, level)
        action = self.net.predict(state)[0]
        return action

    def execute_action(self, action):
        """Execute chosen action"""
        if action == 0:
            self.enemy.patrol()
        elif action == 1:
            self.enemy.chase_mode()
        elif action == 2:
            self.enemy.jump() if hasattr(self.enemy, 'jump') else None
        elif action == 3:
            self.enemy.attack() if hasattr(self.enemy, 'attack') else None

    def remember_experience(self, state, action, reward, next_state, done):
        """Store experience in buffer"""
        self.experience_buffer.append({
            'state': state,
            'action': action,
            'reward': reward,
            'next_state': next_state,
            'done': done
        })

        # Train if buffer is full enough
        if len(self.experience_buffer) >= 10:
            self.train()
            self.experience_buffer.clear()

    def train(self):
        """Train on accumulated experience"""
        if not self.experience_buffer:
            return

        batch_size = len(self.experience_buffer)
        states = np_array([exp['state'].flatten() for exp in self.experience_buffer])
        actions = np_array([[exp['action']] for exp in self.experience_buffer])
        rewards = np_array([[exp['reward']] for exp in self.experience_buffer])

        # Forward pass
        output = self.net.forward(states)

        # Create target output with rewards
        target = output.copy()
        for i in range(batch_size):
            target[i, int(actions[i, 0])] = rewards[i, 0]

        # Backward pass
        self.net.backward(states, target, output)
        self.training_sessions += 1

    def update(self, player, level) -> bool:
        """Update AI"""
        action = self.choose_action(player, level)
        self.execute_action(action)

        # Calculate reward signal
        distance_to_player = abs(self.enemy.x - player.x)
        reward = 1.0 if distance_to_player < 100 else -0.1  # Reward for being close to player

        next_state = self.get_state(player, level)
        self.remember_experience(self.get_state(player, level), action, reward, next_state, False)

        return True


class AIEngine:
    """Master AI engine that manages different AI types"""

    def __init__(self, enemy, ai_type: AIType = AIType.RULE_BASED):
        """
        Initialize AI engine

        Args:
            enemy: Enemy object to control
            ai_type: Type of AI to use
        """
        self.enemy = enemy
        self.ai_type = ai_type
        self.rule_based_ai = RuleBasedAI(enemy)
        self.behavior_tree = BehaviorTree(enemy)
        self.ml_ai = MachineLearningAI(enemy)

        # Set up default behaviors
        self.rule_based_ai.add_default_patrol_ai()
        self.behavior_tree.create_patrol_and_chase_tree()

    def set_ai_type(self, ai_type: AIType):
        """Switch AI type"""
        self.ai_type = ai_type

    def update(self, player, level) -> bool:
        """
        Update AI and execute behavior

        Args:
            player: Player object
            level: Level object

        Returns:
            True if action was taken
        """
        if self.ai_type == AIType.RULE_BASED:
            return self.rule_based_ai.update(player, level)

        elif self.ai_type == AIType.BEHAVIOR_TREE:
            return self.behavior_tree.execute()

        elif self.ai_type == AIType.MACHINE_LEARNING:
            return self.ml_ai.update(player, level)

        elif self.ai_type == AIType.SCRIPTED:
            # Default patrolling
            return self.rule_based_ai.update(player, level)

        return False

    def get_ai_info(self) -> str:
        """Get current AI type info"""
        info = {
            'type': self.ai_type.value,
            'rule_based': f"Rules: {len(self.rule_based_ai.rules)}",
            'ml_training': f"Sessions: {self.ml_ai.training_sessions}",
            'ml_buffer': f"Experiences: {len(self.ml_ai.experience_buffer)}"
        }
        return info
