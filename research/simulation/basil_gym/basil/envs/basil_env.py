import gym
from gym import spaces, logger
import numpy as np

# Temperatura, umidade e luz

# Temp:    21 até 27
# Umidade: 60 até 65
# Falta luz

class BasilEnv(gym.Env):
    def __init__(self) -> None:
        self.observation_space = spaces.Box(np.array([21., 60.]), np.array([27., 65.]), dtype=np.float64)
        # [+/-temp +/-umid]
        self.action_space = spaces.MultiBinary(2)
        self.state = self.observation_space.sample()
        self.steps_beyond_done = None

    def reset(self):
        self.state = self.observation_space.sample()
        self.steps_beyond_done = None
        return self.state
    
    def step(self, action):
        '''
        Action = [+/-temp +/-umid]
            0: negative action related to the metric
            1: positive action related to the metric
        '''
        temp_act = action[0]
        humid_act = action[1]

        self.state[0] += 0.5 if temp_act == 1 else -0.5
        self.state[1] += 2 if humid_act == 1 else -2

        temperature, humidity = self.state

        done = bool(
            temperature < 21
            or temperature > 27
            or humidity < 60
            or humidity > 65
        )

        if not done:
            reward = 1.0
        elif self.steps_beyond_done is None:
            # Pole just fell!
            self.steps_beyond_done = 0
            reward = 1.0
        else:
            if self.steps_beyond_done == 0:
                logger.warn(
                    "You are calling 'step()' even though this "
                    "environment has already returned done = True. You "
                    "should always call 'reset()' once you receive 'done = "
                    "True' -- any further steps are undefined behavior."
                )
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(self.state), reward, done, {}
    
    def render(self):
        print(f'Temperature: {self.state[0]:.2f}°C')
        print(f'Humidity: {self.state[1]:.2f}%')

env = BasilEnv()
env.render()
print(env.step([0, 0]))
print(env.step([0, 0]))
env.render()