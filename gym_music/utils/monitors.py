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
    self.gat_p = None
    self._handle = None
    self._uuid = None
    #self.connect()
    #print(self.read())

    self.rounds = 30

  def record(self):
    # Spawn Heartrate monitor process for the next K seconds
    self.connect()
    total = 0
    for i in range(self.rounds):
      try:
        total = total + self.read()
        print('current hr : {}'.format(total/(i+1)))
      except pexpect.TIMEOUT:
        return total/(i+1) # IF timeout, just return current estimate

      time.sleep(1)

    return total/self.rounds

  def reset(self):
    self._close_p()

  def close(self):
    self._close_p()

  def _close_p(self):
    if self.gat_p is not None:
      self.gat_p.terminate()
 
  def getHeartRate(self,message):
    
    hrFormatID = message[0] & 1
    sensorStatusID = message[0] & 6 

    if hrFormatID == 0:
      hr = message[1]
    elif hrFormatID == 1:
      hr = (message[2] << 8) | message[1]

    return hr, sensorStatusID

  def connect(self):

    connected = False
    self.gat_p = pexpect.spawn('gatttool -b ' + self.macAddress+ ' -t random --interactive') 

    while not connected:

      self.gat_p.expect(r"\[LE\]>")
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
    print('connection successful, registering monitor handles') 
    self.register()

  def register(self):
    self.gat_p.sendline('char-desc')
    registered = False
    charWriteSet = False
    while not (registered and charWriteSet):
      try:
        self.gat_p.expect( r'handle: (0x[0-9a-f]+), uuid: ([0-9a-f]{8})', timeout= 10)
      except pexpect.TIMEOUT:
          print('registration failed : retrying')
      except KeyboardInterrupt:
        self.gat_p.close()
        quit()
      
      handle = self.gat_p.match.group(1).decode()
      uuid = self.gat_p.match.group(2).decode()
      
      if uuid == '00002902' and registered:
        self.charWriteHandle = handle
        charWriteSet = True
      
      if uuid == '00002a37':
        self._handle = handle
        registered = True
    self.gat_p.sendline('char-write-req '+self.charWriteHandle+' 0100')
        
    print('handle registration successful')
  
  def read(self):
    try:
      expect_message = 'Notification handle = '+self._handle+' value: ([0-9a-f ]+)'
      #expect_message = '(.*)'
      self.gat_p.expect(expect_message, timeout = 10)
      #print(self.gat_p.match.group(1))
      
      message = self.gat_p.match.group(1).strip()
      message = [int(byte,16) for byte in message.split(b' ')]
      hr, status = self.getHeartRate(message)
      return hr

    except pexpect.TIMEOUT:
      print('connection lost to HR monitor, restarting connection')
      self.gat_p.close()
      self.connect()
      raise pexpect.TIMEOUT

    except KeyboardInterrupt:
      self.gat_p.close()
      quit()


