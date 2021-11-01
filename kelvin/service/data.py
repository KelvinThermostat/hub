from os import environ

from influxdb import InfluxDBClient


class DataService:
    def __init__(self):
        database = environ['influxdb_database']
        self.client = InfluxDBClient(environ['influxdb_host'],
                                     database=database)
        self.client.create_database(database)

    def get_average_temperature(self):
        response = self.client.query(
            'SELECT mean("value") FROM "current_temperature" WHERE time > now() - 10m'
        )

        print(response)

    def set_measurements(self, current_temperature, target_temperature,
                         humidity, heating):
        json_body = [{
            "measurement": "current_temperature",
            "fields": {
                "value": current_temperature
            }
        }, {
            "measurement": "target_temperature",
            "fields": {
                "value": target_temperature
            }
        }, {
            "measurement": "humidity",
            "fields": {
                "value": humidity
            }
        }, {
            "measurement": "heating",
            "fields": {
                "value": heating
            }
        }]

        self.client.write_points(json_body)
