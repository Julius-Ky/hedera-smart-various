from flask import Flask, render_template, jsonify
import numpy as np
import tensorflow as tf
import random
import json
import os

app = Flask(__name__)

# Feature list
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
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(24, input_dim=self.state_space, activation='relu'))
        model.add(tf.keras.layers.Dense(24, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_space, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
        return model

    def act(self, state):
        q_values = self.model.predict(state, verbose=0)
        return np.argmax(q_values[0])

    def load_model(self, file_name):
        self.model = tf.keras.models.load_model(file_name)

class SmartContractEnvironment:
    def __init__(self):
        self.state_space = len(features)
        self.action_space = 2

    def reset(self):
        return [0] * self.state_space

def test_pretrained_model(agent):
    agent.load_model("dqn_model.h5")  # Load the pretrained model
    test_states = [
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1]
    ]
    results = []

    for state in test_states:
        state_reshaped = np.reshape(state, [1, len(state)])
        action = agent.act(state_reshaped)

        result = {
            "vulnerability": features[state.index(1)] if 1 in state else "No vulnerability",
            "action": "Apply recommendation" if action == 0 else "Leave it as it is"
        }
        results.append(result)

    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train')
def train_model():
    # Run the training (this would normally be done separately)
    os.system('python train_model.py')
    return jsonify({"message": "Training completed!"})

@app.route('/results')
def results():
    agent = DQNAgent(state_space=len(features), action_space=2)
    results = test_pretrained_model(agent)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
