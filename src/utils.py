from numpy.core.fromnumeric import argmax
import pickle

class Agent:
    def __init__(self):
        self.model = self.load_model("'files/model.pkl'")

    def load_model(self, path):
        with open(path, 'rb') as model:
            return pickle.load(model)
    
    def discretize_state(self, state):
        new_state = tuple()
        for i, element in enumerate(state):
            new_state = new_state + (int(element - self.bounds[i]['lower']),)
        
        return new_state
    
    def decide_action(self, state):
        discretized_state = self.discretize_state(state)
        return argmax(self.model[discretized_state])