import smtplib, ssl
from email.mime.text import MIMEText
import datetime
import locale
import json

#ロケールの設定。後でstrftime(%a)したときに日本語で出力される。
locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

#今日が月のうち何週目なのかを取得する関数。
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
    #引数をもとにメールを作成
    gmail_account = "********@gmail.com"
    gmail_password = "***************"
    subject = "ゴミ収集 今日は{}".format(garbage)
    body = "今日は第{}{}曜日。ゴミ収集は{}となっています。".format(week_nom, day, garbage)
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_address
    msg["From"] = gmail_account
　　
　　#サーバーに接続
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg)
    print("ok")

#日付の取得
today_day = datetime.date.today().weekday()　#今日の曜日の取得。返り値の型はint。
today_date = datetime.datetime.today()　#今日の日付の取得。返り値の型はdatetime。・・・(1)
day = today_date.strftime("%a")　# (1)で取得した日付から曜日だけを日本語の省略形で取得。 返り値の型はstring。
date = today_date.strftime("%m%d")　#(1)で取得した日付から月と日付をつなぎ合わせた4桁の数字で取得。返り値の型はstring。
week_nom = week_nom_get(today_date) #week_nom_get関数を実行し、返り値をweek_nomに代入。
week_nom_index = week_nom - 1　#後々使うためにweek_nomから１引いたもの。インデックス番号用。
day_nom_str = str(today_day)

f_cl = open("/home/ec2-user/program/garbage_client.json", "r") #クライアントリストのjsonをオープン
data_cl = json.load(f_cl) #jsonの型をpythonの型として読み込めるようにロード
f_ad = open("/home/ec2-user/program/garbage_adrs_num.json", "r") #同様
data_ad = json.load(f_ad)

for cl in data_cl:　#clはクライアントのIDを指している。
    mail_address = data_cl[cl]['mail_address']　#data_cl[cl]でIDの値となっているdictを参照。またdictにキーの['mail_address']をつけ、バリューであるメールアドレスを取得。
    address_num = str(data_cl[cl]['address_num'])　#同様に地区番号を取得。またintからstrに変換。
    if len(data_ad[address_num][day_nom_str]) == 1: #曜日ごとのゴミ収集のリストの要素数が１(=毎週同じゴミの曜日)であるときの処理。
        today_garbage = data_ad[address_num][day_nom_str][0]
    else:　#それ以外のときの処理
        today_garbage = data_ad[address_num][day_nom_str][week_nom_index] 

    if date == "1231" or date == "0101" or date == "0102": #年末年始は休みなのでその分の処理も足しておく。
        today_garbage = "年末年始の為休業"
    create_mail(mail_address, today_garbage, week_nom, day) #いままでに取得した情報を引数としてcreate_mail関数を実行。

f_cl.close()　#jsonのクローズ
f_ad.close()
