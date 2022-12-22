from logging import info
from os import environ

from requests import get


class TemperatureService:
    _instance = None

    def __init__(self):
        self.actual_temperature: float = 0.0
        self.target_temperature: float = 0.0
        self.humidity: int = 0
        self.boosting: bool = False
        self.heating: bool = False
        self._thermostat_url = environ['thermostat_url']

    @staticmethod
    def get_instance():
        if TemperatureService._instance == None:
            TemperatureService._instance = TemperatureService()

        return TemperatureService._instance

    def read(self):
        info('Reading thermostat')

        response = get(f'{self._thermostat_url}/api/status')
        reading = response.json()

        self.actual_temperature = float(reading['actual_temperature'])
        self.target_temperature = float(reading['target_temperature'])
        self.humidity = int(reading['humidity'])
        self.heating = bool(reading['heating'])
