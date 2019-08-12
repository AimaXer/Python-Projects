import requests
#from bs4 import BeautifulSoup as bs

hdrs = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

response = requests.get('https://www.google.pl', headers=hdrs)
