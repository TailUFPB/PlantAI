import gym
from gym import spaces, logger
import numpy as np

# Temperatura, umidade

# Temp:    21 até 27
# Umidade: 60 até 65

class BasilEnv(gym.Env):
    def __init__(self) -> None:
        self.observation_space = spaces.Box(np.array([21., 60.]), np.array([27., 65.]), dtype=np.float64)
        # [(+temp), (+umid), (+temp e umid), (vazio)]
        self.action_space = spaces.Discrete(4)
        self.state = self.observation_space.sample()
        self.steps_beyond_done = None

    def reset(self):
        self.step_number = 0
        self.state = self.observation_space.sample()
        self.steps_beyond_done = None
        return self.state
    
    def step(self, action, reward=0):
        '''
        Action = [0(+temp), 1(+umid), 2(+temp,+umid), 3(vazio)]
        '''

        self.step_number += 1
        
        if action == 0:
            self.state[0] += 0.5
            reward -= 0.1

        if action == 1:
            self.state[1] += 0.5
            reward -= 0.1

        if action == 2:
            self.state[0] += 0.5
            self.state[1] += 0.5
            reward -= 0.2

        if action == 3:
            pass
        

        temperature, humidity = self.state

        done = bool(
            temperature < 21
            or temperature > 27
            or humidity < 60
            or humidity > 65
        )

        if self.step_number >= 10000:
            done = True

        if not done:
            reward += 0.5
        elif self.steps_beyond_done is None:
            # Pole just fell!
            self.steps_beyond_done = 0
            reward += 0.5
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