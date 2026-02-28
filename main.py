#!/usr/bin/env python3
"""
Cecil's Big Game - Platform Game with Tinkercad Integration and Block Editor
Main entry point
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.game import Game


def main():
    """Main entry point"""
    print("Starting Cecil's Big Game...")
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
