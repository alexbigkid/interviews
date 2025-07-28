import unittest
from io import StringIO
import sys
from src.design_patterns.adapter import AudioPlayer, MediaAdapter, VlcPlayer, Mp4Player


class TestAdapter(unittest.TestCase):
    
    def setUp(self):
        self.player = AudioPlayer()
    
    def test_mp3_playback(self):
        """Test native MP3 playback without adapter"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.player.play("mp3", "song.mp3")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Playing mp3 file: song.mp3", output)
    
    def test_vlc_playback_through_adapter(self):
        """Test VLC playback through adapter"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.player.play("vlc", "movie.vlc")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Playing vlc file: movie.vlc", output)
    
    def test_mp4_playback_through_adapter(self):
        """Test MP4 playback through adapter"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.player.play("mp4", "video.mp4")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Playing mp4 file: video.mp4", output)
    
    def test_unsupported_format(self):
        """Test unsupported format handling"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.player.play("avi", "movie.avi")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Invalid media. avi format not supported", output)
    
    def test_media_adapter_vlc(self):
        """Test MediaAdapter with VLC player directly"""
        adapter = MediaAdapter("vlc")
        self.assertIsInstance(adapter.advanced_player, VlcPlayer)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        adapter.play("vlc", "test.vlc")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Playing vlc file: test.vlc", output)
    
    def test_media_adapter_mp4(self):
        """Test MediaAdapter with MP4 player directly"""
        adapter = MediaAdapter("mp4")
        self.assertIsInstance(adapter.advanced_player, Mp4Player)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        adapter.play("mp4", "test.mp4")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Playing mp4 file: test.mp4", output)
    
    def test_vlc_player_direct(self):
        """Test VlcPlayer directly"""
        vlc_player = VlcPlayer()
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        vlc_player.play_vlc("direct.vlc")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Playing vlc file: direct.vlc", output)
    
    def test_mp4_player_direct(self):
        """Test Mp4Player directly"""
        mp4_player = Mp4Player()
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        mp4_player.play_mp4("direct.mp4")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Playing mp4 file: direct.mp4", output)


if __name__ == '__main__':
    unittest.main()