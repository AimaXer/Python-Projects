import requests, re
from bs4 import BeautifulSoup as bs
import smtplib
import unicodedata
import time

version = 1.0

def get_item(content, id):
    return content.find("div", {"class":id}).text

def main():
    hdrs = {
        'Content-type': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    url = "https://allegro.pl/oferta/macbook-pro-15-i7-16gb-240-ssd-bcm-8381191094"
    response = requests.get(url, headers=hdrs)

    wanted_price = 10000

    page_content = bs(response.content, "html.parser")

    price = int(float(re.sub(',','.',re.sub('[A-Za-złńąść ]','', get_item(page_content, '_wtiln _bdn9q _9a071_2MEB_')))))
    time_left = unicodedata.normalize("NFKD",get_item(page_content, '_9a071_9F8-G')).encode('ascii', 'ignore')
    title = unicodedata.normalize("NFKD",get_item(page_content, '_1h7wt _15mod')).encode('ascii', 'ignore')

    time_left_int15 = 0
    time_left_int00 = '01'

    try:
        time_left_int15 = int(time_left[3:5].decode("utf-8"))
        time_left_int00 = str(time_left[0:2].decode("utf-8"))
        print(time_left_int00)
        print(time_left_int15)
    except ValueError:
        print('Time is not in intiger type')

    if wanted_price > price and time_left_int15 < 150 and time_left_int00 == '18':
        send_mail(url, wanted_price, time_left, title)

def send_mail(url, wanted_price, time_left, name):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('maciej.jakub.chmielewski@gmail.com', 'ohgxepsdirjpemfe')

    subject = str(name.decode("utf-8"))+' | Allegro PW v'+str(version)
    body = 'Aukcja konczy sie ponizej ceny '+str(wanted_price)+'zl\nDo konca aukcji pozostalo mniej niz 10 min !\n('+str(time_left.decode("utf-8"))+')\n\nLink do aukcji: '+str(url)

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'maciej.jakub.chmielewski@gmail.com',
        'maciej.jakub.chmielewski@gmail.com',
        msg
    )

if __name__ == '__main__':
   main()



