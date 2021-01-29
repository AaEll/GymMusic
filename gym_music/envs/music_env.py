import gym
from gym import error, spaces, utils
from gym.utils import seeding
import asyncio

from ..utils.builders import MidiBuilder
from ..utils.players import MidiPlayer


class MusicEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self, max_rounds = 30, builder = None, player = None, monitor = None):
    super().__init__()
    self.action_space = spaces.MultiDiscrete([2]*10)
    self.observation_space = spaces.Discrete(2)
    
    # define Midi utility objects

    self.builder = MidiBuilder() if builder is None else builder
    self.player = MidiPlayer(monitor = monitor) if player is None else player

    # stop condition number of rounds
    self._proto_rounds = 0
    self.max_proto_rounds = max_rounds


  def step(self, action):

    self._proto_rounds = self._proto_rounds + 1

    if self._is_stop_action(action):
      self.builder.append(action)
      midi_file_path = self.builder.build()
      reward = self.player.queue(midi_file_path)
      reward = reward.result() if asyncio.isfuture(reward) else reward 
      obs = 1
      done = 1

    else:
      self.builder.append(action)
      reward = 0
      obs = 0
      done = 0

    return obs,reward,done, {}

  def reset(self):
    self._proto_rounds = 0
    self.builder.reset()
    self.player.reset()
    
  
  def render(self, mode='human',):
    pass

  def close(self):
    self.builder.close()
    self.player.close()
    

  def _is_stop_action(self,action):
    return self._proto_rounds >= self.max_proto_rounds
    

