import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('6403907703:AAF-w0kF0AwTmrrYoPMohfoV0_RqV8rmlcw')

admin = 1402781294
#admin = 999985425

inline_kb1 = InlineKeyboardMarkup()
inline_btn_1 = InlineKeyboardButton("оставить анонимку💌", callback_data="1")
inline_kb1.add(inline_btn_1)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("оставить анонимку💌")
markup.add(item1)


@bot.message_handler(commands=["start"])
def start(m):
    if m.chat.id == admin:
        bot.send_message(m.chat.id, "ммм, анонимки самому себе, классно!", reply_markup=inline_kb1)

    else:
        bot.send_message(m.chat.id,
                         'привет! хан квокка рад тебя видеть. у тебя есть что-нибудь для него?', reply_markup=inline_kb1)

    return

@bot.callback_query_handler(func=None)
def process_callback_button1(callback_query: types.CallbackQuery):
    if callback_query.data == "1":
        bot.send_message(callback_query.from_user.id, "напиши всё что угодно✏")
        bot.register_next_step_handler(callback_query.message, send_anon)
    else:
        bot.send_message(callback_query.from_user.id, "напиши ответ:")
        bot.register_next_step_handler(callback_query.message, reply_anon, to_answ=callback_query.data)
    return


def send_anon(m):
    bot.send_message(m.chat.id, "спасибо, анонимка отправлена!", reply_markup=markup, parse_mode="Markdown")
    inline_o = InlineKeyboardMarkup()
    otvet = InlineKeyboardButton("ответить💌", callback_data=str(m.chat.id) + " " + str(m.id))
    inline_o.add(otvet)
    if m.content_type != 'text':
        if m.caption is not None:
            bot.copy_message(admin, m.chat.id, message_id=m.id, caption="_новая анонимка:_💌\n\n"+ m.caption, reply_markup=inline_o, parse_mode="Markdown")
        else:
            bot.copy_message(admin, m.chat.id, message_id=m.id, caption="_новая анонимка:_💌\n\n", reply_markup=inline_o, parse_mode="Markdown")
    else:
        bot.send_message(admin, "_новая анонимка:_💌\n\n"+m.text, reply_markup=inline_o, parse_mode="Markdown")
    return

def reply_anon(m, to_answ):
    m1 = telebot.types.Message(message_id=int(to_answ.split()[1]), chat=telebot.types.Chat(id=int(to_answ.split()[0]),
                                                                                            type="private"),
                               from_user={},
                               date=0, content_type=None, options={}, json_string={})
    bot.reply_to(m1, m.text)
    bot.send_message(m.chat.id, "ты ответил на анонимку✔")
    return


@bot.message_handler(func=lambda message: "оставит" in message.text or "написат" in message.text)
def get_anon(m):
    bot.send_message(m.chat.id, "напиши всё что угодно✏")
    bot.register_next_step_handler(m, send_anon)
    return

@bot.message_handler(func=None)
def we_dont_know(m):
    bot.send_message(m.chat.id,
                     'прости, я тебя не понял, попробуй воспользоваться кнопочкой снизу🔽',
                     reply_markup=markup)
    return


from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Masha_han_bot'

if __name__ == '__main__':
    app.run()
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(str(e))
