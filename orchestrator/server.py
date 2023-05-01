import logging
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
# from services import post_multiply, post_power, post_sqrt, post_division, post_sub, post_sum
import json
import services

logging.basicConfig(level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")

api = Flask(__name__)
metrics = PrometheusMetrics(api)

metrics.info("orchestrator_microservice_info",
             "The information of orchestrator microservice", version="1.0.0")


def handle_api_error(response):
    try:
        content = json.loads(response.content)
        if isinstance(content, dict) and 'error' in content:
            return content['error']
        else:
            return "API Error: " + response.content.decode('utf-8')
    except Exception:
        return "API Error: " + response.content.decode('utf-8')


@api.route('/equation', methods=['POST'])
def calculate_equation():

    data = request.get_json()
    a = data['a']
    b = data['b']
    c = data['c']

    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int):
        return "Error: All of the coeffs should be numbers", 400

    try:

        b_exponent_2 = services.post_power({'base': b, 'exponent': 2})
        print("b_exponent_2", b_exponent_2)

        multiply_result = services.post_multiply({'c': c, 'a': a})
        print("MULT_RES", multiply_result)
        a_c_4 = multiply_result['4ac']
        denominator = multiply_result['2a']

        b2_sub_4ac = services.post_sub({'numbers': [b_exponent_2, a_c_4]})

        result = None
        if b2_sub_4ac >= 0:

            sqrt_b2_sub_4ac = services.post_sqrt({'number': b2_sub_4ac})

            numinator1 = services.post_sum({'numbers': [-b, sqrt_b2_sub_4ac]})

            numinator2 = services.post_sub({'numbers': [-b, sqrt_b2_sub_4ac]})

            x1 = services.post_division({'numbers': [numinator1, denominator]})

            x2 = services.post_division({'numbers': [numinator2, denominator]})

            result = {'results': [x1, x2]}, 200

        else:
            result = {'results': "No Real Roots"}, 200

        return result

        # return result

    except Exception as e:
        return e
        # return handle_api_error(e.response), e.response.status_code
