from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from get_weather import get_weather
from get_timezone import get_timezone
from datetime import timedelta, timezone, datetime
import os

load_dotenv()

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
    update.message.reply_text("Введите город,в котором вы хотите узнать погоду")
    return 1


def start_time_conversation(update, context):
    update.message.reply_text("Введите город,в котором вы хотите узнать время")
    return 2


def get_weather_information(update, context):
    information_about_weather = get_weather(update.message.text)
    if information_about_weather == None:
        update.message.reply_text('Извините, такой город не найден', reply_markup=markup)
        return ConversationHandler.END
    icon = information_about_weather["Icon"]
    condition = information_about_weather["condition"]
    context.bot.send_photo(update.message.chat_id, icon, caption=condition)
    answer = [f"{parameter}: {information_about_weather[parameter]}"
              for parameter in information_about_weather if parameter not in ["Icon", 'condition']]
    update.message.reply_text("\n".join(answer), reply_markup=markup)
    return ConversationHandler.END


def get_time_inforamtion(update, context):
    information_about_timezone = get_timezone(update.message.text)
    if information_about_timezone == None:
        update.message.reply_text('Извините, такой город не найден', reply_markup=markup)
        return ConversationHandler.END
    time_change_in_timezone = timedelta(hours=information_about_timezone)
    timezone_in_city = timezone(time_change_in_timezone)
    time = datetime.now(tz=timezone_in_city).strftime('%H:%M:%S')
    update.message.reply_text(time, reply_markup=markup)
    return ConversationHandler.END


def stop(update, context):
    return ConversationHandler.END


def run_telegram_bot():
    updater = Updater(os.getenv("TOKEN"), use_context=True)
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
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    run_telegram_bot()
