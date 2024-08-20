from flask import Flask, render_template, request, jsonify
import numpy as np
import random

app = Flask(__name__)

# RL Model Constants
ALPHA = 0.1  # Learning rate
GAMMA = 0.9  # Discount factor
EPSILON = 0.2  # Exploration rate

# Possible recommendations
recommendations = {
    0: "Consider optimizing the gas usage by refactoring expensive operations.",
    1: "The contract appears to be secure based on current analysis.",
    2: "Reduce the complexity of your functions to improve readability and maintainability.",
    3: "Fix potential vulnerabilities, such as reentrancy attacks or unchecked external calls.",
    4: "Use a modular approach to break down large functions into smaller, reusable components."
}

# Simulated environment (this would normally be your dataset)
def simulate_environment(action, contract_features):
    true_label = contract_features['is_real']  # Boolean: True if real, False if fake
    improvement_needed = contract_features['needs_improvement']  # Boolean: Does it need improvement?

    if action == 1:  # Secure analysis
        if true_label and not improvement_needed:
            reward = 1  # Correct recommendation
        else:
            reward = -1  # Incorrect
    elif improvement_needed:
        reward = 2 if action in [0, 2, 3, 4] else -1  # Recommendations for needed improvements
    else:
        reward = 0  # No improvement needed

    return reward

# Initialize Q-table
state_space = 10  # Placeholder for the number of features (states)
action_space = len(recommendations)  # Actions correspond to recommendations
Q_table = np.zeros((state_space, action_space))

# Training the RL agent
def train_agent(epochs=1000):
    for epoch in range(epochs):
        contract_features = {
            'is_real': random.choice([True, False]),
            'needs_improvement': random.choice([True, False])
        }
        state = random.randint(0, state_space - 1)  # Simplified state representation

        if random.uniform(0, 1) < EPSILON:
            action = random.randint(0, action_space - 1)
        else:
            action = np.argmax(Q_table[state])

        reward = simulate_environment(action, contract_features)
        Q_table[state, action] = Q_table[state, action] + ALPHA * (reward + GAMMA * np.max(Q_table[state]) - Q_table[state, action])

# Run the training
train_agent()

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to classify and recommend based on input features
@app.route('/classify', methods=['POST'])
def classify():
    is_real = request.form.get('is_real') == 'true'
    needs_improvement = request.form.get('needs_improvement') == 'true'
    
    contract_features = {
        'is_real': is_real,
        'needs_improvement': needs_improvement
    }
    
    state = random.randint(0, state_space - 1)  # This should be derived from contract features
    action = np.argmax(Q_table[state])
    recommendation = recommendations[action]
    
    return jsonify({'recommendation': recommendation})

if __name__ == '__main__':
    app.run(debug=True)
