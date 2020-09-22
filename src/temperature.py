from datetime import datetime, timedelta
from logging import exception, info
from os import environ
from threading import Thread
from time import sleep

from influxdb import InfluxDBClient
from requests import get

from heater import HeaterService


class TemperatureService:
    _instance = None

    def __init__(self):
        self.actual_temperature = 0.0
        self.target_temperature = 0.0
        self.humidity = 0

        self._boosting = False
        self._heating_end = None
        self._heating = False
        self._heating_started = None
        self._sensor_url = environ.get('sensor_url')
        self._heater = HeaterService()

    @staticmethod
    def getInstance():
        if TemperatureService._instance == None:
            TemperatureService._instance = TemperatureService()

        return TemperatureService._instance

    def boost(self, minutes):
        if self._boosting:
            raise Exception('Boosting in progress.')

        self._boosting = True
        self._heat(minutes)

    def start(self):
        thread = Thread(target=self._worker)
        thread.start()

    def _check_heating_start(self):
        if self.actual_temperature <= self.target_temperature:
            self._heat(30)

    def _check_heating_stop(self):
        if self.actual_temperature > self.target_temperature \
            and datetime.now() > self._heating_end:

            info('Stopping heating.')
            self._heater.stop()
            self._boosting = False
            self._heating = False
            self._heating_end = None
            self._heating_started = None

    def _heat(self, minutes):
        self._heater.start()
        self._heating = True
        self._heating_end = datetime.now() + timedelta(minutes=minutes)
        self._heating_started = datetime.now()

        info('Starting heating until {self._heating_end}')

    def _read_sensor(self):
        info('Reading sensor')

        response = get(f'{self._sensor_url}/api/status')
        reading = response.json()

        self.actual_temperature = reading['actual_temperature']
        self.humidity = int(reading['humidity'])

    def _worker(self):
        while True:
            try:
                self._read_sensor()

                info(
                    f'Checking temperature. Current: {self.actual_temperature}'
                )

                if self._heating:
                    self._check_heating_stop()
                else:
                    self._check_heating_start()
            except:
                exception('Error on TemperatureService._worker.')
            finally:
                sleep(60)
