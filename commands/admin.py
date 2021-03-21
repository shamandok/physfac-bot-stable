from implib import *
import modules.keyboards as key
import modules.navigation as nav
import modules.data_access as data
from telebot.apihelper import ApiException

def check_admin(message):
    if data.check_admin(message.chat.id):
        return True
    else:
        bot.send_message(message.chat.id, "Ви не адмін, сорі.")
        return False

# =========== EMAILS =======================

@bot.message_handler(commands=['del_email'])
def whats_dep_del(message):
    if check_admin(message) == True:
        markup_dep = key.email_dep()
        msg = bot.send_message(
            message.chat.id, "Виберіть, будь ласка, кафедру.", reply_markup=markup_dep)
        bot.register_next_step_handler(msg, whats_name_del)

def whats_name_del(message):
    nav.upd_edep(message.chat.id, message.text)
    markup_name = key.email_name(message.text)
    msg = bot.send_message(
        message.chat.id, "Виберіть, будь ласка, викладача.", reply_markup=markup_name)
    bot.register_next_step_handler(msg, del_mail)

def del_mail(message):
    nav.upd_ename(message.chat.id, message.text)
    name, dep = nav.get_edata(message.chat.id)
    nav.del_edata(message.chat.id)
    data.email_remove(name, dep)
    bot.send_message(message.chat.id, "Видалено!")


@bot.message_handler(commands=['add_email'])
def add_name(message):
    if check_admin(message) == True:
        msg = bot.send_message(
            message.chat.id, "Введіть, будь ласка, прізвище та ініціали.")
        bot.register_next_step_handler(msg, add_dep)

def add_dep(message):
    nav.upd_ename(message.chat.id, message.text)
    markup_dep = key.departments()
    msg = bot.send_message(
        message.chat.id, "Виберіть, будь ласка, кафедру.", reply_markup=markup_dep)
    bot.register_next_step_handler(msg, add_mail)

def add_mail(message):
    key_rem = telebot.types.ReplyKeyboardRemove()
    nav.upd_edep(message.chat.id, message.text)
    msg = bot.send_message(
        message.chat.id, "Введіть, будь ласка, пошту.", reply_markup=key_rem)
    bot.register_next_step_handler(msg, write_mail)

def write_mail(message):
    email = message.text
    name, dep = nav.get_edata(message.chat.id)
    data.add_email(name, dep, email)
    nav.del_edata(message.chat.id)
    bot.send_message(message.chat.id, "Додано!")

# ============== LIBRARY ========================
@bot.message_handler(commands=['add_books'])
def add_book(message):
    if check_admin(message) == True:
        nav.delete_all(message.chat.id)
        msg = bot.send_message(message.chat.id, "Надішліть, будь ласка, файл.")
        bot.register_next_step_handler(msg, add_year)


def add_year(message):
    nav.libUpdLink(message.chat.id, message.document.file_id)
    nav.libUpdName(message.chat.id, message.document.file_name)
    markup_year = key.lib_years(message.chat.id)
    msg = bot.send_message(message.chat.id,
                           "Надішліть ще один файл або ведіть назву первинної директорії (рекомендовано назву курсу)" +
                           " або виберіть зі списку. Якщо файл відноситься до кількох курсів - " +
                           "перелічіть їх через кому (зі списку можна вибрати лише 1 варіант).",
                           reply_markup=markup_year)
    bot.register_next_step_handler(msg, add_lesson)


def add_lesson(message):
    if message.document != None:
        return add_year(message)
    else:
        nav.libSetYear(message.chat.id, message.text)
        markup_lesson = key.lib_lessons(message.text, message.chat.id)
        msg = bot.send_message(message.chat.id,
                               "Введіть вторинну директорію (рекомендовано назву предмету; * якщо відсутні).",
                               reply_markup=markup_lesson)
        bot.register_next_step_handler(msg, add_aus)


def add_aus(message):
    nav.libSetLesson(message.chat.id, message.text)
    markup_aus = key.lib_aus(nav.libGetYear(
        message.chat.id), message.text, message.chat.id)
    msg = bot.send_message(message.chat.id,
                           "Введіть імʼя автора або директорію третього рівня(* якщо відстутні).",
                           reply_markup=markup_aus)
    bot.register_next_step_handler(msg, save_to_lib)


def save_to_lib(message):
    nav.libSetAus(message.chat.id, message.text)
    key_rem = telebot.types.ReplyKeyboardRemove()
    names, links, year, lesson, aus = nav.libGetAll(message.chat.id)
    for i in range(0, len(names)):
        data.add_book(names[i], links[i], year, lesson, aus)
        bot.send_message(message.chat.id,
                         "Збережено!\n" + str(links[i]) + '\n' + str(names[i]) + '\n' + str(
                             year) + '\n' + str(lesson) + '\n' + str(aus),
                         reply_markup=key_rem)


@bot.message_handler(commands=['remove_book'])
def rb_start(message):
    nav.delete_all(message.chat.id)
    if check_admin(message) == True:
        markup_years = key.lib_years(message.chat.id)
        markup_years.row('Вихід')
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть розділ/файл.",
            reply_markup=markup_years
        )
        bot.register_next_step_handler(msg, rb_year)

def rb_year(message):
    if message.text == "Вихід":
        key_rem = telebot.types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "ок",
            reply_markup=key_rem,
            parse_mode="Markdown"
        )
    elif message.text not in [k[0] for k in data.get_lib_years()]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, rb_year)
    else:
        nav.libSetYear(message.chat.id, message.text)
        markup_lessons = key.lib_lessons(message.text, message.chat.id)
        markup_lessons.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Оберіть розділ/файл.",
            reply_markup=markup_lessons
        )
        bot.register_next_step_handler(msg, rb_lesson)


def rb_lesson(message):
    if message.text == "Назад":
        markup_years = key.lib_years(message.chat.id)
        markup_years.row('Вихід')
        msg = bot.send_message(
            message.chat.id,
            "Архів літератури.\nБудь ласка, оберіть розділ/файл.",
            reply_markup=markup_years
        )
        bot.register_next_step_handler(msg, rb_year)

    elif message.text not in [k[0] for k in data.get_lib_lessons(nav.libGetYear(message.chat.id))]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, rb_lesson)
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
        bot.register_next_step_handler(msg, rb_aus)


def rb_aus(message):
    if message.text == "Назад":
        markup_lessons = key.lib_lessons(
            nav.libGetYear(message.chat.id), message.chat.id)
        markup_lessons.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть розділ/файл.",
            reply_markup=markup_lessons
        )
        bot.register_next_step_handler(msg, rb_lesson)
    elif message.text not in [k[0] for k in data.get_lib_aus(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id))[0]] + [k[0] for k in data.get_lib_aus(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id))[1]]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, rb_aus)
    else:
        if message.text in [k[0] for k in data.get_lib_aus(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id))[1]]:
            key_rem = telebot.types.ReplyKeyboardRemove()
            data.del_book(message.text)
            bot.send_message(
                message.chat.id,
                "Файл видалено.",
                reply_markup=key_rem
            )
            nav.delete_all(message.chat.id)
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
            bot.register_next_step_handler(msg, rb_finally)


def rb_finally(message):
    if message.text == "Назад":
        markup_aus = key.lib_aus(nav.libGetYear(
            message.chat.id), nav.libGetLesson(message.chat.id), message.chat.id)
        markup_aus.row('Назад')
        msg = bot.send_message(
            message.chat.id,
            "Будь ласка, оберіть розділ/файл.",
            reply_markup=markup_aus
        )
        bot.register_next_step_handler(msg, rb_aus)
    elif message.text not in [k[0] for k in data.get_lib_names(nav.libGetYear(message.chat.id), nav.libGetLesson(message.chat.id), nav.libGetAus(message.chat.id))]:
        msg = bot.send_message(
            message.chat.id,
            "Оберіть варіант зі списку, будь ласка."
        )
        bot.register_next_step_handler(msg, rb_finally)
    else:
        key_rem = telebot.types.ReplyKeyboardRemove()
        data.del_book(message.text)
        bot.send_message(
            message.chat.id,
            "Файл видалено.",
            reply_markup=key_rem
        )
        nav.delete_all(message.chat.id)

# ========= OTHER ADMIN COMMANDS =============
@bot.message_handler(commands=['setnumerator'])
def setnumerator(message):
    if check_admin(message) == True:
        data.set_numerator()
        bot.send_message(message.chat.id, "Зроблено! Тепер - чисельник.")


@bot.message_handler(commands=['setdenominator'])
def setdenominator(message):
    if check_admin(message) == True:
        data.set_denominator()
        bot.send_message(message.chat.id, "Зроблено! Тепер - знаменник.")


@bot.message_handler(commands=['get_admin'])
def get_admin_start(message):
    bot.send_message(message.chat.id, "Введіть пароль.")
    bot.register_next_step_handler(message, get_admin_end)

def get_admin_end(message):
    if message.text == 'Вихід':
        pass
    elif message.text == data.get_password('get_admin'):
        data.make_admin(message.chat.id)

        if data.check_admin(message.chat.id) == True:
            bot.send_message(message.chat.id, "Успішно!")
        else:
            bot.send_message(message.chat.id, "Щось пішло не так...")

    else:
        bot.send_message(message.chat.id, "Пароль невірний, спробуйте ще, або напишіть 'Вихід'.")
        bot.register_next_step_handler(message, get_admin_end)


@bot.message_handler(commands=['informall'])
def informall_start(message):
    if check_admin(message) == True:
        bot.send_message(message.chat.id, "Будь ласка, введіть повідомлення.")
        bot.register_next_step_handler(message, informall_end)

def informall_end(message):
    ids = data.get_news_chat_ids()
    for id in ids:
        try:
            bot.send_message(
                id[0],
                message.text
            )
        except ApiException:
            pass