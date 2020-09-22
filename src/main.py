import logging

from dotenv import load_dotenv

from dashboard import DashboardService
from temperature import TemperatureService

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

load_dotenv()


def load_services():
    temperature = TemperatureService.getInstance()
    dashboard = DashboardService()

    temperature.target_temperature = 19.6

    temperature.start()
    dashboard.start()


if __name__ == '__main__':
    load_services()
