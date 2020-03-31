import smtplib, ssl
from email.mime.text import MIMEText
import datetime
import locale
import json

locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

def week_nom_get(date):
    date_k = int(date.strftime('%d')) / 7
    if date_k <= 1:
        return 1
    elif date_k >= 1 and date_k <= 2:
        return 2
    elif date_k >= 2 and date_k <= 3:
        return 3
    elif date_k >= 3 and date_k <= 4:
        return 4
    elif date_k >= 4 and date_k <= 5:
        return 5
    else:
        return None

def create_mail(mail_address, garbage, week_nom, day):
    gmail_account = "********@gmail.com"
    gmail_password = "***************"
    subject = "ゴミ収集 今日は{}".format(garbage)
    body = "今日は第{}{}曜日。ゴミ収集は{}となっています。".format(week_nom, day, garbage)
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_address
    msg["From"] = gmail_account

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg)
    print("ok")

today_day = datetime.date.today().weekday()
today_date = datetime.datetime.today()
day = today_date.strftime("%a")
date = today_date.strftime("%m%d")
week_nom = week_nom_get(today_date)
week_nom_index = week_nom - 1
day_nom_str = str(today_day)

f_cl = open("/home/ec2-user/program/garbage_client.json", "r")
data_cl = json.load(f_cl)
f_ad = open("/home/ec2-user/program/garbage_adrs_num.json", "r")
data_ad = json.load(f_ad)

for cl in data_cl:
    mail_address = data_cl[cl]['mail_address']
    address_num = str(data_cl[cl]['address_num'])
    if len(data_ad[address_num][day_nom_str]) == 1:
        today_garbage = data_ad[address_num][day_nom_str][0]
    else:
        today_garbage = data_ad[address_num][day_nom_str][week_nom_index]

    if date == "1231" or date == "0101" or date == "0102":
        today_garbage = "年末年始の為休業"
    create_mail(mail_address, today_garbage, week_nom, day)

f_cl.close()
f_ad.close()
