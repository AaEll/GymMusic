import gym
from gym import error, spaces, utils
from gym.utils import seeding
from typing import Sequence, Callable, List, Union, Tuple, Optional, Mapping, Dict, Any
from ..music_player.midi_music_player import MidiMusicPlayer
class MusicFuturesEnv(gym.Env):
  """
  OpenAI gym Environment encapsulating an FMU model.
  """

  metadata = {'render.modes': ['human']}

  def __init__(self,
               music_player = MidiMusicPlayer(),
               stopping_criteria: Callable[[List[str]], bool],
              ):

      self.current_time = 0.0
    self.time_delta = music_player.time_delta
    self.music_player = music_player

    self.stopping_criteria = stopping_criteria
    self.is_done = False
    
  def step(self, action:List[str]):
    self.timestamp = self.timestamp + self.time_delta
    
    self.is_done = self.stopping_criteria(action)
    
    self.music_player.midi_builder.append(action) 
    
    reward_future = self.music_player.get_reward(self.timestamp)
    return obs, reward_future, self.is_done, {}

  def reset(self):
    self.current_time = 0.0
    self.is_done = False
  
  def render(self, mode='human'):
    
    self.music_player.run()
    

  def close(self):
    self.music_player.close()


