import requests, re
from bs4 import BeautifulSoup as bs
import smtplib
import unicodedata
import time, json

version = "1.0.0"
hdrs = {
    'Content-type': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
time_before_end_min = 30
time_before_end_hr = 0

def get_item(content, id):
    return content.find("div", {"class":id}).text

def get_data():
    with open("data.txt") as file:
        data = json.load(file)['data']
    return data

def main():
    while True:
        data = get_data()

        for item in data:
            response = requests.get(item['link'], headers=hdrs)
            page_content = bs(response.content, "html.parser")

            price = int(float(re.sub(',','.',re.sub('[A-Za-złńąść ]','', get_item(page_content, '_wtiln _bdn9q _9a071_2MEB_')))))
            time_left = unicodedata.normalize("NFKD",get_item(page_content, '_9a071_9F8-G')).encode('ascii', 'ignore')
            title = unicodedata.normalize("NFKD",get_item(page_content, '_1h7wt _15mod')).encode('ascii', 'ignore')

            try:
                time_left_int_min = int(time_left[3:5].decode("utf-8"))
                time_left_int_hr = int(time_left[0:2].decode("utf-8"))
            except ValueError as e:
                print('Value Error Line 30-34 ('+str(e)+')')
                continue

            try:
                if int(item['price']) >= price and time_left_int_min <= time_before_end_min and time_left_int_hr <= time_before_end_hr:
                    send_mail(item['link'], item['price'], time_left, title)
            except ValueError as e:
                print('Value Error Line 40-41 ('+str(e)+')')
                continue
            time.sleep(300)


def send_mail(url, wanted_price, time_left, name):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('maciej.jakub.chmielewski@gmail.com', 'ohgxepsdirjpemfe')

    subject = str(name.decode("utf-8"))+' | Allegro PW v'+version
    body = 'Aukcja konczy sie ponizej ceny '+str(wanted_price)+'zl\nDo konca aukcji pozostalo mniej niz 10 min !\n('+str(time_left.decode("utf-8"))+')\n\nLink do aukcji: '+str(url)

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'maciej.jakub.chmielewski@gmail.com',
        'maciej.jakub.chmielewski@gmail.com',
        msg
    )

if __name__ == '__main__':
   main()



