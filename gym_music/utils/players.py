import subprocesses

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
    self.soundfont = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
    self.samplerate = '44100'

  def queue(self,content_path):
    subprocess.call(['fluidsynth', '-i','-a','pulseaudio', self.soundfont, content_path,'-r',self.samplerate],shell=False)



  def reset(self):
    pass

  def close(self):
    pass




