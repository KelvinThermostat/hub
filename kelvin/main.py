from fastapi import FastAPI

from .service.temperature import TemperatureService
from .worker import start_workers, stop_workers

temperature_service = TemperatureService.getInstance()

app = FastAPI()


@app.on_event('startup')
def startup():
    start_workers()


@app.on_event('shutdown')
def shutdown():
    stop_workers()


@app.get('/api/heating/boost/<int:minutes>', status_code=201)
def heating_boost(minutes):
    temperature_service.boost(minutes)


@app.get('/api/heating/stop', status_code=201)
def heating_stop():
    temperature_service.stop_heating()


@app.get('/api/heating/target/<float:temperature>', status_code=201)
def set_temperature(temperature):
    temperature_service.target_temperature = temperature


@app.get('/api/status')
def status():
    response = {
        'actual_temperature': temperature_service.actual_temperature,
        'boosting': temperature_service.boosting,
        'heating': temperature_service.heating,
        'heating_end': temperature_service.heating_end,
        'heating_started': temperature_service.heating_started,
        'target_temperature': temperature_service.target_temperature,
    }

    return response
