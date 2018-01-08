# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import numpy as np
class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        # Получаем все строки
        with self.connection:
            return self.cursor.execute('SELECT * FROM all_music_list').fetchall()

    def select_single(self, rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM all_music_list WHERE row_Num = ?',(rownum,)).fetchall()[0]


    def count_rows(self):
        # Считаем количество строк
        with self.connection:
            result = self.cursor.execute('SELECT * FROM all_music_list').fetchall()
            return len(result)
    def insert(self,row):
        # Добавляем в БД еще одну строку 
        self.cursor.execute('''INSERT INTO all_music_list 
                                   (autor, performer, song, style, album, year, text, music, id_telegram, playlist, tags,user)
                                   VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')'''.format(row['autor'], row['performer'], row['song'], row['style'], row['album'], row['year'], row['text'], row['music'], row['id_telegram'], row['playlist'], row['tags'], row['user']))
        self.connection.commit()

    def random_from_all_db(self):
        # Выбираем случайную строку из всей базы
        q_from_list = self.cursor.execute("SELECT count(*) FROM all_music_list aml").fetchall()[0][0]
        ter = np.random.randint(0,q_from_list)
        return(self.cursor.execute("with l as (SELECT aml.*, (select count(*) from all_music_list b  where aml.id_telegram >= b.id_telegram) as cnt FROM all_music_list aml) select * from l l where l.cnt={0} ".format(ter+1)).fetchall())
        
    def random_from_playlist(self, playlist):
        # Выбираем случайную строку из выбранного плейлиста
        q_from_list = self.cursor.execute("SELECT count(*) FROM all_music_list aml where aml.playlist='{0}'".format(playlist)).fetchall()[0][0]
        ter = np.random.randint(0,q_from_list)
        return(self.cursor.execute("with l as (SELECT aml.*, (select count(*) from all_music_list b  where aml.id_telegram >= b.id_telegram and b.playlist='{0}') as cnt FROM all_music_list aml where aml.playlist='{0}') select * from l l where l.cnt={1} ".format(playlist,ter+1)).fetchall())
       
    def free_reqvest(self, reqvest):
        # функция для выполнения произвольного запроса
        return(self.cursor.execute(reqvest)).fetchall()
    
    def pandas_test(self, reqvest):
        # Пробую забирать таблицы через pandas
        with self.connection as conn:
            result = pd.read_sql(reqvest, conn)
        return (result)
            
    def close(self):
        # Закрываем текущее соединение с БД
        self.connection.close()