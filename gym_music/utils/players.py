import subprocess
import os
class Player():

  def __init__(self):
    pass

  def queue(self,content_path):
    pass

  def close(self):
    pass

  def reset(self):
    pass

class MidiPlayer(Player):
  
  def __init__(self):
    super(MidiPlayer, self).__init__()
    self._p = None
    self.soundfont_path = '/usr/share/sounds/sf2/FluidR3_GM.sf2'

    self.env = os.environ.copy()
    self.env["PATH"] = '/usr/local/bin:'+self.env["PATH"]

  def queue(self,content_path):
    if self.is_running():
      self._p.wait(30) # give the current audio 30s to complete
    
    self._p = subprocess.Popen(["fluidsynth",'-i','-a','pulseaudio',self.soundfont_path,content_path],env = self.env)
    
    

  def reset(self):
    pass
  def close(self):
    pass
  
  def is_running(self):
    if self._p is None:
      return False
    else:
      return self._p.poll() is None
