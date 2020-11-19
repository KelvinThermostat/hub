FROM python:3.8

COPY . /app/kelvin
WORKDIR /app/kelvin
RUN pip install -r requirements.txt
EXPOSE 5000

ENTRYPOINT [ "uvicorn", "kelvin.main:app", "--host", "0.0.0.0", "--port", "5000" ]
