"""
Audio Manager - Handle game sounds and music
Generates procedural sounds for game events
"""

import pygame
import numpy as np
from typing import Optional


class AudioManager:
    """Manages all game audio - sounds and music"""

    def __init__(self):
        """Initialize audio manager"""
        pygame.mixer.init()
        self.master_volume = 0.7
        self.sfx_volume = 0.6
        self.music_volume = 0.5
        self.current_music = None
        self.sounds = {}

        # Pregenerate common sounds
        self._generate_sounds()

    def _generate_sounds(self):
        """Pre-generate all sound effects"""
        # Jump sound - ascending pitch
        self.sounds['jump'] = self._generate_jump_sound()

        # Land sound - descending pitch
        self.sounds['land'] = self._generate_land_sound()

        # Coin/collectible - ascending ping
        self.sounds['collect'] = self._generate_collect_sound()

        # Enemy defeated - dropping pitch
        self.sounds['enemy_defeat'] = self._generate_enemy_defeat_sound()

        # Level complete - success chord
        self.sounds['level_complete'] = self._generate_level_complete_sound()

        # Game over - descending failure sound
        self.sounds['game_over'] = self._generate_game_over_sound()

        # Menu select - click sound
        self.sounds['menu_select'] = self._generate_menu_select_sound()

    def _generate_jump_sound(self) -> pygame.mixer.Sound:
        """Generate jump sound effect"""
        sample_rate = 22050
        duration = 0.15
        samples = int(sample_rate * duration)

        # Ascending frequency sweep
        frequencies = np.linspace(400, 800, samples)
        t = np.linspace(0, duration, samples)

        # Envelope - quick attack, decay
        envelope = np.exp(-t * 8)

        wave = np.sin(2 * np.pi * frequencies * t) * envelope
        wave = np.int16(wave * 32767 * 0.3)

        sound = pygame.mixer.Sound(wave)
        sound.set_volume(self.sfx_volume * self.master_volume)
        return sound

    def _generate_land_sound(self) -> pygame.mixer.Sound:
        """Generate land/thud sound effect"""
        sample_rate = 22050
        duration = 0.1
        samples = int(sample_rate * duration)

        # Descending frequency
        frequencies = np.linspace(300, 100, samples)
        t = np.linspace(0, duration, samples)

        # Sharp envelope
        envelope = np.exp(-t * 20)

        wave = np.sin(2 * np.pi * frequencies * t) * envelope
        wave = np.int16(wave * 32767 * 0.4)

        sound = pygame.mixer.Sound(wave)
        sound.set_volume(self.sfx_volume * self.master_volume)
        return sound

    def _generate_collect_sound(self) -> pygame.mixer.Sound:
        """Generate collectible/coin sound"""
        sample_rate = 22050
        duration = 0.2
        samples = int(sample_rate * duration)

        # Rising tones
        t = np.linspace(0, duration, samples)

        # Two quick tones
        wave1 = np.sin(2 * np.pi * 800 * t[:samples // 2])
        wave2 = np.sin(2 * np.pi * 1200 * t[samples // 2:])

        envelope = np.exp(-t * 15)

        wave = np.concatenate([wave1, wave2]) * envelope
        wave = np.int16(wave * 32767 * 0.3)

        sound = pygame.mixer.Sound(wave)
        sound.set_volume(self.sfx_volume * self.master_volume)
        return sound

    def _generate_enemy_defeat_sound(self) -> pygame.mixer.Sound:
        """Generate enemy defeat sound"""
        sample_rate = 22050
        duration = 0.3
        samples = int(sample_rate * duration)

        # Descending pitch with noise
        t = np.linspace(0, duration, samples)
        frequencies = np.linspace(500, 100, samples)

        # Add some noise
        noise = np.random.randn(samples) * 0.3
        wave = np.sin(2 * np.pi * frequencies * t) + noise

        # Envelope - fade out
        envelope = np.exp(-t * 6)
        wave = wave * envelope

        wave = np.int16(wave * 32767 * 0.3)

        sound = pygame.mixer.Sound(wave)
        sound.set_volume(self.sfx_volume * self.master_volume)
        return sound

    def _generate_level_complete_sound(self) -> pygame.mixer.Sound:
        """Generate level complete - success fanfare"""
        sample_rate = 22050
        duration = 0.5
        samples = int(sample_rate * duration)

        t = np.linspace(0, duration, samples)

        # Chord - C major (frequencies for C, E, G)
        freqs = [262, 330, 392]  # C, E, G
        wave = np.zeros(samples)

        for freq in freqs:
            wave += np.sin(2 * np.pi * freq * t)

        # Envelope - attack and sustain
        envelope = np.ones(samples)
        envelope[:int(samples * 0.1)] = np.linspace(0, 1, int(samples * 0.1))
        envelope[int(samples * 0.8):] = np.linspace(1, 0, int(samples * 0.2))

        wave = wave * envelope / len(freqs)
        wave = np.int16(wave * 32767 * 0.3)

        sound = pygame.mixer.Sound(wave)
        sound.set_volume(self.sfx_volume * self.master_volume)
        return sound

    def _generate_game_over_sound(self) -> pygame.mixer.Sound:
        """Generate game over - sad trombone effect"""
        sample_rate = 22050
        duration = 0.8
        samples = int(sample_rate * duration)

        t = np.linspace(0, duration, samples)

        # Descending glissando
        frequencies = np.linspace(400, 80, samples)
        wave = np.sin(2 * np.pi * frequencies * t)

        # Envelope - slow fade
        envelope = np.exp(-t * 3)
        wave = wave * envelope

        wave = np.int16(wave * 32767 * 0.4)

        sound = pygame.mixer.Sound(wave)
        sound.set_volume(self.sfx_volume * self.master_volume)
        return sound

    def _generate_menu_select_sound(self) -> pygame.mixer.Sound:
        """Generate menu selection click"""
        sample_rate = 22050
        duration = 0.08
        samples = int(sample_rate * duration)

        t = np.linspace(0, duration, samples)

        # Simple beep
        wave = np.sin(2 * np.pi * 600 * t)

        # Sharp envelope
        envelope = np.exp(-t * 30)
        wave = wave * envelope

        wave = np.int16(wave * 32767 * 0.4)

        sound = pygame.mixer.Sound(wave)
        sound.set_volume(self.sfx_volume * self.master_volume)
        return sound

    def play_sound(self, sound_name: str):
        """
        Play a sound effect by name

        Args:
            sound_name: Name of the sound to play
        """
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def play_jump(self):
        """Play jump sound"""
        self.play_sound('jump')

    def play_land(self):
        """Play land sound"""
        self.play_sound('land')

    def play_collect(self):
        """Play collectible sound"""
        self.play_sound('collect')

    def play_enemy_defeat(self):
        """Play enemy defeated sound"""
        self.play_sound('enemy_defeat')

    def play_level_complete(self):
        """Play level complete sound"""
        self.play_sound('level_complete')

    def play_game_over(self):
        """Play game over sound"""
        self.play_sound('game_over')

    def play_menu_select(self):
        """Play menu selection sound"""
        self.play_sound('menu_select')

    def set_master_volume(self, volume: float):
        """
        Set master volume (0.0-1.0)

        Args:
            volume: Volume level
        """
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_sfx_volume(self, volume: float):
        """Set sound effect volume"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def set_music_volume(self, volume: float):
        """Set music volume"""
        self.music_volume = max(0.0, min(1.0, volume))
        self._update_volumes()

    def _update_volumes(self):
        """Update all sound volumes"""
        for sound in self.sounds.values():
            if isinstance(sound, pygame.mixer.Sound):
                sound.set_volume(self.sfx_volume * self.master_volume)

    def play_music(self, music_file: Optional[str] = None, loops: int = -1):
        """
        Play background music

        Args:
            music_file: Path to music file (or None to stop)
            loops: Number of loops (-1 for infinite)
        """
        try:
            if music_file is None:
                pygame.mixer.music.stop()
                self.current_music = None
            else:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
                pygame.mixer.music.play(loops)
                self.current_music = music_file
        except pygame.error as e:
            print(f"Could not load music file {music_file}: {e}")

    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        self.current_music = None

    def fade_out_music(self, duration_ms: int = 1000):
        """Fade out music over specified duration"""
        pygame.mixer.music.fadeout(duration_ms)
