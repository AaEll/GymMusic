import vlc
from .player_base import Player
class VLC_Player(Player):

  def __init__(self):
    super(VLC_Player, self).__init__()
    self.instance = vlc.Instance
    
  
  def run(self):
    pass

  def play(self, content_path):
    pass

  def close(self):
    pass
  


