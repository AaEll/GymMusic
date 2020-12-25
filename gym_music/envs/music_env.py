import gym
from gym import error, spaces, utils
from gym.utils import seeding

from ..utils.builders import MidiBuilder
from ..utils.players import MidiPlayer


class MusicEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self, max_rounds = 10):
    super(MusicEnv,self).__init__()
    self.action_space = spaces.MultiDiscrete([2]*10)
    self.observation_space = spaces.Discrete(2)
    
    # define Midi utility objects
    self.builder = MidiBuilder()
    self.player = MidiPlayer()

    # stop condition number of rounds
    self._proto_rounds = 0
    self.max_proto_rounds = max_rounds


  def step(self, action):

    self._proto_rounds = self._proto_rounds + 1

    if self._is_stop_action(action):
      self.builder.append(action)
      midi_file_path = self.builder.build()
      self.player.queue(midi_file_path)

      #reward = self.player.wait(song_id)
      reward = 1
      obs = 1
      done = 1

    else:
      self.builder.append(action)
      reward = 0
      obs = 0
      done = 0

    return obs,reward,done, {}

  def reset(self):
    self.builder.reset()
    self.player.reset()
    return None
  
  def render(self, mode='human',):
    pass

  def close(self):
    self.builder.close()
    self.player.close()
    pass

  def _is_stop_action(self,action):
    return self._proto_rounds >= self.max_proto_rounds
    

