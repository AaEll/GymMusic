import pygame

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
    pygame.mixer.init()

  def queue(self,content_path):

    if pygame.mixer.music.get_busy(): # if currently playing music
      pygame.mixer.music.queue(content_path)
    else:
      pygame.mixer.music.load(content_path)
      pygame.mixer.music.play()

  def reset(self):
    pygame.mixer.quit()
    pygame.mixer.init()

  def close(self):
    pygame.mixer.quit()





