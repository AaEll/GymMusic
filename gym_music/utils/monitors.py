import pexpect
import sys
import time

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

    self.macAddress = macAddress
    self._handle = None
    self._uuid = None

    # initialize HR monitor 
    self.connect()

    self.rounds = 30

  def record(self):
    # Spawn Heartrate monitor process for the next K seconds
    
    total = 0
    for i in range(self.rounds):
      try:
        total = total + self.read()
        print('current hr : {}'.format(total/(i+1)))
      except pexpect.TIMEOUT:
        return total/(i+1) # IF timeout, just return current estimate

      time.sleep(1)

    return total/self.rounds

      

    # Read the process value


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

  def connect(self):

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
        registered = True
      except pexcpect.TIMEOUT:
          print('registration failed : retrying')
      except KeyboardInterrupt:
        self.gat_p.close()
        quit()
      self._handle = self.gat_p.match.group(1).decode()
      self._uuid = self.gat_p.match.group(2).decode()
    print('registration successful')


  def read(self):
    try:
      self.gat_p.expect('Notification handle = ' + self._handle + 'value: ([0-9a-f]+)', timeout = 10)
      message = self.gat_p.match.group(1).strip()
      message = [int(byte,16) for byte in message.split(b' ')]
      hr, status = getHeartRate(message)
      return hr

    except pexcept.TIMEOUT:
      print('connection lost to HR monitor, restarting connection')
      self.gat_p.close()
      self.connect()
      raise pexcept.TIMEOUT

    except KeyboardInterrupt:
      self.gat_p.close()
      quit()



