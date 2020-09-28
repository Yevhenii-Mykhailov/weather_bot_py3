from pyowm import OWM
from pyowm.utils.config import get_default_config

config = get_default_config()
config['language'] = 'ru'
owm = OWM('19e61cb7f95ce780f94c2f1eeae6f4ec', config)


place = input("В каком городе?: ")
mgr = owm.weather_manager()
observation = mgr.weather_at_place(place)

w = observation.weather
temperature = str(w.temperature('celsius')['temp'])
wind = str(w.wind())
print()
print()
print()
# print(w)
