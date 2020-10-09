import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.utils import timestamps

config = get_default_config()
config['language'] = 'ru'
owm = OWM('19e61cb7f95ce780f94c2f1eeae6f4ec', config)
bot = telebot.TeleBot("940637130:AAF1jHlCTBr3s0_4J9-OG_A6cMboOMHM4BE")


@bot.message_handler(commands=['start', 'help'], content_types=['text'])
def send_welcome(message):
    try:
        bot.reply_to(message, "Привет! Напиши название города, желательно латиницей, и я покажу тебе погоду на данный "
                              "момент")
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['text'])
def send_echo(message):
    try:
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        temperature = w.temperature('celsius')['temp']
        wind = w.wind()['speed']
        current_time = timestamps.now('iso')


        thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
        drizzle = u'\U0001F4A7'         # Code: 300's
        rain = u'\U00002614'            # Code: 500's
        snowflake = u'\U00002744'       # Code: 600's snowflake
        snowman = u'\U000026C4'         # Code: 600's snowman, 903, 906
        atmosphere = u'\U0001F301'      # Code: 700's foogy
        clearSky = u'\U00002600'        # Code: 800 clear sky
        fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
        clouds = u'\U00002601'          # Code: 802-803-804 clouds general
        hot = u'\U0001F525'             # Code: 904
        defaultEmoji = u'\U0001F300'    # default emojis


        answer = "Сейчас: " + str(current_time) + "\n\n"
        answer += "Температура в " + message.text + ": " + str(temperature) + " ℃" + "\n"
        answer += "Ветер: " + str(wind) + " м/с " + "\n"
        answer += "В общем - " + w.detailed_status + emojo + "\n\n"

        if temperature < 10:
            answer += "Сейчас очень холодно, одевайся!"
        elif temperature < 20:
            answer += "Сейчас холодно, оденься теплее."
        else:
            answer += "Сейчас тепло, одевай что хочешь."

        bot.send_message(message.chat.id, answer)
    except Exception as e:
        error = str(e)
        bot.send_message(message.chat.id, error + ". Please try again!")



bot.polling(none_stop=True)
