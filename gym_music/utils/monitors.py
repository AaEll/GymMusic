import pexpect
import sys

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
  def __init__(self, macAddress):
    super().__init__()

    self._p = None

    self.macAddress = macAddress
    self._handle = None
    self._uuid = None


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
 
  def getHeartRate(message):

    hrFormatID = message[0] & 1
    sensorStatusID = message[0] & 6 

    if hrFormatID == 0:
        hr = message[1]
    elif hrFormatID == 1:
        hr = (message[2] << 8) | message[1]

    return hr, sensorStatusID

  def connect():

    connected = False
    self.gat_p = pexpect.spawn('gattool -b ' + self.macAddress+ ' -t random --interactive') as gat_p
    self.gat_p.logfile = sys.stdout

    while not connected:
      self.gat_p.expect(r'\[LE\}>')
      self.gat_p.sendline('connect')

      try:
        status = self.gat_p.expect(['Connection successful.',r'\[CON\]'],timeout = 10)
        if not status:
          self.gat_p.expect(r'\[LE\]>', timeout = 10)
        connected = True
      except pexpect.TIMEOUT:
        print('connection failed : retrying')
      except KeyboardInterrupt:
        self.gat_p.close()
        quit()
    print('connection successful, registering') 
    
    self.gat_p.sendline('char-desc')
    registered = False
    while not registered:
      try:
        self.gat_p.expect( r'handle: (0x[0-9a-f]+), uuid: ([0-9a-f]{8})', timeout= 10)
      except pexcpect.TIMEOUT:
          print('registration failed : retrying')
      except KeyboardInterrupt:
        self.gat_P.close()
        quit()
      self._handle = self.gat_p.match.group(1).decode()
      self._uuid = self.gat_p.match.group(2).decode()
    print('registration successful')


  def read_hr():
    pass 


