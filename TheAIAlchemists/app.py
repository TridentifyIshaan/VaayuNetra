from flask import Flask, render_template, request, jsonify  # Import jsonify for returning JSON responses
import pickle
import numpy as np

model = pickle.load(open('/Users/sainava/Desktop/TheAIAlchemists_New/TheAIAlchemists/Cloud_model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve input values from the form
    cpu_usage = float(request.form.get('cpu_usage'))
    memory_usage = float(request.form.get('memory_usage'))
    energy_efficiency = float(request.form.get('energy_efficiency'))
    network_traffic = float(request.form.get('network_traffic'))
    power_consumption = float(request.form.get('power_consumption'))
    execution_time = float(request.form.get('execution_time'))

    # Prepare the input data to match the shape (1, 10, 3)
    input_data = np.array([
        [cpu_usage, memory_usage, energy_efficiency],
        [network_traffic, power_consumption, execution_time],
        [cpu_usage, memory_usage, energy_efficiency],  # Repeat to fill
        [network_traffic, power_consumption, execution_time],
        [cpu_usage, memory_usage, energy_efficiency],
        [network_traffic, power_consumption, execution_time],
        [cpu_usage, memory_usage, energy_efficiency],
        [network_traffic, power_consumption, execution_time],
        [cpu_usage, memory_usage, energy_efficiency],
        [network_traffic, power_consumption, execution_time]
    ])  # This will create an array with shape (10, 3)

    input_data = input_data.reshape(1, 10, 3)  # Now reshape to (1, 10, 3)

    # Make prediction using the model
    prediction = model.predict(input_data)

    # Convert prediction to a regular list
    prediction_values = prediction[0].tolist()  # Convert numpy array to a list

    # Format the prediction results with labels
    response = {
        "CPU-usage": float(prediction_values[0]),  # Convert to float for JSON serialization
        "Memory-usage": float(prediction_values[1]),
        "Energy-efficiency": float(prediction_values[2])
    }

    return jsonify(response)  # Return the response as JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
