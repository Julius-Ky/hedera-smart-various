rom flask import Flask, jsonify, request
import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import threading

# Constants for the DQN model
ALPHA = 0.001  # Learning rate value generally displays useful convergance
GAMMA = 0.9  # Discount factor helps the agent to focus on long-term goals or short term
EPSILON = 1.0  # Exploration rate associated with how random you take an action.
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.995 #rate of decay, it should help faster convergance between the learning for past actions and new ones


# Flask app setup
app = Flask(__name__)

class DQNAgent:
    def __init__(self, state_space, action_space):
        self.state_space = state_space
        self.action_space = action_space
        self.memory = deque(maxlen=2000) # We are using a deque instead normal list in python is because we are performing append function a lot. The complexity of the append function in the list is O(N) and in deque is O(1) which is constant. 
        self.gamma = GAMMA  # Discount factor
        self.epsilon = EPSILON  # Exploration rate
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = EPSILON_DECAY
        self.model = self.build_model()

    def build_model(self):
        # Our Agent will build its own simple neural network model based on learning experience. Let us define it
        model = tf.keras.Sequential()
        model.add(layers.Dense(24, input_dim=self.state_space, activation='relu'))
        model.add(layers.Dense(24, activation='relu'))
        model.add(layers.Dense(self.action_space, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=ALPHA))# adaptive optimizers like Adam helps in sequence of problems as  policy evolves
        return model

    def remember(self, state, action, reward, next_state, done): #The meaning of done, means the episode if it is finished or not
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):  # Begin to make random actions so our neural networks begin to learn and create new connections
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def replay(self, batch_size):# replace the values from the last episode and stick with the actions that worked properly
        minibatch = random.sample(self.memory, batch_size)#minibatch is used to store a small amount of information for the network to build new learning from past experience
        for state, action, reward, next_state, done in minibatch: # For every action there is a reward so the NN will save it.
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

class SmartContractEnvironment:
    def __init__(self):
        self.state_space = 5  # Example: Unauthorized access, Incomplete whitelists checks, Lack of event logging, Gas Efficiency, Documentation
        self.action_space = 2  # Example: recommend improvement or leave as it is
        self.state = [0, 0, 0, 0, 0]  # Initial state

    def reset(self):
        self.state = [0, 0, 0, 0 , 0]
        return self.state

    def step(self, action):
        # This varible introduces the logic for taking a step (action) in the environment
        # You can replace this with the actual contract evaluation logic
        reward = random.choice([1, -1]) #  random reward for simplicity in this logic we do not use punishment since we are already using gamma and epsilon
        done = random.choice([True, False])
        self.state = [random.randint(0, 1) for _ in range(self.state_space)]
        return self.state, reward, done

def simulate_environment(contract_features):
    true_label = contract_features['is_real']
    if not true_label:
        return None

    reward = 1
    return reward

def train_dqn(epochs=1000, batch_size=32):
    env = SmartContractEnvironment()
    agent = DQNAgent(state_space=env.state_space, action_space=env.action_space)
# Lists that store data for plotting performance purposes
    rewards_list = []
    epsilon_list = []
      # Only train if the contract is real
    for epoch in range(epochs):
        contract_features = {'is_real': random.choice([True, False])}
        reward = simulate_environment(contract_features)
        if reward is None:
            continue  # Skip this iteration if the contract is not real

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

            # Append data for plotting
        rewards_list.append(total_reward)
        epsilon_list.append(agent.epsilon)

    # Measure and display the performance of the NN training 
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(rewards_list)
    plt.xlabel('Epoch')
    plt.ylabel('Total Reward')
    plt.title('Rewards over Time')

    plt.subplot(1, 2, 2)
    plt.plot(epsilon_list)
    plt.xlabel('Epoch')
    plt.ylabel('Epsilon')
    plt.title('Epsilon Decay over Time')

    plt.tight_layout()
    plt.savefig('training_results.png')  # Save plot as an image

@app.route('/train', methods=['POST'])
def start_training():
    data = request.json
    epochs = data.get('epochs', 1000)
    batch_size = data.get('batch_size', 32)
    
    # Run training in a separate thread to avoid blocking the main thread
    training_thread = threading.Thread(target=train_dqn, args=(epochs, batch_size))
    training_thread.start()
    
    return jsonify({"message": "Training started!"}), 200

@app.route('/results', methods=['GET'])
def get_results():
    try:
        with open('training_results.png', 'rb') as f:
            img = f.read()
        return img, 200, {'Content-Type': 'image/png'}
    except FileNotFoundError:
        return jsonify({"message": "Training results not found."}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
