from implib import *

import modules.keyboards as key
import modules.navigation as nav
import modules.data_access as data

@bot.message_handler(commands=['library'])
def lib_start(message):
    nav.delete_all(message.chat.id)
    markup_years = key.lib_years(message.chat.id)
    markup_years.row('Вихід')
    msg = bot.send_message(
        message.chat.id,
        "Архів літератури.\nБудь ласка, оберіть розділ/файл.",
        reply_markup=markup_years
    )
    bot.register_next_step_handler(msg, lib_year)


def lib_year(message):
    if message.text == "Вихід":
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "Список доступних команд:" + c.avaiable_comands,
            reply_markup=key_rem,
            parse_mode="Markdown"
        )
    elif message.text == "Отримати літературу":
        names = nav.libGetChoosed(message.chat.id)
        key_rem = telebot.types.ReplyKeyboardRemove()
        for name in names:
            link = data.get_book(name)[0]
            bot.send_document(message.chat.id, link, reply_markup=key_rem)
    elif message.text not in [k[0] for k in data.get_lib_years()]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, lib_year)
    else:
        nav.libSetYear(message.chat.id, message.text)
        markup_lessons = key.lib_lessons(message.text, message.chat.id)
        markup_lessons.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Оберіть розділ/файл.",
            reply_markup=markup_lessons
        )
        bot.register_next_step_handler(msg, lib_lesson)


def lib_lesson(message):
    if message.text == "Назад":
        markup_years = key.lib_years(message.chat.id)
        markup_years.row('Вихід')
        msg = bot.send_message(
            message.chat.id,
            "Архів літератури.\nБудь ласка, оберіть розділ/файл.",
            reply_markup=markup_years
        )
        bot.register_next_step_handler(msg, lib_year)
    elif message.text == "Отримати літературу":
        names = nav.libGetChoosed(message.chat.id)
        key_rem = telebot.types.ReplyKeyboardRemove()
        for name in names:
            link = data.get_book(name)[0]
            bot.send_document(message.chat.id, link, reply_markup=key_rem)
    elif message.text not in [k[0] for k in data.get_lib_lessons(nav.libGetYear(message.chat.id))]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, lib_lesson)
    else:
        nav.libSetLesson(message.chat.id, message.text)
        markup_aus = key.lib_aus(nav.libGetYear(
            message.chat.id), message.text, message.chat.id)
        markup_aus.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Оберіть розділ/файл.",
            reply_markup=markup_aus
        )
        bot.register_next_step_handler(msg, lib_aus)


def lib_aus(message):
    if message.text == "Назад":
        markup_lessons = key.lib_lessons(
            nav.libGetYear(message.chat.id), message.chat.id)
        markup_lessons.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть розділ/файл.",
            reply_markup=markup_lessons
        )
        bot.register_next_step_handler(msg, lib_lesson)
    elif message.text == "Отримати літературу":
        names = nav.libGetChoosed(message.chat.id)
        key_rem = telebot.types.ReplyKeyboardRemove()
        for name in names:
            link = data.get_book(name)[0]
            bot.send_document(message.chat.id, link, reply_markup=key_rem)
    elif message.text not in [k[0] for k in data.get_lib_aus(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id))[0]] + [k[0] for k in data.get_lib_aus(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id))[1]]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, lib_aus)
    else:
        if message.text in [k[0] for k in data.get_lib_aus(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id))[1]]:
            nav.libUpdChoosed(message.chat.id, message.text)
            markup_aus = key.lib_aus(nav.libGetYear(
                message.chat.id), nav.libGetLesson(message.chat.id), message.chat.id)
            markup_aus.row('Назад')
            msg = bot.send_message(
                message.chat.id,
                "Файл додано до списку.",
                reply_markup=markup_aus
            )
            bot.register_next_step_handler(msg, lib_aus)
        else:
            nav.libSetAus(message.chat.id, message.text)
            markup_files = key.lib_files(nav.libGetYear(message.chat.id), nav.libGetLesson(
                message.chat.id), message.text, message.chat.id)
            markup_files.row('Назад')
            msg = bot.send_message(
                message.chat.id,
                "Будь ласка, оберіть розділ/файл.",
                reply_markup=markup_files
            )
            bot.register_next_step_handler(msg, lib_finally)


def lib_finally(message):
    if message.text == "Назад":
        markup_aus = key.lib_aus(nav.libGetYear(
            message.chat.id), nav.libGetLesson(message.chat.id), message.chat.id)
        markup_aus.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть розділ/файл.",
            reply_markup=markup_aus
        )
        bot.register_next_step_handler(msg, lib_aus)
    elif message.text == "Отримати літературу":
        names = nav.libGetChoosed(message.chat.id)
        key_rem = telebot.types.ReplyKeyboardRemove()
        for name in names:
            link = data.get_book(name)[0]
            bot.send_document(message.chat.id, link, reply_markup=key_rem)
    elif message.text not in [k[0] for k in data.get_lib_names(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id), nav.libGetAus(message.chat.id))]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, lib_finally)
    else:
        nav.libUpdChoosed(message.chat.id, message.text)
        markup_files = key.lib_files(nav.libGetYear(message.chat.id), nav.libGetLesson(
            message.chat.id), nav.libGetAus(message.chat.id), message.chat.id)
        markup_files.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Файл додано до списку.",
            reply_markup=markup_files
        )
        bot.register_next_step_handler(msg, lib_finally)