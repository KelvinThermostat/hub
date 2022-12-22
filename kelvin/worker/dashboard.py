from logging import exception
from threading import Event, Thread

from kelvin.service.data import DataService
from kelvin.service.temperature import TemperatureService


class DashboardWorker():
    def __init__(self, shuttingdown_event: Event):
        self.shuttingdown_event = shuttingdown_event
        self.temperature_service = TemperatureService.get_instance()
        self.data_service = DataService()

    def start(self):
        thread = Thread(target=self._worker)
        thread.start()

    def _worker(self):
        while not self.shuttingdown_event.is_set():
            try:
                self.temperature_service.read()

                self.data_service.set_measurements(
                    self.temperature_service.actual_temperature,
                    self.temperature_service.target_temperature,
                    self.temperature_service.humidity,
                    self.temperature_service.heating)

            except:
                exception('Error on DashboardWorker._worker.')

            finally:
                self.shuttingdown_event.wait(60)
