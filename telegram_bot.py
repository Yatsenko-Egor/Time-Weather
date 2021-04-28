from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from get_weather import get_weather
from get_timezone import get_timezone
from datetime import timedelta, timezone, datetime
import os

keyboard = [["/time", "/weather"], ['/help']]
markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


def start(update, context):
    update.message.reply_text(
        "Привет! Я бот Time&Weather.")
    update.message.reply_text("Я могу написать время или погоду в интересующем тебя городе", reply_markup=markup)


def help(update, context):
    update.message.reply_text("Для того, чтобы узнать время введите команду /time")
    update.message.reply_text("Для того, чтобы узнать погоду введите команду /weather", reply_markup=markup)


def start_weather_conversation(update, context):
    update.message.reply_text("Введите город, в котором вы хотите узнать погоду")
    return 1


def start_time_conversation(update, context):
    update.message.reply_text("Введите город, в котором вы хотите узнать время")
    return 2


def get_weather_information(update, context):
    try:
        information_about_weather = get_weather(update.message.text)
    except Exception:
        update.message.reply_text('Извините, такой город не найден', reply_markup=markup)
        return ConversationHandler.END
    answer = [information_about_weather["condition"]]
    answer.extend([f"{parameter}: {information_about_weather[parameter]}"
                   for parameter in information_about_weather if parameter not in ["Icon", 'condition']])
    update.message.reply_text("\n".join(answer))
    update.message.reply_text(
        f"Узнать больше можно на сайте Time-Weather по ссылке https://py-time-weather.herokuapp.com/current_weather/{update.message.text}",
        reply_markup=markup)
    return ConversationHandler.END


def get_time_inforamtion(update, context):
    information_about_timezone = get_timezone(update.message.text)
    if information_about_timezone == None:
        update.message.reply_text('Извините, такой город не найден', reply_markup=markup)
        return ConversationHandler.END
    time_change_in_timezone = timedelta(hours=information_about_timezone)
    timezone_in_city = timezone(time_change_in_timezone)
    time = datetime.now(tz=timezone_in_city).strftime('%H:%M:%S')
    update.message.reply_text(time)
    update.message.reply_text(
        f"Узнать больше можно на сайте Time-Weather по ссылке https://py-time-weather.herokuapp.com/current_weather/{update.message.text}",
        reply_markup=markup)
    return ConversationHandler.END


def stop(update, context):
    return ConversationHandler.END


def run_telegram_bot():
    TOKEN = "1740487455:AAGXLm5H-5_QCu5K0-tT_BTulRP9goz7iuc"
    HEROKU_APP_NAME = "time-weather-telegram-bot"
    PORT = int(os.environ.get('PORT', 5000))
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    conversation = ConversationHandler(
        entry_points=[CommandHandler("time", start_time_conversation),
                      CommandHandler("weather", start_weather_conversation)],
        states={1: [MessageHandler(Filters.text, get_weather_information)],
                2: [MessageHandler(Filters.text, get_time_inforamtion)]},
        fallbacks=[CommandHandler('stop', stop)])
    dp.add_handler(conversation)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN, webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
    updater.idle()
    
    
if __name__=="__main__":
    run_telegram_bot()
