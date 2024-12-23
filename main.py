import telebot
from telebot import types
import psycopg2
from config import host, user, password, db_name, TOKEN

bot = telebot.TeleBot(TOKEN)

#CONNECT
connection = psycopg2.connect(
   host = host,
   user = user,
   password = password,
   database = db_name
)


def checkQuestionInDB(user_question):
    try: 
        with connection.cursor() as cursor: 
            cursor.execute("SELECT COUNT(*) FROM questiontest WHERE answer = %s;", (user_question,))
            count = cursor.fetchone()[0]
            return count > 0  
    except Exception as _ex: 
        print("[INFO] Error while working with PostgreSQL", _ex) 
        return False  



@bot.message_handler(commands=['start'])
def main(message):
    bot.delete_message(message.chat.id, message.id)
    send_menu(message)




last_menu_messages = {}

def send_menu(message):
    global last_menu_messages 

    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='Ответы на FAQ', callback_data='btn1')
    btn2 = types.InlineKeyboardButton(text='Задать вопрос', callback_data='btn2')
    # btn3 = types.InlineKeyboardButton(text='Кнопка 3', callback_data='btn3')
    btn4 = types.InlineKeyboardButton(text='Установить приложение ЭТРАН', callback_data='btn4',
                                      url="https://ozd-center.ru/cat/help/etran/install")
    btn5 = types.InlineKeyboardButton(text='Тех.поддержка', callback_data='btnTp', url="https://t.me/phyphloran")
    
    kb.add(btn1, btn2, btn4, btn5)

    pic = open('menu.jpeg', 'rb')

    if message.chat.id in last_menu_messages:
        try:
            bot.delete_message(message.chat.id, last_menu_messages[message.chat.id])
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
    last_menu_message = bot.send_photo(message.chat.id, pic, f'Здравствуйте, {message.from_user.first_name}! Выберите функцию.', reply_markup=kb)
    last_menu_messages[message.chat.id] = last_menu_message.message_id


@bot.message_handler(func=lambda message: message.text == "Перезапуск")
def restart_message(message):
    send_menu(message)

user_questions = {}
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'btn1':
            kb1 = types.InlineKeyboardMarkup(row_width=1)
            btn11 = types.InlineKeyboardButton(text='Что такое ЭТРАН?', callback_data='btn11')
            btn12 = types.InlineKeyboardButton(text='Можно ли интегрировать ЭТРАН с др. системами учёта?', callback_data='btn12')
            btn13 = types.InlineKeyboardButton(text='Как создать электронную транспортную накладную?', callback_data='btn13')
            btn14 = types.InlineKeyboardButton(text='Что такое ЭТРАН и какие задачи он решает?', callback_data='btn14')
            btn15 = types.InlineKeyboardButton(text='Имеют ли документы в ЭТРАН юридическую силу?', callback_data='btn15')
            btnBack = types.InlineKeyboardButton(text='⭠ Назад', callback_data='btnBack')

            kb1.add(btn11, btn12, btn13, btn14, btn15, btnBack)

            pic1 = open('podmenu1.jpeg', 'rb')
            
            bot.edit_message_media(
                chat_id=call.message.chat.id, 
                message_id=call.message.message_id,
                media=types.InputMediaPhoto(pic1), 
            )
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=kb1)


        elif call.data == 'btn11': 
            try: 
                with connection.cursor() as cursor: 
                    cursor.execute("SELECT answer FROM Answers WHERE id = '1';") 
                    res = cursor.fetchone()             
                    if res: 
                        kbBack = types.InlineKeyboardMarkup(row_width=1)
                        btnOnlyBack = types.InlineKeyboardButton(text='Очистить', callback_data='btnOnlyBack')
                        kbBack.add(btnOnlyBack)
                        bot.send_message(call.message.chat.id, res[0], reply_markup=kbBack) 
                    else:
                        bot.send_message(call.message.chat.id, "Ответ не найден.")  
            except Exception as _ex: 
                print("[INFO] Error while working with PostgreSQL", _ex) 
                bot.send_message(call.message.chat.id, "Произошла ошибка при обращении к базе данных.")
        elif call.data == 'btn12': 
            try: 
                with connection.cursor() as cursor: 
                    cursor.execute("SELECT answer FROM Answers WHERE id = '2';") 
                    res = cursor.fetchone()             
                    if res: 
                        kbBack = types.InlineKeyboardMarkup(row_width=1)
                        btnOnlyBack = types.InlineKeyboardButton(text='Очистить', callback_data='btnOnlyBack')
                        kbBack.add(btnOnlyBack)
                        bot.send_message(call.message.chat.id, res[0], reply_markup=kbBack) 
                    else:
                        bot.send_message(call.message.chat.id, "Ответ не найден.")  
            except Exception as _ex: 
                print("[INFO] Error while working with PostgreSQL", _ex) 
                bot.send_message(call.message.chat.id, "Произошла ошибка при обращении к базе данных.")


        elif call.data == 'btn2': 
            bot.send_message(call.message.chat.id, "Пришлите ваш вопрос")
            user_questions[call.message.chat.id] = None
                
        elif call.data == 'btn13': 
            try: 
                with connection.cursor() as cursor: 
                    cursor.execute("SELECT answer FROM Answers WHERE id = '3';") 
                    res = cursor.fetchone()            
                    if res: 
                        kbBack = types.InlineKeyboardMarkup(row_width=1)
                        btnOnlyBack = types.InlineKeyboardButton(text='Очистить', callback_data='btnOnlyBack')
                        kbBack.add(btnOnlyBack)
                        bot.send_message(call.message.chat.id, res[0], reply_markup=kbBack) 
                    else:
                        bot.send_message(call.message.chat.id, "Ответ не найден.")  
            except Exception as _ex: 
                print("[INFO] Error while working with PostgreSQL", _ex) 
                bot.send_message(call.message.chat.id, "Произошла ошибка при обращении к базе данных.")
        elif call.data == 'btn14': 
            try: 
                with connection.cursor() as cursor: 
                    cursor.execute("SELECT answer FROM Answers WHERE id = '4';") 
                    res = cursor.fetchone()
                    if res: 
                        kbBack = types.InlineKeyboardMarkup(row_width=1)
                        btnOnlyBack = types.InlineKeyboardButton(text='Очистить', callback_data='btnOnlyBack')
                        kbBack.add(btnOnlyBack)
                        bot.send_message(call.message.chat.id, res[0], reply_markup=kbBack) 
                    else:
                        bot.send_message(call.message.chat.id, "Ответ не найден.")  
            except Exception as _ex: 
                print("[INFO] Error while working with PostgreSQL", _ex) 
                bot.send_message(call.message.chat.id, "Произошла ошибка при обращении к базе данных.")
        elif call.data == 'btn15': 
            try: 
                with connection.cursor() as cursor: 
                    cursor.execute("SELECT answer FROM Answers WHERE id = '5';") 
                    res = cursor.fetchone()
                    if res: 
                        kbBack = types.InlineKeyboardMarkup(row_width=1)
                        btnOnlyBack = types.InlineKeyboardButton(text='Очистить', callback_data='btnOnlyBack')
                        kbBack.add(btnOnlyBack)
                        bot.send_message(call.message.chat.id, res[0], reply_markup=kbBack)  
                    else:
                        bot.send_message(call.message.chat.id, "Ответ не найден.")  
            except Exception as _ex: 
                print("[INFO] Error while working with PostgreSQL", _ex) 
                bot.send_message(call.message.chat.id, "Произошла ошибка при обращении к базе данных.")
        elif call.data == 'btnBack':
            send_menu(call.message)
        elif call.data == 'btnOnlyBack':
            bot.delete_message(call.message.chat.id, call.message.message_id)




@bot.message_handler(func=lambda message: message.chat.id in user_questions and user_questions[message.chat.id] is None)
def handle_question(message):
    user_questions[message.chat.id] = message.text
    
    try:
        with connection.cursor() as cursor:
            if checkQuestionInDB(message.text):  
                print(f"Вопрос от пользователя {message.chat.id}: {message.text}")  
                bot.send_message(message.chat.id, "Данный вопрос уже в обработке!")
            else:
                cursor.execute('INSERT INTO questiontest (answer, Telegramid) VALUES (%s, %s)', (message.text, message.chat.id))
                connection.commit()
                print(f"Вопрос от пользователя {message.chat.id}: {message.text}")  
                bot.send_message(message.chat.id, "Ваш вопрос сохранен!")
    
    except Exception as ex:
        print("[ERROR] Ошибка при обработке вопроса:", ex)
        bot.send_message(message.chat.id, "Произошла ошибка при обработке вашего вопроса.")
        connection.rollback()  
    
    send_menu(message) 


bot.polling(non_stop=True)