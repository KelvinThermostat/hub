import logging

from dotenv import load_dotenv

load_dotenv()

from dashboard import DashboardService
from temperature import TemperatureService
from web import app

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def load_services():
    temperature = TemperatureService.getInstance()
    dashboard = DashboardService()

    temperature.start()
    dashboard.start()


if __name__ == '__main__':
    load_services()
    app.run(host='0.0.0.0')
