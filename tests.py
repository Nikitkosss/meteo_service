import unittest
from unittest.mock import patch
from app import app, get_weather


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('app.requests.get')
    @patch('app.Nominatim.geocode')
    def test_get_weather_valid_city(self, mock_geocode, mock_get):
        mock_geocode.return_value.latitude = 40
        mock_geocode.return_value.longitude = -73
        mock_get.return_value.json.return_value = {
            "hourly": {
                "time": ["2022-09-01T00:00:00", "2022-09-01T01:00:00"],
                "temperature_2m": [20, 21]
            }
        }
        weather_data = get_weather('New York')
        self.assertIsNotNone(weather_data)
        self.assertTrue('00:00:00' in weather_data.keys())
        self.assertTrue('01:00:00' in weather_data.keys())

    @patch('app.requests.get')
    @patch('app.Nominatim.geocode')
    def test_get_weather_invalid_city(self, mock_geocode, mock_get):
        mock_geocode.return_value = None
        weather_data = get_weather('Invalid City')
        self.assertIsNone(weather_data)


if __name__ == '__main__':
    unittest.main()
