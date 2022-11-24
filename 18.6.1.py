import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу с ботом введите команду в следующем формате:\n\
<имя валюты> \
<имя валюты конвертации> \
<количество первой валюты>\n\
Увидеть список всех валют можно по команде /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values_low = message.text.lower()
        values = values_low.split(' ')
        if len(values) > 3:
            raise ConvertionException("Много параметров")
        if len(values) < 3:
            raise ConvertionException("Мало параметров")
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote.lower(), base.lower(), amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        if int(amount) % 10 == 1 and quote == 'доллар':
            text = f'Цена {amount} {quote}а в {base} - {total_base} {base}'
            bot.send_message(message.chat.id, text)
        elif quote =='доллар':
            text = f'Цена {amount} {quote}ов в {base} - {total_base} {base}'
            bot.send_message(message.chat.id, text)
        elif (int(amount) % 10 == 0 or int(amount) % 10 >= 5) and quote == 'рубль':
            text = f'Цена {amount} рублей в {base} - {total_base} {base}'
            bot.send_message(message.chat.id, text)
        elif int(amount) % 2 == 0 and quote == 'рубль':
            text = f'Цена {amount} рубля в {base} - {total_base} {base}'
            bot.send_message(message.chat.id, text)
        else:
            text = f'Цена {amount} {quote} в {base} - {total_base} {base}'
            bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)