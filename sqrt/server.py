import logging
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
import math

logging.basicConfig(level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")

api = Flask(__name__)
metrics = PrometheusMetrics(api)

metrics.info("sqrt_microservice_info", "The information of sqrt microservice", version="1.0.0")


@api.route('/sqrt', methods=['POST'])
def calculate_sqrt():

    data = request.get_json()
    if not data:
        return 'Error: request must contain a JSON object with a a number.', 400

    number = data['number']
    if not isinstance(number, int):
        return 'Error: request must contain a JSON of a number.', 400

    if number < 0:
        return "Error: number should be bigger than 0", 400

    try:
        if number == 0:
            total = 0
        else:
            total = math.sqrt(number)
        return {'sqrt': total}, 200
    except TypeError:
        return 'Error: a non negative number', 400
