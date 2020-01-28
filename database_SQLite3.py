
import sqlite3 as lite
import sys
import datetime
import os
import aiohttp
# from plugin_system import Plugin
# plugin = Plugin("DataBase",
#                 usage=["admin only"])

def split_db_str(string_db):
    input_data = string_db.split(',!,')
    len_inputData = len(input_data)
    arr_strDb_info = []
    arr_strDb_info.append(input_data)
    arr_strDb_info.append(len_inputData)
    return arr_strDb_info

def arr_make(user_id, message):
    global data
    data = (
        (user_id, f'{message}'),
    )
    return data

def update_db(id_user, msg):
    current_str = []
    cur.execute(f"SELECT id_user,data FROM data_msg WHERE id_user={id_user}")
    rows = cur.fetchall()
    for row in rows:
        # print(f'row = {row}')
        current_str.append(row[1])
    current_str = ',!,'.join(current_str)
    answer = current_str + ',!,' + msg
    with con:
        cur.execute(f"UPDATE data_msg SET data='{answer}' WHERE id_user={id_user}")
    # con.commit()

def answer_to_user_in_arr(id_user):
    current_str = []
    cur.execute(f"SELECT id_user,data FROM data_msg WHERE id_user={id_user}")
    rows = cur.fetchall()
    for row in rows:
        # print(f'row = {row}')
        current_str.append(row[1])
    current_str = ',!,'.join(current_str)
    answer = split_db_str(current_str)
    # con.commit()
    return answer

def write2Db(id_user, msg):
    data = arr_make(id_user, msg)
    cur.executemany(f"INSERT INTO data_msg VALUES(?, ?)", data)
    # con.commit()

def print_all():
    with con:
        # cur = con.cursor()
        cur.execute("SELECT * FROM data_msg")
        rows = cur.fetchall()

        for row in rows:
            print(f'row [{row[0]}] = {row[1]}')

def init_db():
    global con, cur
    con = lite.connect('db_words_all.db')
    # cur = con.cursor()
    with con:
        cur = con.cursor()
        # cur.execute("DROP TABLE IF EXISTS data_msg")
        cur.execute("CREATE TABLE IF NOT EXISTS data_msg(id_user INT, data TEXT)")
    cur = con.cursor()

def check_user_in_DB(id_user):
    # print(f' ## id_user = {id_user}')
    current_str = []
    cur.execute(f"SELECT id_user FROM data_msg WHERE id_user={id_user}")
    rows = cur.fetchall()
    # print(f' #######   rows = {rows} + type = {type(rows)}')
    # if rows is []:
    # # if rows is (None or 0):
    #     # con.commit()
    #     print(f' ####### []   rows = {rows} + type = {type(rows)}')
    #     return 'no_user'
    if len(rows) < 1:
        # con.commit()
        # print(f' #######  len(   rows = {rows} + type = {type(rows)}')
        return 'no_user'
    elif len(rows) > 0:
        # print(f' #######  > 0  rows = {rows} + type = {type(rows)}')
        for row in rows:
            # print(f' #######  > 0  row # # = {row} + type = {type(rows)}')
            current_str.append(str(row[0]))
        current_str = ''.join(current_str)
        # con.commit()
        return current_str
    else:
        return f"error"


def drop_db():
    cur.execute("DROP TABLE IF EXISTS data_msg")

def make_db_copy_file():
    global current_data, cur_pos
    global dbFile_pos

    cur_pos = os.getcwd()
    current_data = datetime.datetime.now()
    all_db = []
    data_now = str(current_data.day) + "." + str(current_data.month) + "." + str(current_data.year) + "__" + \
               str(current_data.minute) + "." + str(current_data.hour)
    file_db = open(f'DATABASE_{data_now}.txt', 'w')
    dbFile_pos = rf'{cur_pos}/{data_now}.txt'
    print(dbFile_pos)
    with con:
        # cur = con.cursor()
        cur.execute("SELECT * FROM data_msg")
        rows = cur.fetchall()

        for row in rows:
            all_db.append(row)
            # file_db.write(str(row))
            # print(f'row [{row[0]}] = {row[1]}')
    for i in all_db:
        print(i)
        for ii in i:
            print('###############################')
            print(ii)
            iii = str(ii)
            file_db.write(iii + '\n')
    file_db.close()
    return dbFile_pos


def del_file_copy_of_db():
    os.remove(dbFile_pos)

# @plugin.on_command('выгрузи бд', 'Выгрузи бд')
# async def upload_txt_file(file_pos):
#     file_pos = dbFile_pos
#     upload_method = 'docs.getUploadServer'
#     upload_server = await msg.vk.method(upload_method, {'type': 'doc'})
#     url = upload_server.get('upload_url')
#     if not url:
#         return await msg.answer(FAIL_MSG + '   upload')
#
#     form_data = aiohttp.FormData()
#     form_data.add_field('file', file_pos)
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, data=form_data) as resp:
#             file_url = await resp.json()
#             file = file_url.get('file')
#             if not file:
#                 return await msg.answer(FAIL_MSG + 'NOT_FILE')
#
#     # Сохраняем файл в документы (чтобы можно было прикрепить к сообщению)
#     saved_data = await msg.vk.method('docs.save', {'file': file})
#     if not saved_data:
#         return await msg.answer(FAIL_MSG + '   documents')
#     # Получаем первый элемент, так как мы сохранили 1 файл
#     media = saved_data[0]
#     media_id, owner_id = media['id'], media['owner_id']
#     # Прикрепляем аудио к сообщению :)
#     await msg.answer('', attachment=f'doc{owner_id}_{media_id}')





init_db()




























# import random
# con = lite.connect('db_words_all.db')
# cur = con.cursor()
# cur.execute("CREATE TABLE IF NOT EXISTS data_msg(id_user INT, data TEXT)")
# with con:
#     # cur = con.cursor()
#     # cur.execute("DROP TABLE IF EXISTS data_msg")
#
#

#
# sender_id = 100101
# message = ' pfgbcm 1'
# status_id = check_user_in_DB(sender_id)
# print(f'  ###   Ststus_id = {status_id}')
# if status_id == 'no_user':
#     write2Db(sender_id, message)
# elif status_id == "error":
#     print('Ошибка в распознавании наличия юзера в SQLite3')
# else:
#     if int(status_id) == sender_id:
#         update_db(sender_id, message)
#         chance = 45
#         # chance = random.randint(0, 100)
#         if ((chance < 50) and (chance > 40)) is True:
#             answer_itog = answer_to_user_in_arr(sender_id)
#             random_word_pos = random.randint(0, answer_itog[1] - 1)
#             random_word = answer_itog[0][random_word_pos]
#             print(f'{random_word}')
#     else:
#         print(f'Ошибка в распознавании наличия юзера в SQLite3\n'
#               f'Верефикация пройдена: status_id = {status_id}, sender_id = {sender_id}')
#
# sender_id = 100101
# message = 'cfvgbhjnkbgvfcdxcghjk 1'
# status_id = check_user_in_DB(sender_id)
# print(f'  ###   Ststus_id = {status_id}')
# if status_id == 'no_user':
#     write2Db(sender_id, message)
# elif status_id == "error":
#     print('Ошибка в распознавании наличия юзера в SQLite3')
# else:
#     if int(status_id) == sender_id:
#         update_db(sender_id, message)
#         chance = 45
#         # chance = random.randint(0, 100)
#         if ((chance < 50) and (chance > 40)) is True:
#             answer_itog = answer_to_user_in_arr(sender_id)
#             random_word_pos = random.randint(0, answer_itog[1] - 1)
#             random_word = answer_itog[0][random_word_pos]
#             print(f'{random_word}')
#     else:
#         print(f'Ошибка в распознавании наличия юзера в SQLite3\n'
#               f'Верефикация пройдена: status_id = {status_id}, sender_id = {sender_id}')
# # con.close()
