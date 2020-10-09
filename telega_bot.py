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
        status = w.status


        thunderstorm = u'\U0001F4A8'    
        drizzle = u'\U0001F4A7'         
        rain = u'\U00002614'            
        snowflake = u'\U00002744'       
        snowman = u'\U000026C4'         
        atmosphere = u'\U0001F301'     
        clearSky = u'\U00002600'       
        fewClouds = u'\U000026C5'       
        clouds = u'\U00002601'          
        hot = u'\U0001F525'             
        defaultEmoji = u'\U0001F60A'    


        def set_emojo (weather_status):
            try:
                if str(weather_status) == "Thunderstorm":
                    return thunderstorm
                elif str(weather_status) == "Drizzle":
                    return drizzle
                elif str(weather_status) == "Rain":
                    return rain
                elif str(weather_status) == "Snowflake":
                    return snowflake
                elif str(weather_status) == "Snowman":
                    return snowman
                elif str(weather_status) == "Atmosphere":
                    return atmosphere
                elif str(weather_status) == "ClearSky" or "Clear":
                    return clearSky
                elif str(weather_status) == "FewClouds":
                    return fewClouds
                elif str(weather_status) == "Clouds":
                    return clouds
                elif str(weather_status) == "Hot":
                    return hot
                else:
                    return defaultEmoji        
            except Exception as e:
                print(e)


        answer = "Сейчас: " + str(current_time) + "\n\n"
        answer += "Температура в " + message.text + ": " + str(temperature) + " ℃" + "\n"
        answer += "Ветер: " + str(wind) + " м/с " + "\n"
        answer += "В общем - " + w.detailed_status + set_emojo(status) + "\n\n"

        if temperature < 10:
            answer += "Сейчас очень холодно, одевайся!"
        elif temperature < 20:
            answer += "Сейчас холодно, оденься теплее."
        else:
            answer += "Сейчас тепло, одевай что хочешь."

        bot.send_message(message.chat.id, answer)
        print(status)
    except Exception as e:
        error = str(e)
        bot.send_message(message.chat.id, error + ". Please try again!")



bot.polling(none_stop=True)


