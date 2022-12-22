from fastapi import FastAPI, Request

from .worker import start_workers, stop_workers

app = FastAPI()


@app.on_event('startup')
def startup():
    start_workers()


@app.on_event('shutdown')
def shutdown():
    stop_workers()


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Cache-Control'] = 'no-store'

    return response
