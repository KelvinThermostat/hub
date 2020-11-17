from .dashboard import DashboardWorker
from .sensor import SensorWorker
from threading import Event

SHUTTINGDOWN_EVENT = Event()


def start_workers():
    dashboard_worker = DashboardWorker(SHUTTINGDOWN_EVENT)
    sensor_worker = SensorWorker(SHUTTINGDOWN_EVENT)

    dashboard_worker.start()
    sensor_worker.start()


def stop_workers():
    SHUTTINGDOWN_EVENT.set()
