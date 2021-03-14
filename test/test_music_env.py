
from gym_music.envs.music_env import MusicEnv
from gym_music.utils.monitors import Monitor
from gym.spaces import Discrete
import numpy as np

class RandomAgent(object):
  """RandomAgent from gym documentation"""
  def __init__(self, action_space):
    self.action_space = action_space

  def act(self, observation, reward, done):
    return self.action_space.sample()


if __name__ == "__main__":
  
  actions = []
  
  with MusicEnv(monitor = Monitor()) as env:

    agent = RandomAgent(env.action_space)

    for i in range(3):
      obs = env.reset()
      reward,done = (0,0)
      
      while True:
        action = agent.act(obs, reward, done)
        obs, reward, done, _ = env.step(action)
        if done:
          break
