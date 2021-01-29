
class Monitor():
  def __init__(self):
    pass

  def record(self):
    return 0

  def reset(self):
    pass
 
  def close(self):
    pass



class HeartMonitor(Monitor):
  def __init__(self):
    super().__init__()

    self._p = None

    # initialize HR monitor 

  def record(self):
    # Spawn Heartrate monitor process for the next K seconds
    self._p = TODO

    # Read the process value

    future = self._p.TODO

    return future

  def reset(self):
    self._close_p()

  def close(self):
    self._close_p()

  def _close_p(self):
    if self._p is not None:
      self._p.terminate()







