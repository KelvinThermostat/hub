from logging import exception
from os import environ
from threading import Event, Thread

from influxdb import InfluxDBClient
from kelvin.service.temperature import TemperatureService


class DashboardWorker():
    def __init__(self, shuttingdown_event: Event):
        self.shuttingdown_event = shuttingdown_event
        self.temperature_service = TemperatureService.get_instance()

        database = environ['influxdb_database']
        self.client = InfluxDBClient(environ['influxdb_host'],
                                     database=database)
        self.client.create_database(database)

    def start(self):
        thread = Thread(target=self._worker)
        thread.start()

    def _worker(self):
        # Delay to only start after other workers
        self.shuttingdown_event.wait(2)

        while not self.shuttingdown_event.is_set():
            try:
                json_body = [
                    {
                        "measurement": "current_temperature",
                        "fields": {
                            "value":
                            self.temperature_service.actual_temperature
                        }
                    },
                    {
                        "measurement": "target_temperature",
                        "fields": {
                            "value":
                            self.temperature_service.get_target_temperature()
                        }
                    },
                    {
                        "measurement": "humidity",
                        "fields": {
                            "value": self.temperature_service.humidity
                        }
                    },
                    {
                        "measurement": "heating",
                        "fields": {
                            "value": self.temperature_service.heating
                        }
                    }
                ]

                self.client.write_points(json_body)

            except:
                exception('Error on DashboardWorker._worker.')

            finally:
                self.shuttingdown_event.wait(120)
