from gym.envs.registration import register
import gym

register(
    id='BasilEnv-v0',
    entry_point='basil.envs:BasilEnv',
    max_episode_steps=2000
)