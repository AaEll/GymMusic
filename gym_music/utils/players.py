import subprocess
from .monitor import Monitor

class Player():
  def __init__(self):
    pass

  def queue(self,content_path):
    pass
    return 0

  def close(self):
    pass

  def reset(self):
    pass

class MidiPlayer(Player):
  def __init__(self, monitor = None):
    super().__init__()
    self.soundfont = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
    self.samplerate = '44100'
    
    # initialize monitor
    self.monitor = Monitor() if monitor is None else monitor

    # initialize player_process to None
    self._p = None

  def _play_midi(self,content_path):
    self._p = subprocess.call(['fluidsynth', '-i','-a','pulseaudio', self.soundfont, content_path,'-r',self.samplerate],shell=False)

  def queue(self,content_path):
    self._play_midi(content_path)
    
    observation = self.monitor.record()

    return observation

  def reset(self):
    self._close_p()
    self.monitor.reset()

  def close(self):
    self._close_p()
    self.monitor.close()

  def _close_p(self):
    if self._p is not None:
      self._p.terminate()


  def isRunning(self):
    if self._p is None:
      return False
    else:
      return self._p.poll() is None


