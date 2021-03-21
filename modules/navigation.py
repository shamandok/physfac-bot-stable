from config import *
import json
import os
import shelve as sh


def delete_all(chat_id):
    with sh.open(shelve_name) as storage:
        keys = list(storage.keys())
        todel = [key for key in keys if str(chat_id) in key]
        for key in todel:
            del storage[key]

# ------------------SCHEDULE----------------------------------

def update_schedule_path(chat_id,repository):
    with sh.open(shelve_name) as storage:
        try:
            cur_path = storage['sch'+str(chat_id)]
            storage['sch'+str(chat_id)] = cur_path + '/' + repository
        except KeyError:
            storage['sch'+str(chat_id)] = repository

def replace_schedule_path(chat_id, path):
    with sh.open(shelve_name) as storage:
        storage['sch'+str(chat_id)] = path

def del_schedule_path(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            del storage['sch'+str(chat_id)]
        except KeyError:
            pass

def get_schedule_path(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            return storage['sch'+str(chat_id)]
        except KeyError:
            return None

def schedule_step_back(chat_id):
    cur_path = get_schedule_path(chat_id)
    new_path = os.path.split(cur_path)[0]
    replace_schedule_path(chat_id, new_path)


# ---------------EMAILS-----------------------------

def upd_ename(chat_id, name):
    with sh.open(shelve_name) as storage:
            storage['ename'+str(chat_id)] = name

def upd_edep(chat_id, dep):
    with sh.open(shelve_name) as storage:
            storage['edep'+str(chat_id)] = dep

def del_edata(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            del storage['ename'+str(chat_id)]
            del storage['edep'+str(chat_id)]
        except KeyError:
            pass

def get_edep(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            dep = storage['edep'+str(chat_id)]
            return dep
        except KeyError:
            return None

def get_edata(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            name = storage['ename'+str(chat_id)]
            dep = storage['edep'+str(chat_id)]
            return (name, dep)
        except KeyError:
            return None


# ---------------LIBRARY-----------------------------
def libUpdName(chat_id, name):
    with sh.open(shelve_name) as storage:
        try:
            names = json.loads(storage['lib_n'+str(chat_id)])
            names.append(name)
            storage['lib_n'+str(chat_id)] = json.dumps(names)
        except KeyError:
            storage['lib_n'+str(chat_id)] = json.dumps([name])

def libUpdLink(chat_id, link):
    with sh.open(shelve_name) as storage:
        try:
            links = json.loads(storage['lib_link'+str(chat_id)])
            links.append(link)
            storage['lib_link'+str(chat_id)] = json.dumps(links)
        except KeyError:
            storage['lib_link'+str(chat_id)] = json.dumps([link])

def libSetYear(chat_id, year):
    with sh.open(shelve_name) as storage:
        storage['lib_y'+str(chat_id)] = year

def libSetLesson(chat_id, lesson):
    with sh.open(shelve_name) as storage:
        storage['lib_l'+str(chat_id)] = lesson

def libSetAus(chat_id, aus):
    with sh.open(shelve_name) as storage:
        storage['lib_a'+str(chat_id)] = aus

def libGetYear(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            return storage['lib_y'+str(chat_id)]
        except KeyError:
            return None

def libGetLesson(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            return storage['lib_l'+str(chat_id)]
        except KeyError:
            return None

def libGetAus(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            return storage['lib_a'+str(chat_id)]
        except KeyError:
            return None

def libGetAll(chat_id):
    with sh.open(shelve_name) as storage:
        names = json.loads(storage['lib_n'+str(chat_id)])
        links = json.loads(storage['lib_link'+str(chat_id)])
        year = storage['lib_y'+str(chat_id)]
        lesson = storage['lib_l'+str(chat_id)]
        aus = storage['lib_a'+str(chat_id)]
        return [names, links, year, lesson, aus]

def libUpdChoosed(chat_id, bookname):
    with sh.open(shelve_name) as storage:
        try:
            names = json.loads(storage['lib_ch'+str(chat_id)])
            names.append(bookname)
            storage['lib_ch'+str(chat_id)] = json.dumps(names)
        except KeyError:
            storage['lib_ch'+str(chat_id)] = json.dumps([bookname])

def libGetChoosed(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            return json.loads(storage['lib_ch'+str(chat_id)])
        except KeyError:
            return []


# -------------OTHER--------------------------------
def qmm_setsem(chat_id, sem):
    with sh.open(shelve_name) as storage:
        storage['qmmsem'+str(chat_id)] = sem

def qmm_getsem(chat_id):
    with sh.open(shelve_name) as storage:
        try:
            return storage['qmmsem'+str(chat_id)]
        except KeyError:
            return []
