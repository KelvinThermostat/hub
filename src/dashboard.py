from logging import exception, info
from os import environ
from threading import Thread
from time import sleep

from influxdb import InfluxDBClient
from requests import get

from temperature import TemperatureService


class DashboardService:
    def __init__(self):
        host = environ.get('influxdb_host')
        database = environ.get('influxdb_database')

        self.client = InfluxDBClient(host, database=database)
        self.client.create_database(database)
        self.temperature_service = TemperatureService.getInstance()

    def start(self):
        thread = Thread(target=self._worker)
        thread.start()

    def _worker(self):
        sleep(2)

        while True:
            try:
                json_body = [
                    {
                        "measurement": "current_temperature",
                        "fields": {
                            "value": self.temperature_service.actual_temperature
                        }
                    },
                    {
                        "measurement": "target_temperature",
                        "fields": {
                            "value": self.temperature_service.target_temperature
                        }
                    },
                    {
                        "measurement": "humidity",
                        "fields": {
                            "value": self.temperature_service.humidity
                        }
                    },
                ]

                self.client.write_points(json_body)

            except:
                exception('Error on DashboardService._worker.')

            finally:
                sleep(120)
