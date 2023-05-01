import logging
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics


logging.basicConfig(level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")

api = Flask(__name__)
metrics = PrometheusMetrics(api)

metrics.info("multiply_microservice_info",
             "The information of multiply microservice", version="1.0.0")


@api.route('/multiply', methods=['POST'])
def calculate_multiply():

    data = request.get_json()
    if not data:
        return 'Error: request must contain a JSON object with a list of numbers.', 400

    a = data['a']
    c = data['c']
    if not isinstance(c, int) or not isinstance(a, int):
        return 'Error: Variables Should Be Numbers', 400
    try:

        result = {'2a': 2 * a, '4ac': 4 * a *c }
        return result
    except TypeError:
        return 'Error: request must contain a JSON array of numbers.', 400
     
