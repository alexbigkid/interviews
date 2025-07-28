"""
Adapter Pattern - Allows incompatible interfaces to work together
Common interview question: Third-party library integration, Legacy system integration
"""

from abc import ABC, abstractmethod


class MediaPlayer(ABC):
    @abstractmethod
    def play(self, audio_type: str, filename: str):
        pass


class AdvancedMediaPlayer(ABC):
    @abstractmethod
    def play_vlc(self, filename: str):
        pass
    
    @abstractmethod
    def play_mp4(self, filename: str):
        pass


class VlcPlayer(AdvancedMediaPlayer):
    def play_vlc(self, filename: str):
        print(f"Playing vlc file: {filename}")
    
    def play_mp4(self, filename: str):
        pass


class Mp4Player(AdvancedMediaPlayer):
    def play_vlc(self, filename: str):
        pass
    
    def play_mp4(self, filename: str):
        print(f"Playing mp4 file: {filename}")


class MediaAdapter(MediaPlayer):
    def __init__(self, audio_type: str):
        if audio_type == "vlc":
            self.advanced_player = VlcPlayer()
        elif audio_type == "mp4":
            self.advanced_player = Mp4Player()
    
    def play(self, audio_type: str, filename: str):
        if audio_type == "vlc":
            self.advanced_player.play_vlc(filename)
        elif audio_type == "mp4":
            self.advanced_player.play_mp4(filename)


class AudioPlayer(MediaPlayer):
    def play(self, audio_type: str, filename: str):
        if audio_type == "mp3":
            print(f"Playing mp3 file: {filename}")
        elif audio_type in ["vlc", "mp4"]:
            adapter = MediaAdapter(audio_type)
            adapter.play(audio_type, filename)
        else:
            print(f"Invalid media. {audio_type} format not supported")


# Usage example
if __name__ == "__main__":
    player = AudioPlayer()
    
    player.play("mp3", "song.mp3")
    player.play("mp4", "video.mp4")
    player.play("vlc", "movie.vlc")
    player.play("avi", "film.avi")  # Not supported