import logging
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

logging.basicConfig(level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")

api = Flask(__name__)
metrics = PrometheusMetrics(api)

metrics.info("power_microservice_info", "The information of power microservice", version="1.0.0")


@api.route('/power', methods=['POST'])
def calculate_power():
    
    data = request.get_json()
    if not data:
        return 'Error: request must contain a JSON object with a list of numbers.', 400

    base = data['base']
    exponent = data['exponent']
    if not isinstance(base, int) or not isinstance(exponent, int):
        return 'Error: request must contain a JSON array of numbers.', 400
    
    if base == 0:
        return "Error: base cannot be 0", 400

    try:
        total = base ** exponent
        return {'power': total}, 200
    except TypeError:
        return 'Error: request must contain a JSON array of numbers.', 400

