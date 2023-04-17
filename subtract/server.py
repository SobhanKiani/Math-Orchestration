import logging
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

logging.basicConfig(level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")

api = Flask(__name__)
metrics = PrometheusMetrics(api)

metrics.info("subtract_microservice_info", "The information of subtract microservice", version="1.0.0")


@api.route('/subtract', methods=['POST'])
def calculate_subtract():
    
    data = request.get_json()
    if not data:
        return 'Error: request must contain a JSON object with a list of numbers.', 400

    numbers = data['numbers']
    if not isinstance(numbers, list):
        return 'Error: request must contain a JSON array of numbers.', 400
    try:
        total = numbers[0]
        for num in numbers[1:]:
            total -= num
        return {'subtract': total}, 200
    except TypeError:
        return 'Error: request must contain a JSON array of numbers.', 400
     