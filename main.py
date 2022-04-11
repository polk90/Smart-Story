# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import time
sl = 0
# Определяем функцию-обработчик сообщений.
# У неё два параметра, сам бот и класс updater, принявший сообщение.
def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    pass


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater('5174488691:AAGsK3FwP-cO52ARgiuxgpbuBCzKb6_nQKQ', use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("time", time1))
    dp.add_handler(CommandHandler("date", date))
    dp.add_handler(CommandHandler("set_timer", set_timer))
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
    inline_kb1 = InlineKeyboardMarkup([[inline_btn_1]])


# Запускаем функцию main() в случае запуска скрипта.
@dp.callback_query_handler(func=lambda c: c.data == 'button1')
async def process_callback_button1():
    sms()

def time1(update, context):
    time.sleep(int(sl))
    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M:%S")
    update.message.reply_text(str(current_time))


def butfun():
    pass


def date(update, context):
    time.sleep(int(sl))
    now = datetime.datetime.now()
    current_time = now.strftime("%d/%m/%Y")
    update.message.reply_text(str(current_time))


def sms(update, context):
    update.message.reply_text('111')


def set_timer(update, context):
    global sl
    if int(context.args[0]) >= 0:
        sl = context.args[0]

if __name__ == '__main__':
    main()