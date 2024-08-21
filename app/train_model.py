import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# Constants for the DQN model
ALPHA = 0.001
GAMMA = 0.9
EPSILON = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995

features = [
    "Unauthorized Access",
    "Incomplete Whitelists Checks",
    "Lack of Event Logging",
    "Gas Efficiency",
    "Documentation"
]

class DQNAgent:
    def __init__(self, state_space, action_space):
        self.state_space = state_space
        self.action_space = action_space
        self.memory = deque(maxlen=2000)
        self.gamma = GAMMA
        self.epsilon = EPSILON
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = EPSILON_DECAY
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential()
        model.add(layers.Dense(24, input_dim=self.state_space, activation='relu'))
        model.add(layers.Dense(24, activation='relu'))
        model.add(layers.Dense(self.action_space, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=ALPHA))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, use_epsilon=True):
        if use_epsilon and np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        q_values = self.model.predict(state, verbose=0)
        return np.argmax(q_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state, verbose=0)[0])
            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_model(self, file_name):
        self.model.save(file_name)

class SmartContractEnvironment:
    def __init__(self):
        self.state_space = len(features)
        self.action_space = 2

    def reset(self):
        return [0] * self.state_space

    def step(self, action):
        reward = random.choice([1, -1])
        done = random.choice([True, False])
        self.state = [random.randint(0, 1) for _ in range(self.state_space)]
        return self.state, reward, done

def train_dqn(epochs=50, batch_size=32):
    env = SmartContractEnvironment()
    agent = DQNAgent(state_space=env.state_space, action_space=env.action_space)
    rewards_list = []

    for epoch in range(epochs):
        state = env.reset()
        state = np.reshape(state, [1, env.state_space])
        total_reward = 0

        for time in range(500):
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            next_state = np.reshape(next_state, [1, env.state_space])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward

            if done:
                break

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

        rewards_list.append(total_reward)

    agent.save_model("dqn_model.h5")

if __name__ == "__main__":
    train_dqn(epochs=1000, batch_size=32)