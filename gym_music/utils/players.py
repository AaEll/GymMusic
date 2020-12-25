import pygame

class Player():

  def __init__(self):
    pass

  def queue(self,content_path):
    pass

  def close(self):
    pass
  


class MIDI_Player(Player):

  def __init__(self):
    super(MIDI_Player, self).__init__()
    pygame.mixer.init()

  def queue(self,content_path):

    if pygame.mixer.music.get_busy(): # if currently playing music
      pygame.mixer.music.queue(content_path)
    else:
      pygame.mixer.music.load(content_path)
      pygame.mixer.music.play()


  def close(self):
    pygame.mixer.quit()





