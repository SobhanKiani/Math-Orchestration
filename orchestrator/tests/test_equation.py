import json
import unittest
from unittest.mock import patch
from server import api
import math


class EquationEndpointTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.test_client()
        self.app.testing = True

    def test_calculate_equation_valid_input(self):

        with patch('services.post_multiply') as mock_multiply, \
                patch('services.post_power') as mock_power, \
                patch('services.post_sqrt') as mock_sqrt, \
                patch('services.post_sub') as mock_sub, \
                patch('services.post_division') as mock_division, \
                patch('services.post_sum') as mock_sum:
            data = {'a': 1, 'b': -5, 'c': 6}
            mock_power.return_value = data['b'] ** 2
            mock_sqrt.return_value = mock_power.return_value - (4 * data['a'] * data['c'])
            mock_sum.return_value = -data['b'] + mock_sqrt.return_value
            mock_sub.side_effect = lambda args: mock_power.return_value - \
                (4 * data['a'] * data['c']) if mock_power.return_value in args else - \
                (data['b']) - mock_sqrt.return_value
            mock_multiply.side_effect = lambda args: 2 * \
                data['a'] if 2 in args and data['a'] in args else 4 * data['a'] * data['c']

            val1 = -(data['b']) + mock_sqrt.return_value
            val2 = -(data['b']) - mock_sqrt.return_value

            mock_division.side_effect = lambda args: val1 / \
                (2 * data['a']) if val1 in args['numbers'] else val2 / (2 * data['a'])

            response = self.app.post('/equation', json=data)
            # print("RES", mock_sqrt.return_value)

            expected_result = {'result': {'results': [
                3, 2]}, 'status_code': 200}
            self.assertEqual(response.status_code, expected_result['status_code'])
            self.assertEqual(response.json, expected_result['result'])

            # mock_multiply.assert_any_call([2, data['a']])
            # mock_power.assert_called_once_with({'base': data['b'], 'exponent': 2})
            # # mock_sqrt.assert_called_once_with({'number': 1})
            # mock_sum.assert_called_once_with({'numbers': [-data['b'], mock_sqrt.return_value]})
            # mock_sub.assert_any_call(
            #     {'numbers': [mock_power.return_value, mock_multiply.return_value * data['c']]})

    def test_calculate_equation_invalid_input(self):
        data = {'a': 3, 'b': 'not_a_number', 'c': -1}
        response = self.app.post('/equation', data=json.dumps(data),
                                 content_type='application/json')
        print(response.data)

        expected_result = {
            "result": b'Error: All of the coeffs should be numbers', 'status_code': 400}
        self.assertEqual(response.status_code, expected_result['status_code'])
        self.assertEqual(response.data, expected_result['result'])

    def test_calculate_equation_no_real_roots(self):
        with patch('services.post_multiply') as mock_multiply, \
             patch('services.post_power') as mock_power, \
             patch('services.post_sqrt') as mock_sqrt, \
             patch('services.post_sub') as mock_sub, \
             patch('services.post_sum') as mock_sum:
            mock_multiply.return_value = 12
            mock_power.return_value = 4
            mock_sub.return_value = -8

            data = {'a': 1, 'b': 2, 'c': 3}
            response = self.app.post('/equation', data=json.dumps(data), content_type='application/json')

            expected_result = {'result': {'results': "No Real Roots"}, 'status_code': 200}
            self.assertEqual(response.status_code, expected_result['status_code'])
            self.assertEqual(response.json, expected_result['result'])

