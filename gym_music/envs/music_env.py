from gym import Env
import akro
import asyncio
import numpy as np
from scipy.special import softmax

from ..utils.builders import MidiBuilder
from ..utils.players import MidiPlayer
from ..utils.sequence import EventSeq, ControlSeq

class MusicEnv(Env):
  metadata = {'render.modes': ['human']}
  name = 'Music-Env'

  model = {
    'init_dim': 32,
    'event_dim': EventSeq.dim(),
    'control_dim': ControlSeq.dim(),
  }

  def __init__(self, max_rounds = 30, builder = None, player = None, monitor = None):
    super().__init__()

    self.action_space = akro.Discrete(self.model['event_dim'])
    self.observation_space = akro.Discrete(2)
    self.default_dtype = 'int32'
    # define Midi utility objects

    self.builder = MidiBuilder() if builder is None else builder
    self.player = MidiPlayer(monitor = monitor) if player is None else player

    # stop condition number of rounds
    self._proto_rounds = 0
    self.max_proto_rounds = max_rounds
    self._max_episode_steps = max(max_rounds,1)

  def step(self, action):
    self._proto_rounds = self._proto_rounds + 1
    note = action+1
    if self._is_stop_action(action):
      self.builder.append(note)
      midi_file_path = self.builder.build()

      reward = self.player.queue(midi_file_path)
      reward = reward.result() if asyncio.isfuture(reward) else reward 
      obs = 0
      done = True


    else:
      self.builder.append(note)
      reward = 0
      obs = 1
      done = False

    return (np.array((obs,),dtype = self.default_dtype),
            np.array(reward, dtype = self.default_dtype),
            done,
            {},
           )

  def reset(self):
    self._proto_rounds = 0
    self.builder.reset()
    self.player.reset()
    initial_obs = np.array((0,),dtype = self.default_dtype)
    return initial_obs
  
  def render(self, mode='human',):
    pass

  def close(self):

    self.builder.close()
    self.player.close()
    

  def _is_stop_action(self,action):
    return self._proto_rounds >= self.max_proto_rounds
   
