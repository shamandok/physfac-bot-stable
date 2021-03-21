from implib import *

import modules.keyboards as key
import modules.navigation as nav
import modules.minka as minka
import modules.help_functions as help
import modules.data_access as data
import os


@bot.message_handler(commands=['other'])
def other_comands(message):
    msg = "*Інші команди*:\n" + c.other_comands
    bot.send_message(
        message.chat.id,
        msg,
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['qmminka'])
def qmminka_start(message):
    reply = key.minkasem_key()
    bot.send_message(
        message.chat.id, 'Мінка з КМ. Оберіть семестр.', reply_markup=reply)
    bot.register_next_step_handler(message, qmminka)

def qmminka(message):
    if message.text != 'Хватє' and message.text != 'Ще питання':
        nav.qmm_setsem(message.chat.id, message.text)
    if message.text == 'Хватє':
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id, 'Окей, удачі на мінці!', reply_markup=key_rem)
        bot.send_sticker(message.chat.id, 'CAADAgADaQADrKqGF8Qij6L82sPwAg')
    else:
        sem = nav.qmm_getsem(message.chat.id)
        reply = key.minka_key()
        que = minka.get_qm_question(sem)
        bot.send_message(message.chat.id, que, reply_markup=reply)
        bot.register_next_step_handler(message, qmminka)

@bot.message_handler(commands=['ttclinic'])
def ttpolyclinic(message):
    bot.send_message(message.chat.id, "Розклад роботи поліклініки:")
    files = os.listdir(clinic_sch_path)
    opened_files = []
    for file in files:
        opened_files.append(
            open(clinic_sch_path + file, 'rb')
        )
    input_media = [InputMediaPhoto(file) for file in opened_files]
    bot.send_media_group(message.chat.id, input_media)
    for file in opened_files:
        file.close()
    msg_text = "Останнє оновлення розкладу: " + c.last_polyclinic_photos
    bot.send_message(message.chat.id, msg_text)


@bot.message_handler(commands=['ttsport'])
def ttsport(message):
    markup = key.sport_sch_key()
    bot.send_message(message.chat.id,
                     "Розклад роботи секцій спорткомплексу. Будь ласка, оберіть секцію.",
                     reply_markup=markup)
    bot.register_next_step_handler(message, send_sport_shchedule)


def send_sport_shchedule(message):
    if message.text in help.get_sport_files():
        key_rem = telebot.types.ReplyKeyboardRemove()
        schedule = open(sport_sch_path + message.text + '.jpg', 'rb')
        bot.send_photo(
            message.chat.id,
            schedule,
            reply_markup=key_rem
        )
        bot.send_message(
            message.chat.id, "Останнє оновлення розкладу: " + c.last_sport_photos)
    else:
        bot.send_message(
            message.chat.id, "Будь ласка, оберіть варіант зі списку.")
        bot.register_next_step_handler(message, send_sport_shchedule)


@bot.message_handler(commands=['nord'])
def nord(message):
    is_num = data.get_nord()
    if is_num:
        bot.send_message(message.chat.id, "Цього тижня - чисельник.")
    else:
        bot.send_message(message.chat.id, "Цього тижня - знаменник.")

@bot.message_handler(commands=['plasminka'])
def plasminka_start(message):
    bot.send_message(
        message.chat.id, 'Мінка по формулах з предмету "Фізика плазми."')
    plasminka(message)

def plasminka(message):
    if message.text == 'Хватє':
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id, 'Окей, удачі на мінці!', reply_markup=key_rem)
    else:
        reply = key.minka_key()
        que = minka.get_plasma_question()
        bot.send_message(message.chat.id, que, reply_markup=reply)
        bot.register_next_step_handler(message, plasminka)

@bot.message_handler(commands=['edminka'])
def edminka_start(message):
    msg = bot.send_message(
        message.chat.id,
        "Мінка до екзамену з електродинаміки.\n\nСписок питань підготувала @cassini22."
    )
    edminka(msg)

def edminka(message):
    if message.text == 'Хватє':
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id, 'Окей, удачі на мінці!', reply_markup=key_rem)
        bot.send_sticker(message.chat.id, 'CAADAgADhwADrKqGF2eV6us-DDCBFgQ')
    else:
        reply = key.minka_key()
        que = minka.get_eldyn_question()
        bot.send_message(message.chat.id, que, reply_markup=reply, parse_mode="Markdown")
        bot.register_next_step_handler(message, edminka)

@bot.message_handler(commands=['exams'])
def exams_start(message):
    exams_path = 'local_data/session_sch/'
    files = [x[:-4] for x in os.listdir(exams_path)]
    files.sort()
    files.sort(key=len)
    rep_key = key.custom_key(files)
    bot.send_message(
        message.chat.id,
        'Розклад екзаменаційної сесії.\nБудь ласка, оберіть курс.',
        reply_markup=rep_key
    )
    bot.register_next_step_handler(message, lambda x: exams(x, files))

def exams(message, files):
    if message.text not in files:
        rep_key = key.key.custom_key(files)
        bot.send_message(
            message.chat.id,
            'Будь ласка, оберіть варіант зі списку.',
            reply_markup=rep_key
        )
        bot.register_next_step_handler(message, exams)
    else:
        exams_path = 'local_data/session_sch/'
        with open(exams_path + message.text + '.pdf', 'rb') as file:
            key_rem = telebot.types.ReplyKeyboardRemove()
            bot.send_document(message.chat.id, file, reply_markup=key_rem)


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    data.news_unsubscribe(message.chat.id)
    bot.send_message(
        message.chat.id,
        "Ви відписались від новин.\nДля повторної підписки використайте команду /subscribe."
    )

@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    data.news_subscribe(message.chat.id)
    bot.send_message(
        message.chat.id,
        "Ви підписались на новини.\nДля відписки використайте команду /unsubscribe."
    )

@bot.message_handler(commands=['schdoc'])
def schdoc(message):
    bot.send_document(message.chat.id, open(c.sch_doc_path, 'rb'))