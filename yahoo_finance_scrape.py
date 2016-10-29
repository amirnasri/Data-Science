import requests
import numpy as np
from bs4 import BeautifulSoup
import json

def table_to_np_array(table):
	rows = table.find_all('tr')
	return np.array([[c.string for c in r.find_all('td')] for r in rows])

cname = raw_input("company name:")
req = requests.get("http://autoc.finance.yahoo.com/autoc?query=%s&region=US&lang=en-GB" % cname)
js = json.loads(req.content)
symbol = js['ResultSet']['Result'][1]['symbol'].upper()
print("stock sticker symbol: %s" % symbol)
req = requests.get("https://ca.finance.yahoo.com/q/ao?s=" + symbol.upper())
soup = BeautifulSoup(req.text, "html.parser")
tables = soup.find_all('table', attrs='yfnc_datamodoutline1')

for j in range(len(tables)):
	print(table_to_np_array(tables[j]))
	print
	print


