import pygame

# Initialize the music mixer
pygame.mixer.init(frequency=44100)

class MusicManager:
    def __init__(self, track_path):
        """
        Initializes a MusicManager instance.

        Args:
        - track_path (str): Path to the music track file.
        """
        self.track_path = track_path
        self.is_playing = False
        self.volume = 0.5

    def start_music(self):
        """
        Starts playing the music track.

        If music is not already playing, loads the track, sets the volume,
        and plays it in a loop.
        """
        if not self.is_playing:
            pygame.mixer.music.load(self.track_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)  # Play in a loop
            self.is_playing = True

    def stop_music(self):
        """
        Stops the currently playing music track.
        """
        pygame.mixer.music.stop()
        self.is_playing = False

    def set_volume(self, volume):
        """
        Sets the volume of the music.

        Args:
        - volume (float): Volume level (0.0 to 1.0).
        """
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)

# Global instance of MusicManager
music_manager = MusicManager('Python/audioMP3/cancion.mp3')
