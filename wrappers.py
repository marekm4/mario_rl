import gym
import numpy as np

from gym.spaces import Box
from skimage import transform


class CutAndScaleObservation(gym.ObservationWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.shape = (21, 21)
        self.observation_space = Box(low=0, high=255, shape=self.shape, dtype=np.uint8)

    def observation(self, observation):
        resize_obs = transform.resize(observation[120:, 128:], (21, 21))
        resize_obs *= 255
        resize_obs = resize_obs.astype(np.uint8)
        return resize_obs


class SkipFrame(gym.Wrapper):
    def __init__(self, env, skip):
        """Return only every `skip`-th frame"""
        super().__init__(env)
        self._skip = skip

    def step(self, action):
        """Repeat action, and sum reward"""
        total_reward = 0.0
        done = False
        for i in range(self._skip):
            # Accumulate reward and repeat the same action
            obs, reward, done, info = self.env.step(action)
            total_reward += reward
            if done:
                break
        return obs, total_reward, done, info
