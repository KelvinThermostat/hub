import threading
import time
from influxdb import InfluxDBClient
from requests import get

def background_calculation():
    client = InfluxDBClient('influxdb', database='kelvin')
    client.create_database('kelvin')

    while True:
        print('Reading...')
        current_temperature, target_temperature, humidity  = read_sensor()

        json_body = [
            {
                "measurement": "current_temperature",
                "fields": {
                    "value": current_temperature
                }
            },
            {
                "measurement": "target_temperature",
                "fields": {
                    "value": target_temperature
                }
            },
            {
                "measurement": "humidity",
                "fields": {
                    "value": humidity
                }
            },
        ]

        client.write_points(json_body)

        time.sleep(120)


def read_sensor():
    response = get('http://192.168.68.201/api/status')

    reading = response.json()

    return reading['actual_temperature'], reading['target_temperature'], reading['humidity']

def main():
    thread = threading.Thread(target=background_calculation)
    thread.start()


if __name__ == '__main__':
    main()
