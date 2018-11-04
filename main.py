from telegram import  ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import constants, base_work
import logging
import calendar
import time
from datetime import date, timedelta
delete_b = add_b = licension = day_id = admin_add = delete_admin = False
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token=constants.token)

dispatcher = updater.dispatcher

job_queue = updater.job_queue


def start(bot, update):
    message = update.message
    if message.chat.type == 'private' and message.chat.id in base_work.collect_All_id():
        bottons = [['Посмотреть слова', 'Удалить слова'], ['Добавить слово']]
        if  message.chat.id in constants.main_admins:
            bottons1 = [['Выдать лицензию', 'Добавить админа'], ['Список Админов', 'Удалить Админа', 'Дополнительно'] ]
        else: bottons1 = []
        user_markup = ReplyKeyboardMarkup(bottons + bottons1)
        bot.send_message(message.chat.id, 'Здравствуй, админ!', reply_markup=user_markup)
    elif message.chat.type != 'group':
        bot.send_message(message.chat.id, str(message.chat.id))
        for i in constants.main_admins:
            try:
                bot.send_message(i, str(message.chat.id))
            except:
                pass
    elif message.chat.type == 'group' and message.from_user.id in base_work.collect_All_id():
        base_work.add_group(message.from_user.id, message.chat.title)
    else:
        print(message)
    bot.send_message(message.chat.id, constants.hello_text)

def answer(bot, update):
    global delete_b, add_b, licension, datet, day_id, admin_add, delete_admin
    message = update.message
    if message.chat.type  == 'group':
        text1 = message.text.lower().split()
        text2 = base_work.collect_All_words()
        ai = []
        ai2 = []
        for i in text1:
            if i in text2:
                ai = base_work.all_about_all(i)
                for j in ai:
                    if  not j in ai2:
                        bot.forward_message(chat_id=j, from_chat_id=message.chat.id, message_id=message.message_id)
                ai2 = ai
                ai = []

    elif message.text ==  'Дополнительно' and message.chat.id in constants.main_admins:
        bottons = [['Все слова в базе данных', 'Группы/Слова', 'Лицензии'], ['Назад']]
        user_markup = ReplyKeyboardMarkup(bottons)
        bot.send_message(message.chat.id, 'Дополнительно', reply_markup=user_markup)
    elif message.text == 'Все слова в базе данных' and message.chat.id in constants.main_admins:
        all_words = base_work.collect_All_words()
        word = ''
        for i in all_words:
            word += i + '\n'
        bot.send_message(message.chat.id, word)
    elif message.text == 'Посмотреть слова' and  message.chat.id in base_work.collect_All_id():
        try:
            words = base_work.collect_words(message.chat.id)
            word = ''
            for  i in words:
                word += i + '\n'
            bot.send_message(message.chat.id, word)
        except:
            bot.send_message(message.chat.id, 'У вас нет пока что слов')
    elif message.text == 'Удалить слова' and message.chat.id in base_work.collect_All_id():
        bottons = [['Назад']]
        user_markup = ReplyKeyboardMarkup(bottons)
        bot.send_message(message.chat.id, 'Напишите слово, которое хотите удалить', reply_markup=user_markup)
        delete_b = True
    elif delete_b == True:
        delete_b = False
        if message.text == 'Назад':
            update.message.text = 'Назад'
            answer(bot, update)
        else:
            base_work.delete_words(message.chat.id, message.text.lower())
            bot.send_message(message.chat.id, 'Слово "'+ message.text+'" удалено')
            update.message.text = 'Назад'
            answer(bot, update)
    elif  message.text == 'Добавить слово' and message.chat.id in base_work.collect_All_id():
        bottons = [['Назад']]
        user_markup = ReplyKeyboardMarkup(bottons)
        bot.send_message(message.chat.id, 'Напишите слово, которое хотите добавить', reply_markup=user_markup)
        add_b = True
    elif add_b == True:
        add_b = False
        if message.text == 'Назад':
            update.message.text = 'Назад'
            answer(bot, update)
        else:
            base_work.add_words(message.chat.id, message.text.lower())
            bot.send_message(message.chat.id, 'Слово "' + message.text + '" добавлено')
            update.message.text = 'Назад'
            answer(bot, update)
    elif message.text == 'Список Админов' and message.chat.id in constants.main_admins:
        ids = base_work.collect_All_id()
        word = ''
        for i in ids:
            word += str(i) + '\n'
        bot.send_message(message.chat.id, word)
    elif message.text == 'Добавить админа' and message.chat.id in constants.main_admins:
        admin_add = True
        bottons = [['Назад']]
        user_markup = ReplyKeyboardMarkup(bottons)
        bot.send_message(message.chat.id, 'Напишите, id пользователя, чтобы добавить его в список админов', reply_markup=user_markup)
    elif admin_add == True:
        admin_add = False
        if message.text == 'Назад':
            update.message.text = 'Назад'
            answer(bot, update)
        else:
            try:
                base_work.add_id(message.text)
                bot.send_message(message.chat.id, 'Админ добавлен, если хотите посмотреть список всех админов, нажмите "Список Админов"')
                update.message.text = 'Назад'
                answer(bot, update)
            except:
                bot.send_message(message.chat.id, 'Что-то пошло не так. Проверьте правильность написания id')
                update.message.text = 'Назад'
                answer(bot, update)
    elif message.text == 'Удалить Админа' and message.chat.id in constants.main_admins:
        delete_admin = True
        bottons = [['Назад']]
        user_markup = ReplyKeyboardMarkup(bottons)
        bot.send_message(message.chat.id, 'Напишите id админа', reply_markup=user_markup)
    elif delete_admin == True:
        delete_admin = False
        if message.text == 'Назад':
            update.message.text = 'Назад'
            answer(bot, update)
        else:
            try:
                base_work.delete_id(int(message.text))
                bot.send_message(message.chat.id, 'Вы удалили админа')
                update.message.text = 'Назад'
                answer(bot, update)
            except:
                bot.send_message(message.chat.id,'Что-то пошло не так')
                update.message.text = 'Назад'
                answer(bot, update)
    elif message.text == 'Выдать лицензию' and message.chat.id in constants.main_admins:
        bot.send_message(message.chat.id, 'Напишите, на сколько вы хотите выдать лицензию,в формате:')
        bot.send_message(message.chat.id, '1 месяц' )
        bot.send_message(message.chat.id, '2 года')
        bottons = [['Навсегда'],['Назад']]
        user_markup = ReplyKeyboardMarkup(bottons)
        bot.send_message(message.chat.id, 'Или нажмите на кнопку "Навсегда"', reply_markup=user_markup)
        licension = True
    elif licension == True:
        licension = False
        if message.text == 'Назад':
            update.message.text = 'Назад'
            answer(bot, update)
        elif message.text == 'Навсегда':
            datet = 0
            bot.send_message(message.chat.id, 'Выберите id')
            day_id = True
        else:
            text = message.text.split()
            today = date.today()
            if text[1] == 'месяц' or text[1] == 'месяца' or text[1] == 'месяцев':
                days = int(text[0])*31
                datet = today + timedelta(days=days)
                bot.send_message(message.chat.id, 'Выберите id')
                day_id = True
            elif text[1] == 'год' or text[1] == 'года' or text[1] == 'лет':
                days = int(text[0])*31*12
                datet = today + timedelta(days=days)
                bot.send_message(message.chat.id, 'Выберите id')
                day_id = True
            else:
                bot.send_message(message.chat.id, 'Проверьте правильность написания промежутка')
                update.message.text = 'Назад'
                answer(bot, update)
    elif day_id == True:
        day_id = False
        try:
            base_work.incert_date(int(message.text), datet)
            bot.send_message(message.chat.id, 'Изменения добавлены')
            update.message.text = 'Назад'
            answer(bot, update)
        except:
            bot.send_message(message.chat.id, 'Проверьте правильность написания id')
            update.message.text = 'Назад'
            answer(bot, update)
    elif message.text == 'Назад':
        bottons = [['Посмотреть слова', 'Удалить слова'], ['Добавить слово']]
        if message.chat.id in constants.main_admins:
            bottons1 = [['Выдать лицензию','Добавить админа'], ['Список Админов', 'Удалить Админа', 'Дополнительно'] ]
        else:
            bottons1 = []
        user_markup = ReplyKeyboardMarkup(bottons + bottons1)
        bot.send_message(message.chat.id, 'Чем еще могу помочь?', reply_markup=user_markup)
    elif message.text == 'Лицензии' and message.chat.id in constants.main_admins:
        lic = base_work.all_licience()
        bot.send_message(message.chat.id, 'Тут будет написано, до какого действует лицензия, в формате ID / Date')
        line = ''
        for i in lic:
            line += str(i[0]) + ' / '
            if i[1] == 0:
                line += 'Навсегда' + '\n'
            else:
                line += str(i[1]) + '\n'
        bot.send_message(message.chat.id, line)
    elif message.text == 'Группы/Слова' and message.chat.id in constants.main_admins:
        lic = base_work.all_groups()
        bot.send_message(message.chat.id, 'Тут будут выведены все группы и слова админов, в формате ID/ Group/ Words')
        line = ''
        for i in lic:
            line += str(i[0]) + ' / ' + str(i[1])[:-1] + ' / ' +str(i[2])+ '\n'
        bot.send_message(message.chat.id, line)



def chek_time():
    pass



start_handler = CommandHandler('start', start)
answer_handler = MessageHandler(Filters.text, answer)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(answer_handler)
updater.start_polling(clean=True, timeout=5 )