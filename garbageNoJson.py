import smtplib, ssl
from email.mime.text import MIMEText
import datetime

gmail_account = "******@gmail.com"
gmail_password = "password"
mail_to = "example@gmail.com"

def send_gmail(day_today, date_today) :
    week_num_of_mon = int(date_today.strftime('%d'))
    date_num = week_num_of_mon / 7
    subject_and_body = create_gmail_day_case(day_today, date_num)
    subject = subject_and_body[0]
    body = subject_and_body[1]
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_to
    msg["From"] = gmail_account

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg)
    print("ok.")

def create_gmail_day_case(day_of_week, date_num_mon) :
    if day_of_week == 0:
        subject = "ゴミ収集 きょうはありません"
        body = "今日は月曜日。 ゴミ収集はありません"
    elif day_of_week == 1:
        if date_num_mon <= 1:
            subject = "ゴミ収集 きょうは かん・びん"
            body = "今日は第一火曜日。 かん・びん ゴミの日です"
        elif date_num_mon >= 1 and date_num_mon <= 2:
            subject = "ゴミ収集 きょうは ペットボトル・雑がみ"
            body = "今日は第二火曜日。 ペットボトル・雑がみ ゴミの日です"
        elif date_num_mon >= 2 and date_num_mon <= 3:
            subject = "ゴミ収集 きょうは かん・びん"
            body = "今日は第三火曜日。 かん・びん ゴミの日です"
        elif date_num_mon >= 3 and date_num_mon <= 4:
            subject = "ゴミ収集 きょうは ペットボトル・雑がみ"
            body = "今日は第四火曜日。 ペットボトル・雑がみ ゴミの日です"
        else:
            return None
    elif day_of_week == 2:
        subject = "ゴミ収集 きょうは 燃やせるゴミ"
        body = "今日は水曜日。 燃やせるゴミの日です"
    elif day_of_week == 3:
        if date_num_mon <= 1:
            subject = "ゴミ収集 きょうは 大型ごみ"
            body = "今日は第一木曜日。 大型ごみの日です"
        elif date_num_mon >= 1 and date_num_mon <= 2:
            subject = "ゴミ収集 きょうは 燃やせないゴミ"
            body = "今日は第二木曜日。 燃やせないゴミの日です"
        elif date_num_mon >= 2 and date_num_mon <= 3:
            subject = "ゴミ収集 きょうは 紙パック・ダンボール"
            body = "今日は第三木曜日。 紙パック・ダンボール ゴミの日です"
        elif date_num_mon >= 3 and date_num_mon <= 4:
            subject = "ゴミ収集 きょうは 新聞ごみ"
            body = "今日は第四木曜日。 新聞 ゴミの日です"
        else:
            return None
    elif day_of_week == 4:
        subject = "ゴミ収集 きょうはありません"
        body = "今日は金曜日。 ゴミ収集はありません"
    elif day_of_week == 5:
        subject = "ゴミ収集 きょうは 燃やせるゴミ"
        body = "今日は土曜日。 燃やせるゴミの日です"
    elif day_of_week == 6:
        subject = "ゴミ収集 きょうはありません"
        body = "今日は日曜日。 ゴミ収集はありません"
    else:
        return None
    return subject, body

day = datetime.date.today().weekday()
date = datetime.datetime.today()
send_gmail(day, date)
