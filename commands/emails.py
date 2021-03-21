from implib import *

import modules.keyboards as key
import modules.navigation as nav
import modules.data_access as data


@bot.message_handler(commands=['emails'])
def whats_dep(message):
    nav.delete_all(message.chat.id)
    markup_dep = key.email_dep()
    markup_dep.row("Вихід")
    msg = bot.send_message(
        message.chat.id, "База імейлів викладачів.\nВиберіть кафедру або введіть прізвище.", reply_markup=markup_dep)
    bot.register_next_step_handler(msg, whats_name)


def whats_name(message):
    if message.text == "Вихід":
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "Список доступних команд:" + c.avaiable_comands,
            reply_markup=key_rem,
            parse_mode="Markdown"
        )
    elif message.text in data.emails_deplist():
        nav.upd_edep(message.chat.id, message.text)
        markup_name = key.email_name(message.text)
        markup_name.row("Назад")
        msg = bot.send_message(
            message.chat.id,
            "Виберіть викладача.",
            reply_markup=markup_name
        )
        bot.register_next_step_handler(msg, get_mail)
    elif len(data.search_by_name('%{}%'.format(message.text,))) == 1:
        key_rem = telebot.types.ReplyKeyboardRemove()
        email = data.search_by_name('%{}%'.format(message.text,))
        bot.send_message(
            message.chat.id, email[0][0] + '\n' + email[0][1], reply_markup=key_rem)
    else:
        msg = bot.send_message(
            message.chat.id, "Сформулюйте запит точніше, будь ласка.")
        bot.register_next_step_handler(msg, whats_name)


def get_mail(message):
    if message.text == "Назад":
        whats_dep(message)
    elif message.text in data.emails_namelist(nav.get_edep(message.chat.id)):
        bot.send_chat_action(message.chat.id, 'typing')
        nav.upd_ename(message.chat.id, message.text)
        key_rem = telebot.types.ReplyKeyboardRemove()
        name, dep = nav.get_edata(message.chat.id)
        mail = data.get_email(name, dep)
        nav.del_edata(message.chat.id)
        bot.send_message(message.chat.id, name + " :\n" +
                         mail, reply_markup=key_rem)
    else:
        msg = bot.send_message(
            message.chat.id, "Виберіть викладача зі списку, будь ласка!")
        bot.register_next_step_handler(msg, get_mail)

