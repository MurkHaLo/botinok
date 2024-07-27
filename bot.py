import telebot
import Text2ImageAPI

API_TOKEN = '<api_token>'

bot = telebot.TeleBot("7418962566:AAGwke5Uj7CgZ6WPSSPsu4LmbC2a83MX1B8")


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "Ваш заказ принят, ожидайте..")
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', "A635AD912260C35340E39F4AE447D382", "5B21602D3EE528AEBF338C8B2D343D2A")
    model_id = api.get_model()
    uuid = api.generate(message.text, model_id)
    images = api.check_generation(uuid)[0]
    filename = f"image_{message.chat.id}.jpg"
    api.base64_to_img(images, filename)
    image = open(filename, "rb")
    bot.send_photo(message.chat.id, photo=image)


bot.infinity_polling()