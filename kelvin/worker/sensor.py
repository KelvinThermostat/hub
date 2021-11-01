from logging import exception, info
from os import environ
from threading import Event, Thread

from kelvin.service.temperature import TemperatureService
from requests import get


class SensorWorker:
    def __init__(self, shuttingdown_event: Event):
        self.shuttingdown_event = shuttingdown_event
        self.temperature_service = TemperatureService.get_instance()
        self._sensor_url = environ['sensor_url']

    def start(self):
        # Ensure the heating is off when monitor starts
        self.temperature_service.stop_heating()

        thread = Thread(target=self._worker)
        thread.start()

    def _read_sensor(self):
        info('Reading sensor')

        response = get(f'{self._sensor_url}/api/status')
        reading = response.json()

        self.temperature_service.actual_temperature = reading[
            'actual_temperature']
        self.temperature_service.humidity = int(reading['humidity'])

    def _worker(self):
        while not self.shuttingdown_event.is_set():
            try:
                self._read_sensor()

                info(
                    f'Checking temperature. Current: {self.temperature_service.actual_temperature}'
                )

                self.temperature_service.check()
            except:
                exception('Error on SensorWorker._worker.')
            finally:
                self.shuttingdown_event.wait(60)
