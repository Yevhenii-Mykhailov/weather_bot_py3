import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config

config = get_default_config()
config['language'] = 'ru'
owm = OWM('19e61cb7f95ce780f94c2f1eeae6f4ec', config)
bot = telebot.TeleBot("940637130:AAF1jHlCTBr3s0_4J9-OG_A6cMboOMHM4BE")


@bot.message_handler(content_types=['text'])
def send_echo(message):
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(message.text)
    w = observation.weather
    temperature = w.temperature('celsius')['temp']
    wind = w.wind()
    # "℃"

    answer = "Температура в " + message.text + ": " + str(temperature) + "℃" + "\n"
    answer += "Ветер: " + str(wind) + "\n"
    answer += "В общем - " + w.detailed_status + "\n\n"

    if temperature < 10:
        answer += "Сейчас очень холодно, одевайся!"
    elif temperature < 20:
        answer += "Сейчас холодно, оденься теплее."
    else:
        answer += "Сейчас тепло, одевай что хочешь."

    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
