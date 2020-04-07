import requests
import telebot


def get_curr_rate(curr):
    url = 'http://134.122.29.160/api/v1/currency/rates/'
    api_params = {
        'USD': {'currency': '1'},
        'EUR': {'currency': '2'}
    }[curr]

    headers = {
               'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg3NDA2ODQ3LCJqdGkiOiI2MTA0Y2QwODYyYmY0OGI1YTNhZjNhMGVhMmFhYTlkYyIsInVzZXJfaWQiOjF9.rlDop6ABNnpuju7iWc6OWo7Zi-0RywR7zzID7VqxdSc'}

    r = requests.get(url, headers=headers, params=api_params)
    rates = r.json()
    bot_asw = []
    for rate in rates:
        bot_asw.append(f'Date: {rate["created"]}, Buy: {rate["buy"]}, Sale: {rate["sale"]}, Source: {rate["get_source_display"]}')
    return bot_asw



# Настройка телеграмм бота
TOKEN = "878387462:AAGeJ3SbULbnWfplP-FT65AFkO_zfGLcGFw"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    lastChatId = message.chat.id
    bot.reply_to(message, "Testing my first bot")
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton("EUR")
    itembtn2 = telebot.types.KeyboardButton("USD")
    markup.add(itembtn1, itembtn2)
    bot.send_message(lastChatId, 'My code works and I have no idea why', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    lastChatId = message.chat.id

    if message.text == 'EUR':
      bot.send_message(lastChatId, '\n'.join(get_curr_rate('EUR')))
    elif message.text == 'USD':
      bot.send_message(lastChatId, '\n'.join(get_curr_rate('USD')))

print('Bot is ready!')
bot.polling()
