
from gym_music.envs.music_env import MusicEnv
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
  
  with open('test/utils/example_actions.txt','r') as f:
    for line in f.readlines():
      line = line.strip('][\n')
      action = np.array([int(s) for s in line.split(',')])
      actions.append(action)


  
  with MusicEnv() as env:

    agent = RandomAgent(Discrete(len(actions)))

    for i in range(3):
      env.reset()
      obs,reward,done = (0,0,0)
      
      while True:
        action_idx = agent.act(obs, reward, done)
        action = actions[action_idx]
        obs, reward, done, _ = env.step(action)
        if done:
          break
