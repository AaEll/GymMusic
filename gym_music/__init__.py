from gym.envs.registration import register

register(
    id='music-v0',
    entry_point='gym_music.envs:MusicEnv',
)

