from v1.config import BOT_TOKEN

from logging import getLogger

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext.filters import Filters

import weather.search
import weather.weather as wethr

from googletrans import Translator

import database.db as db

bot_logger = getLogger(__name__)

translator = Translator()


def debug_requests(f):
    def inner(*args, **kwargs):
        try:
            bot_logger.info(f'Function {f.__name__}')
        except Exception:
            bot_logger.exception(f'Error in handler {f.__name__}')
            raise

    return inner


def get_base_reply_keyboard():
    keyboard = [
        [KeyboardButton(text='⭐️Вибрані⭐️'), KeyboardButton(text='⛔️Очистити вибрані⛔️')],
        [KeyboardButton(text='🆘Допомога🆘')]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_city_choose(citys):
    """Build an inline keyboard with output from function weather.search()"""

    if type(citys) == list:
        if 3 > len(citys) > 0:
            keyboard = [[InlineKeyboardButton(text=city, callback_data='callback_' + city) for city in citys if city != '<null>']]
        elif 5 > len(citys) >= 3:
            keyboard = [[InlineKeyboardButton(text=city, callback_data='callback_' + city) for city in
                         citys[:int(len(citys) / 2)] if city != '<null>'],
                        [InlineKeyboardButton(text=city, callback_data='callback_' + city) for city in
                         citys[int(len(citys) / 2):] if city != '<null>']]
        elif 7 > len(citys) >= 5:
            keyboard = [[InlineKeyboardButton(text=city, callback_data='callback_' + city) for city in
                         citys[:int(len(citys) / 3)] if city != '<null>'],
                        [InlineKeyboardButton(text=city, callback_data='callback_' + city) for city in
                         citys[int(len(citys) / 3):int(len(citys) / 3) + int(len(citys) / 3)] if city != '<null>'],
                        [InlineKeyboardButton(text=city, callback_data='callback_' + city) for city in
                         citys[int(len(citys) / 3) + int(len(citys) / 3):] if city != '<null>']]
        elif 9 > len(citys) >= 7:
            keyboard = [[InlineKeyboardButton(text=city, callback_data='callback_' + city) for city in
                         citys[:int(len(citys) / 4)] if city != '<null>'],
                        [InlineKeyboardButton(text=city, callback_data='callback_' + city) for city in
                         citys[int(len(citys) / 4):int(len(citys) / 4) + int(len(citys) / 3)] if city != '<null>'],
                        [InlineKeyboardButton(text=city, callback_data='callback_' + city) for city in
                         citys[int(len(citys) / 4) + int(len(citys) / 4):int(3 * len(citys) / 4)] if city != '<null>'],
                        [InlineKeyboardButton(text=city, callback_data='callback_' + city) for city in
                         citys[int(3 * len(citys) / 4):] if city != '<null>']]

        else:
            keyboard = None
        if keyboard is not None:
            return InlineKeyboardMarkup(keyboard)


def start_handle(bot, update):
    """Handling command '/start''"""

    bot.send_message(update.message.chat_id,
                     text='Привіт, надішли мені назву міста',
                     reply_markup=get_base_reply_keyboard())

    # print(update)


def favorites_buttons(favorites_list):
    print(favorites_list)
    keyboard = [[InlineKeyboardButton(text=fav, callback_data='callback_' + fav) for fav in favorites_list]]

    return InlineKeyboardMarkup(keyboard)


def choose_city(bot, update):
    """Show inline buttons"""
    if update.message.text == '⭐️Вибрані⭐️':
        bot.send_message(update.message.chat_id,
                         text='⭐️Вибрані⭐️',
                         reply_markup=get_city_choose(db.get_favorites(update.message.chat_id)[0][0].split(', ')))
        print(db.get_favorites(update.message.chat_id)[0][0])
    elif update.message.text == '🆘Допомога🆘':
        pass
    elif update.message.text == '⛔️Очистити вибрані⛔️':
        db.del_favorites(update.message.chat_id)
    else:
        # print(translator.translate(update.message.text, dest='en').text)
        # print(type(weather.search.search_city(update.message.text)), type(list))
        if type(weather.search.search_city(translator.translate(update.message.text, dest='en').text)) != type([]):
            bot.send_message(update.message.chat_id,
                             text='❗❗️❗️There are no cities matching this query❗️❗️❗️',
                             )
        else:

            bot.send_message(update.message.chat_id,
                             text='🌆Choose city🌆',
                             reply_markup=get_city_choose(
                                 weather.search.search_city(translator.translate(update.message.text, dest='en').text)))
        # print(weather.search.search_city(update.message.text)[0][0:weather.search.search_city(update.message.text)[0].index('(')])


def add_to_favorites_button():
    keyboard = [[InlineKeyboardButton(text='⭐️Add to favorites', callback_data='callback_fav')]]
    return InlineKeyboardMarkup(keyboard)


def buttons_handle(bot, update, chat_data=None, **kwargs):
    """Hadle user peek dorm inline buttons and show weather"""

    query = update.callback_query
    print(query)
    data = query.data
    db.init_db()
    if data == 'callback_fav':
        bot.send_message(query['message']['chat']['id'],
                         text='✅Добавлено в вибрані✅')
        db.add_to_favorite(query['message']['chat']['id'],
                           query['message']['text'][14:query['message']['text'].index('п') - 1])
    else:
        if '(' in data:
            city = translator.translate(data[data.index('_') + 1:data.index('(')], dest='en').text
            print(city)
            wthr = wethr.get_weather(city=city)
        # print(wthr['current_condition'][0]['temp_C'])
            message = f"☂️☂️☂️Погода у {city} прямо зараз☂️☂️☂️\n" \
                      f"☀️Температура повітря зараз - {wthr['current_condition'][0]['temp_C']}°C\n" \
                      f"🌡Відчувається як {wthr['current_condition'][0]['FeelsLikeC']}°C\n" \
                      f"🌬Швидкість вітру {wthr['current_condition'][0]['windspeedKmph']} км/г\n" \
                      f"Кількість опадів - {wthr['current_condition'][0]['precipMM']} мм\n" \
                      f"Вологість - {wthr['current_condition'][0]['humidity']} %"
            bot.send_message(query['message']['chat']['id'],
                         text=message,
                         reply_markup=add_to_favorites_button())

            if not db.get_id(query['message']['chat_id']):
                db.insert_to_db(query['message']['chat']['id'], True)
        else:
            city = translator.translate(data[data.index('_') + 1:], dest='en').text
            print(city)
            wthr = wethr.get_weather(city=city)
            # print(wthr['current_condition'][0]['temp_C'])
            message = f"☂️☂️☂️Погода у {city} прямо зараз☂️☂️☂️\n" \
                      f"☀️Температура повітря зараз - {wthr['current_condition'][0]['temp_C']}°C\n" \
                      f"🌡Відчувається як {wthr['current_condition'][0]['FeelsLikeC']}°C\n" \
                      f"🌡Швидкість вітру {wthr['current_condition'][0]['windspeedKmph']} км/г"
            bot.send_message(query['message']['chat']['id'],
                             text=message,
                             reply_markup=add_to_favorites_button())

            if not db.get_id(query['message']['chat_id']):
                db.insert_to_db(query['message']['chat']['id'], True)


def main():
    bot = Bot(token=BOT_TOKEN)

    updater = Updater(bot=bot)

    start_handler = CommandHandler('start', start_handle)
    city_choose_handler = MessageHandler(filters=Filters.text, callback=choose_city)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(city_choose_handler)

    buttons_handler = CallbackQueryHandler(callback=buttons_handle, pass_chat_data=True)

    updater.dispatcher.add_handler(buttons_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

# TODO Button handlers +
# TODO Translator
# TODO get_weather() module +
# TODO Beautify
# TODO Змінити long_polling на bebhook
