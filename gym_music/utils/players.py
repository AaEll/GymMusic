import subprocess
from .monitors import Monitor
import time

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
    self.steps = 15
    # initialize monitor
    self.monitor = Monitor() if monitor is None else monitor

    # initialize player_process to None
    self._p = None


  def queue(self,content_path):
    0 if self.monitor.isConnected() else self.monitor.connect()

    self._p = subprocess.Popen(['fluidsynth', '-i','-a','pulseaudio', self.soundfont, content_path,'-r',self.samplerate])
    total = 0
    for i in range(self.steps):
      obs = self.monitor.read()
      total = total + obs
      time.sleep(1)
    feedback = total/self.steps

    if self.isRunning():
      self._p.wait()
    
    with open(content_path+'.feedback', 'w') as f:
      f.write('hr\n{}'.format(feedback))
    return feedback

  def reset(self):
    self._close_p()
    self.monitor.reset()

  def close(self):
    self._close_p()
    self.monitor.close()

  def _close_p(self):
    if self.isRunning():
      # TODO wrap terminate() call in try: catch (error if _p has already finished): pass
      self._p.terminate()


  def isRunning(self):
    return (False if self._p is None else (self_p.poll is None))


