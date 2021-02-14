import pexpect
import sys
import time

class Monitor():
  def __init__(self):
    pass
  def read(self):
    return 0

  def connect(self):
    pass
  
  def reset(self):
    pass
 
  def close(self):
    pass

  @property
  def connected(self):
    return True




class HeartMonitor(Monitor):
  def __init__(self, macAddress):
    super().__init__()

    self.macAddress = macAddress

    # initialize HR monitor 
    self.gat_p = None
    self._handle = None
    self._uuid = None
    self._connected = False


  def read(self):
    try:
      expect_message = 'Notification handle = '+self._handle+' value: ([0-9a-f ]+)'
      self.gat_p.expect(expect_message, timeout = 10)

      message = self.gat_p.match.group(1).strip()
      message = [int(byte,16) for byte in message.split(b' ')]
      if len(message) < 2:
        raise ValueError('Received malformed heartrate message')
      hr, status = self.getHeartRate(message)
      return hr

    except (pexpect.TIMEOUT, ValueError ) as e:
      self._close_p()
      raise ValueError('Lost connection to HR Monitor')

    except KeyboardInterrupt:
      self.gat_p.close()
      raise KeyboardInterrupt()

  def reset(self):
    pass
    #self._close_p()

  def close(self):
    self._close_p()

  def _close_p(self):
    if self.gat_p: 
      self.gat_p.close()
      self.gat_p = None
    self._connected = False
 
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
        raise KeyboardInterrupt()
    self._connected = True
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
        raise KeyboardInterrupt()
      
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
  
  @property
  def connected(self):
    return self._connected

  def __getstate__(self):
    state = self.__dict__.copy()
    state['gat_p'] = None
    state['_connected']= False

    return state

  """
  def __deepcopy__(self, memo):
    gat_p = self.gat_p
    self.gat_p = None

    deepcopy_method = self.__deepcopy__
    self.__deepcopy__ = None # this line needed for deepcopy to have normal behavior
    cp = deepcopy(self, memo)
    # undo self.__deepcopy__ = None
    self.__deepcopy__ = deepcopy_method
    cp.__deepcopy__ = deepcopy_method

    self.gat_p = gat_p
    cp._connected = False
    return cp
"""
