from os import environ

from requests import get


class HeaterService:
    def __init__(self):
        self.heater_switch_url = environ['heater_switch_url']

    def start(self):
        self._switch('on')

    def stop(self):
        self._switch('off')

    def _switch(self, command):
        response = get(f'{self.heater_switch_url}/{command}')

        if response.status_code != 201:
            raise Exception('Invalid response from heater switch.')
