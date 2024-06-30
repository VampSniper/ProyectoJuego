import pygame

# Inicializa el mezclador de música
pygame.mixer.init(frequency=44100)

class MusicManager:
    def __init__(self, track_path):
        self.track_path = track_path
        self.is_playing = False
        self.volume = 0.5

    def start_music(self):
        if not self.is_playing:
            pygame.mixer.music.load(self.track_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)  # Reproducir en bucle
            self.is_playing = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)

# Instancia global de MusicManager
music_manager = MusicManager('Python/audioMP3/cancion.mp3')
