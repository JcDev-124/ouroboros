import pygame

class AudioManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Initialize only once
            pygame.mixer.init()
            self._background_music = None
            self._sound_effects = {}
            self.initialized = True

    def play_background_music(self, audio_directory, loops=-1):
        if self._background_music != audio_directory:
            pygame.mixer.music.load(audio_directory)
            pygame.mixer.music.play(loops=loops)
            self._background_music = audio_directory

    def stop_background_music(self):
        pygame.mixer.music.stop()

    def load_sound_effect(self, name, audio_directory):
        self._sound_effects[name] = pygame.mixer.Sound(audio_directory)

    def play_sound_effect(self, name):
        if name in self._sound_effects:
            self._sound_effects[name].play()

    def stop_sound_effect(self, name):
        if name in self._sound_effects:
            self._sound_effects[name].stop()
