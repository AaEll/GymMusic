from .vlc_player import VLC_Player
from .midi_builder import MidiBuilder

class MIDI_Player(VLC_Player):

  def __init__(self):
    super(MIDI_Player, self).__init__()
    self.instance = vlc.Instance
    self.midi_builder = MidiBuilder()




