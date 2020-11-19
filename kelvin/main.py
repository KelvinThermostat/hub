from fastapi import FastAPI, Request

from .database import create
from .service.temperature import TemperatureService
from .worker import start_workers, stop_workers

temperature_service = TemperatureService.get_instance()

app = FastAPI()


@app.on_event('startup')
def startup():
    create()
    start_workers()


@app.on_event('shutdown')
def shutdown():
    stop_workers()


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Cache-Control'] = 'no-store'

    return response


@app.get('/api/heating/boost/{minutes}', status_code=201)
def heating_boost(minutes: int):
    temperature_service.boost(minutes)


@app.get('/api/heating/stop', status_code=201)
def heating_stop():
    temperature_service.stop_heating()


@app.get('/api/heating/target/{temperature}', status_code=201)
def set_temperature(temperature: float):
    temperature_service.set_target_temperature(temperature)


@app.get('/api/status')
def status():
    response = {
        'actual_temperature': temperature_service.actual_temperature,
        'boosting': temperature_service.boosting,
        'heating': temperature_service.heating,
        'heating_end': temperature_service.heating_end,
        'heating_started': temperature_service.heating_started,
        'target_temperature': temperature_service.get_target_temperature(),
    }

    return response
