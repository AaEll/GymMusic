import subprocess
from .monitors import Monitor
import time
from copy import deepcopy
import logging

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
  def __init__(self, monitor = None, steps = 30):
    super().__init__()
    self.soundfont = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
    self.samplerate = '44100'
    self.steps = steps
    # initialize monitor
    self.monitor = Monitor() if monitor is None else monitor

    # initialize player_process to None
    self._p = None


  def queue(self,content_path):
    while not self.monitor.connected:
      try:
        self.monitor.connect()
      except ValueError as e:
        print('caught error while connecting retrying')


    self._p = subprocess.Popen(['fluidsynth', '-i','-a','pulseaudio', self.soundfont, content_path,'-r',self.samplerate])
    total = 0
    for i in range(self.steps):
      try:
        obs = self.monitor.read()
      except ValueError as e:
        logging.warning('monitor connection lost: retrying')
        self._close_p()
        return self.queue(content_path)
      total = total + obs
      time.sleep(1)
    feedback = -total/self.steps

    if self.isRunning():
      self._p.wait()
    
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
    self._p = None

  def isRunning(self):
    return (False if self._p is None else (self._p.poll is None))
  
  def __getstate__(self):
    state = self.__dict__.copy()
    state['_p'] = None
    return state
  """
  def __deepcopy__(self, memo):
    # remove unwanted child temporarily
    _p = self._p
    self._p = None
    
    deepcopy_method = self.__deepcopy__

    self.__deepcopy__ = None # this line needed for deepcopy to have normal behavior
    cp = deepcopy(self, memo)

    # undo self.__deepcopy__ = None
    self.__deepcopy__ = deepcopy_method
    cp.__deepcopy__ = deepcopy_method
    
    # return unwanted child
    self._p = _p

    return cp

  """
