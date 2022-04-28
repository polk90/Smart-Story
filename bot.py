import logging
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
definition = 'start'


def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    query = update.callback_query
    update.message.reply_text("Добро пожаловать в интерактивный читальный зал! Здесь вы можете выбрать книгу для "
                              "прохождения из списка ниже.")
    photo = open('images/img.png', 'rb')
    update.message.reply_photo(photo=photo)
    keyboard = [
        [
            InlineKeyboardButton("Начать читать книги", callback_data='0'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Но для начала...', reply_markup=reply_markup)


def star(nupdate: Update, ncontext: CallbackContext, photo) -> None:
    nupdate.message.reply_photo(photo=photo)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    qd = query.data
    if qd[0] == 'Ꮎ':
        qd = qd.split('Ꮎ')
        if qd[2][-1] != 'b':
            read_book(qd[1], qd[2], update, context)
        else:
            if qd[2][-2] == 'f':
                base = sqlite3.connect('SMdb.db')
                cur = base.cursor()
                state = "'" + str(qd[2]) + "'"
                newid = "'" + str(qd[1]) + "'"
                text = cur.execute("SELECT rating FROM books where id = " + newid).fetchall()
                keyboard = [
                    [
                        InlineKeyboardButton("Вернуться к списку книг", callback_data='0'),
                    ],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text[0][0], reply_markup=reply_markup)
            else:
                base = sqlite3.connect('SMdb.db')
                cur = base.cursor()
                state = "'" + str(qd[2]) + "'"
                newid = "'" + str(qd[1]) + "'"
                text = cur.execute("SELECT text FROM " + newid + " where state = " + state).fetchall()
                keyboard = [
                    [
                        InlineKeyboardButton("1", callback_data='🥇1' + newid),
                        InlineKeyboardButton("2", callback_data='🥇2' + newid),
                        InlineKeyboardButton("3", callback_data='🥇3' + newid),
                        InlineKeyboardButton("4", callback_data='🥇4' + newid),
                        InlineKeyboardButton("5", callback_data='🥇5' + newid),
                    ],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(text[0][0], reply_markup=reply_markup)
    if qd == '0':
        choose_book(update, context)
    elif qd == '2':
        writing_book(update, context)
    elif qd[0] == '🥇':
        base = sqlite3.connect('SMdb.db')
        cur = base.cursor()
        tex = "SELECT rating FROM books where id = " + qd[2:]
        rat = cur.execute("SELECT rating FROM books where id = " + qd[2:]).fetchall()[0][0]
        rat = rat + ' ' + qd[1]
        tex = "update books set rating = '" + rat + "' where id = " + qd[2:]
        cur.execute(tex)
        base.commit()
        choose_book(update, context)
    else:
        start_read_book(str(qd[0]), update, context)
    query.answer()


def writing_book(new_upd: Update, new_cont: CallbackContext):
    query = new_upd.callback_query
    qd = query.data
    write_book(new_upd, new_cont)


def write_book(new_upd: Update, new_cont: CallbackContext):
    query = new_upd.callback_query
    keyboard = [
        [
            InlineKeyboardButton("Начать написание 1 главы", callback_data='0'),
        ],
    ]
    query.edit_message_text('Написание книги с разветвленным сюжетом - непростой процесс.'
                            'Основа книги - главы. У каждой главы есть варианты продвижения,'
                            ' выбирая которые, читатель переходит на другую главу.'
                            'Поэтому для начала лучше продумать весь сюжет, а затем '
                            'приступать к написанию.')


def choose_book(update: Update, context: CallbackContext):
    query = update.callback_query
    base = sqlite3.connect('SMdb.db')
    cur = base.cursor()
    books = cur.execute('''SELECT name, rating, id FROM books''').fetchall()
    keyboard = []
    namelist = []
    for i in books:
        keyboard.append([InlineKeyboardButton(i[0], callback_data=str(i[2]))])
        rate = sum(list(map(int, i[1].split()))) / len(i[1].split())
        namelist.append(': оценка ⭐️'.join([i[0], str(round(rate, 2))]))
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.answer()
    query.edit_message_text("Доступные книги:\n" + '\n'.join(namelist) + "\nВыберите книгу, которую хотите прочесть",
                            reply_markup=reply_markup)


def start_read_book(book_id, update: Update, context: CallbackContext):
    read_book(book_id, 1, update, context)


def read_book(book_id, state, update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    base = sqlite3.connect('SMdb.db')
    cur = base.cursor()
    state = str(state)
    newid = "'" + str(book_id) + "'"
    text = cur.execute("SELECT text FROM " + newid + " where state = " + state).fetchall()
    var = cur.execute('SELECT vars FROM ' + newid + " where state = " + state).fetchall()
    answers = var[0][0].split('⚡')
    mainkeyboard = []
    for i in answers:
        if len(i.split('✫')) == 2:
            mainkeyboard.append([InlineKeyboardButton(i.split('✫')[0], callback_data=('Ꮎ' + str(book_id) + 'Ꮎ' +
                                                                                      i.split('✫')[1]))])
    reply_markup = InlineKeyboardMarkup(mainkeyboard)
    update.callback_query.message.edit_text(text[0][0], reply_markup=reply_markup)
    query.answer()


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Интерактивные истории")


def main() -> None:
    con = sqlite3.connect("SMdb.db")
    cur = con.cursor()
    a = cur.execute("select name from sqlite_master where type = 'table' and name not like '_all'").fetchall()
    updater = Updater("5214247971:AAF_GJxHw26jfu8A84b8oMiPMSnxFV_3z8w")
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()