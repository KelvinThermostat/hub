from datetime import datetime, timedelta
from logging import info

from .heater import HeaterService

HEATING_INTERVAL = 45

class TemperatureService:
    _instance = None

    def __init__(self):
        self.actual_temperature: float = 0.0
        self.target_temperature: float = 0.0
        self.humidity: int = 0
        self.boosting: bool = False
        self.heating_end: datetime = None
        self.heating: bool = False
        self.heating_started: datetime = None

        self._heater = HeaterService()

    @staticmethod
    def getInstance():
        if TemperatureService._instance == None:
            TemperatureService._instance = TemperatureService()

        return TemperatureService._instance

    def check(self):
        if self.heating:
            self._check_heating_stop()
        else:
            self._check_heating_start()

    def boost(self, minutes):
        if self.boosting:
            return

        self.boosting = True
        self._heat(minutes)

    def stop_heating(self):
        info('Stopping heating.')
        self._heater.stop()
        self.boosting = False
        self.heating = False
        self.heating_end = None
        self.heating_started = None

    def _check_heating_start(self):
        if self.actual_temperature <= self.target_temperature:
            self._heat(HEATING_INTERVAL)

    def _check_heating_stop(self):
        if self.actual_temperature > self.target_temperature \
            and datetime.now() > self.heating_end:
            self.stop_heating()

    def _heat(self, minutes):
        self._heater.start()
        self.heating = True
        self.heating_end = datetime.now() + timedelta(minutes=minutes)
        self.heating_started = datetime.now()

        info('Starting heating until {self._heating_end}')
