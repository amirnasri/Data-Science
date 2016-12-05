import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def read_table(t):
	rows = t.find_all('tr')
	if rows is None:
		return None
	#get_str = lambda s: s.strip() if s is not None else s
	def get_str(s):
		if s is None or s.string is None:
			return None
		return s.string.strip()

	first_row = rows[0].find_all('th')
	headers = None
	if (len(first_row) != 0):
		headers = map(get_str, first_row)
		rows = rows[1:]

	body = []
	for r in rows:
		body.append(map(get_str, r.find_all('td')))
	df = pd.DataFrame(body)
	if headers is not None:
		df.columns = headers
	df.dropna(axis=0, how='all', inplace=True)
	df.dropna(axis=1, how='all', inplace=True)
	return df



req = requests.get('http://bccondos.net/821-cambie')
soup = BeautifulSoup(req.content, 'html.parser')
table = soup.find_all('table')[4]
print read_table(table)