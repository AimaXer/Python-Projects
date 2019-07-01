import requests
from bs4 import BeautifulSoup as bs

resp = requests.get('https://www.olx.pl')

data_r = bs(resp.text, 'html.parser')

print(data_r.prettify())
