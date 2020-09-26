from flask import Flask, jsonify

from temperature import TemperatureService

app = Flask(__name__)
temperature_service = TemperatureService.getInstance()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/heating/boost/<int:minutes>', methods=['GET'])
def heating_boost(minutes):
    temperature_service.boost(minutes)

    return '', 201

@app.route('/api/heating/stop', methods=['GET'])
def heating_stop():
    temperature_service.stop_heating()

    return '', 201

@app.route('/api/heating/target/<float:temperature>', methods=['GET'])
def set_temperature(temperature):
    temperature_service.target_temperature = temperature

    return '', 201

@app.route('/api/status', methods=['GET'])
def status():
    response = {
        'actual_temperature': temperature_service.actual_temperature,
        'boosting': temperature_service.boosting,
        'heating': temperature_service.heating,
        'heating_end': temperature_service.heating_end,
        'heating_started': temperature_service.heating_started,
        'target_temperature': temperature_service.target_temperature,
    }

    return jsonify(response)
