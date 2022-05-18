import telebot
from time import sleep
from telebot import types
from threading import Thread
import requests
from plyer.utils import platform
from plyer import notification
import pandas as pd
from datetime import datetime
import pytz

ttz = pytz.timezone('Asia/Tashkent')
day_of_year = datetime.now(tz=ttz).timetuple().tm_yday
rr = ""

botToken = '5271483848:AAF9LHnnvEcxU_93LyBnQ17SPo1Apiz5Dcw'
idim = '764620858'
bot = telebot.TeleBot(botToken)
url = 'https://api.telegram.org/bot' + str(botToken) + '/sendMessage?chat_id='+idim + '&text='


def farq(x1, x2):
    x = datetime.now(tz=ttz)
    y = x.timetuple().tm_yday+1
    yil = x.year
    if x1 > 2 and yil % 4 != 0:
        x2 = x2 + 1
    y2 = 0
    if x1 == 1:
        y2 = x2
    elif x1 == 2:
        y2 = x2 + 31
    elif x1 == 3:
        y2 = x2 + 59
    elif x1 == 4:
        y2 = x2 + 90
    elif x1 == 5:
        y2 = x2 + 120
    elif x1 == 6:
        y2 = x2 + 151
    elif x1 == 7:
        y2 = x2 + 181
    elif x1 == 8:
        y2 = x2 + 212
    elif x1 == 9:
        y2 = x2 + 243
    elif x1 == 10:
        y2 = x2 + 273
    elif x1 == 11:
        y2 = x2 + 304
    elif x1 == 12:
        y2 = x2 + 334
    return y2 - y


def task1():
    while True:
        data = pd.read_excel(r'den.xlsx')

        inps = pd.DataFrame(data, columns=['ИНПС']).values.tolist()
        asosiy = pd.DataFrame(data, columns=["Дата рождения"]).values
        fio = pd.DataFrame(data, columns=['Сотрудник']).values.tolist()
        bolimi = pd.DataFrame(data, columns=["Подразделение организации"]).values.tolist()
        mansabi = pd.DataFrame(data, columns=['Должность']).values.tolist()
        tel = pd.DataFrame(data, columns=['Телефон']).values.tolist()

        for x in range(0, 10):
            for i in range(len(asosiy)):
                dat = str(asosiy[i][0])
                yili = int(dat[:4])
                oyi = int(dat[5:7])
                kuni = int(dat[8:10])
                qoldi = farq(oyi, kuni)
                if qoldi == x:
                    if qoldi == 0:
                        rr = fio[i][0]+ " Отдел " + bolimi[i][0]+ ", " + mansabi[i][0]+ ".\nBugun tugilgan kuni!!!"
                    else:
                        rr = fio[i][0]+ " Отдел "+ bolimi[i][0]+ ", "+ mansabi[i][0]+ "\n"+ str(qoldi)+ " kundan keyin tugilgan kuni. Ehtiyot choralarini ko'ring"
                    #rr = ''.join(rr)
                    notification.notify(
                        title="Tug'ilgan kun",
                        message=rr,
                        app_name='Kun sanagich',
                    )
                    r = requests.get(url+rr)
            sleep(1)

        #webbrowser.open(url)


        sleep(60*60*24)

def task2():
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        id = message.chat.id
        name = message.from_user.first_name
        text = 'Salomlar'
        markup = types.ReplyKeyboardMarkup()
        itembtn1 = types.KeyboardButton('Bugun')
        itembtn2 = types.KeyboardButton('ertaga')
        itembtn3 = types.KeyboardButton('3 kundan keyin')
        itembtn4 = types.KeyboardButton('Shu oy')
        itembtn5 = types.KeyboardButton('Button 5')
        itembtn6 = types.KeyboardButton('Button 6')
        itembtn7 = types.KeyboardButton('/start')
        markup.row(itembtn1, itembtn2, itembtn3)
        markup.row(itembtn4, itembtn5, itembtn6)
        markup.row(itembtn7)
        bot.send_message(message.chat.id, text, reply_markup=markup)

    @bot.message_handler(content_types=["text"])
    def get_information(message):
        txt = message.text.lower()
        if txt.find('salom') != -1:
            bot.send_message(message.chat.id, "Assalomalekum" + message.from_user.first_name + " " + message.from_user.last_name, parse_mode='html')
        elif txt == "bugun":
            bot.send_message(message.chat.id, "Kutib turing. \n Yuklanyapti . . .")
            data = pd.read_excel(r'den.xlsx')

            inps = pd.DataFrame(data, columns=['ИНПС']).values.tolist()
            asosiy = pd.DataFrame(data, columns=["Дата рождения"]).values
            fio = pd.DataFrame(data, columns=['Сотрудник']).values.tolist()
            bolimi = pd.DataFrame(data, columns=["Подразделение организации"]).values.tolist()
            mansabi = pd.DataFrame(data, columns=['Должность']).values.tolist()
            tel = pd.DataFrame(data, columns=['Телефон']).values.tolist()
            bot.send_message(message.chat.id, "\nBugungi tug'ilgan kunlar:")

            for i in range(len(asosiy)):
                dat = str(asosiy[i][0])
                yili = int(dat[:4])
                oyi = int(dat[5:7])
                kuni = int(dat[8:10])
                qoldi = farq(oyi, kuni)
                if qoldi == 0:
                    rr = fio[i][0] + " Отдел " + bolimi[i][0] + ", " + mansabi[i][0] + ".\n"
                    r = requests.get(url + rr)
        elif txt == "ertaga":
            bot.send_message(message.chat.id, "Kutib turing. \n Yuklanyapti")
            data = pd.read_excel(r'den.xlsx')

            inps = pd.DataFrame(data, columns=['ИНПС']).values.tolist()
            asosiy = pd.DataFrame(data, columns=["Дата рождения"]).values
            fio = pd.DataFrame(data, columns=['Сотрудник']).values.tolist()
            bolimi = pd.DataFrame(data, columns=["Подразделение организации"]).values.tolist()
            mansabi = pd.DataFrame(data, columns=['Должность']).values.tolist()
            tel = pd.DataFrame(data, columns=['Телефон']).values.tolist()
            bot.send_message(message.chat.id, "\nErtangi tug'ilgan kunlar:")

            for i in range(len(asosiy)):
                dat = str(asosiy[i][0])
                yili = int(dat[:4])
                oyi = int(dat[5:7])
                kuni = int(dat[8:10])
                qoldi = farq(oyi, kuni)
                if qoldi == 1:
                    rr = fio[i][0] + " Отдел " + bolimi[i][0] + ", " + mansabi[i][0] + ".\n"
                    r = requests.get(url + rr)
        elif txt == "indinga":
            bot.send_message(message.chat.id, "Kutib turing. \n Yuklanyapti")
            data = pd.read_excel(r'den.xlsx')

            inps = pd.DataFrame(data, columns=['ИНПС']).values.tolist()
            asosiy = pd.DataFrame(data, columns=["Дата рождения"]).values
            fio = pd.DataFrame(data, columns=['Сотрудник']).values.tolist()
            bolimi = pd.DataFrame(data, columns=["Подразделение организации"]).values.tolist()
            mansabi = pd.DataFrame(data, columns=['Должность']).values.tolist()
            tel = pd.DataFrame(data, columns=['Телефон']).values.tolist()
            bot.send_message(message.chat.id, "\nIndingi tug'ilgan kunlar:")

            for i in range(len(asosiy)):
                dat = str(asosiy[i][0])
                yili = int(dat[:4])
                oyi = int(dat[5:7])
                kuni = int(dat[8:10])
                qoldi = farq(oyi, kuni)
                if qoldi == 2:
                    rr = fio[i][0] + " Отдел " + bolimi[i][0] + ", " + mansabi[i][0] + ".\n"
                    r = requests.get(url + rr)
        elif txt == "3 kundan keyin":
            bot.send_message(message.chat.id, "Kutib turing. \n Yuklanyapti")
            data = pd.read_excel(r'den.xlsx')

            inps = pd.DataFrame(data, columns=['ИНПС']).values.tolist()
            asosiy = pd.DataFrame(data, columns=["Дата рождения"]).values
            fio = pd.DataFrame(data, columns=['Сотрудник']).values.tolist()
            bolimi = pd.DataFrame(data, columns=["Подразделение организации"]).values.tolist()
            mansabi = pd.DataFrame(data, columns=['Должность']).values.tolist()
            tel = pd.DataFrame(data, columns=['Телефон']).values.tolist()
            bot.send_message(message.chat.id, "\n3 kundan keyingi tug'ilgan kunlar:")

            for i in range(len(asosiy)):
                dat = str(asosiy[i][0])
                yili = int(dat[:4])
                oyi = int(dat[5:7])
                kuni = int(dat[8:10])
                qoldi = farq(oyi, kuni)
                if qoldi == 3:
                    rr = fio[i][0] + " Отдел " + bolimi[i][0] + ", " + mansabi[i][0] + ".\n"
                    r = requests.get(url + rr)
        elif txt == "shu oy":
            bot.send_message(message.chat.id, "Kutib turing. \n Yuklanyapti")
            data = pd.read_excel(r'den.xlsx')

            inps = pd.DataFrame(data, columns=['ИНПС']).values.tolist()
            asosiy = pd.DataFrame(data, columns=["Дата рождения"]).values
            fio = pd.DataFrame(data, columns=['Сотрудник']).values.tolist()
            bolimi = pd.DataFrame(data, columns=["Подразделение организации"]).values.tolist()
            mansabi = pd.DataFrame(data, columns=['Должность']).values.tolist()
            tel = pd.DataFrame(data, columns=['Телефон']).values.tolist()
            bot.send_message(message.chat.id, "\n3 kundan keyingi tug'ilgan kunlar:")
            xx = datetime.now(tz=ttz).month
            for i in range(len(asosiy)):
                dat = str(asosiy[i][0])
                yili = int(dat[:4])
                oyi = int(dat[5:7])
                kuni = int(dat[8:10])
                qoldi = farq(oyi, kuni)
                if xx == oyi:
                    rr = fio[i][0] + " Отдел " + bolimi[i][0] + ", " + mansabi[i][0] + ".\n"
                    r = requests.get(url + rr)
        else:
            bot.send_message(message.chat.id, "a???", parse_mode='html')
        #send user all text with information


    bot.polling(none_stop=True)



t1 = Thread(target=task1)
t2 = Thread(target=task2)
t1.start()
t2.start()
t1.join()
t2.join()

