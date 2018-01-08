import shelve
from config import shelve_name, shelve_name_field
from telebot import types
import sqlite3
def set_user_load(chat_id,user_id,r): # Юрик добарь коммент, я туплю
    with shelve.open(shelve_name) as storage:
        """
        ключу id чата и id пользователя ставится в соответствие статус загрузки аудио
        """
        storage[str(chat_id)+str(user_id)] = [True,r] 
def game_chek(message): # Юрик добарь коммент, я туплю
    with shelve.open(shelve_name) as storage:
        return str(message.chat.id)+str(message.from_user.id) in storage.keys()

def print_xyz():
    return 'xyz'

def generate_markup():
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    list_items = ['плейлист','исполнитель','название','теги','ой все'] 
    # Заполняем разметку элементами
    for item in list_items:
        markup.add(item)
    return markup

def finish_user_game(chat_id,user_id):
    """
    Нужно внести в БД запись о результате пользователя
    """
    
    """
    Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    :param chat_id: id юзера
    """
    try:
        with shelve.open(shelve_name) as storage:
            del storage[str(chat_id)+str(user_id)]
    except:
        pass
    try:
        with shelve.open(shelve_name_field) as storage:
            del storage[str(chat_id)+str(user_id)]
    except:
        pass
def put_describe(text, ):
    return None


def check_field(message):
    with shelve.open(shelve_name) as storage:
        try:
            #print (storage[str(message.chat.id)+str(message.from_user.id)][1].values())
            return(True in storage[str(message.chat.id)+str(message.from_user.id)][1].values())
        except:
            return False
        
def insert(db,row):
    #print('''INSERT INTO all_music_list VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')'''.format(row['autor'], row['performer'], row['song'], row['style'], row['album'], row['year'], row['text'], row['music'], row['id_telegram'], row['playlist'], row['tags'], row['user']))
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO all_music_list VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')'''.format(row['autor'], row['performer'], row['song'], row['style'], row['album'], row['year'], row['text'], row['music'], row['id_telegram'], row['playlist'], row['tags'], row['user']))
    conn.commit()
    conn.close()
