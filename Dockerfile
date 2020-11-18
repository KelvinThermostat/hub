FROM python:3.8

COPY . /home/kelvin
WORKDIR /home/kelvin
RUN pip install -r requirements.txt
EXPOSE 5000

ENTRYPOINT [ "uvicorn", "kelvin.main:app" ]
