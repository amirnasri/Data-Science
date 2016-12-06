import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import dbutils
import sys

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
# Get current timestamp
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


# Get new listings
req = requests.get('http://bccondos.net/821-cambie')
soup = BeautifulSoup(req.content, 'html.parser')
table = soup.find_all('table')[4]
new_listings = read_table(table)
new_listings.date = st

# Get most recently stored listings from db
db = dbutils.get_db('/home/amir/git/ds/Email_new_listings/listings.db')
#q_res = make_query(db, 'select * from t2;')
most_recent = pd.read_sql_query("select * from most_recent", db)


if most_recent None:
	new_listings.to_sql('most_recent', db, if_exists = 'replace')	
	new_listings.to_sql('listings', db, if_exists = 'replace')	
	sys.exit(0)

is_new = new_listings.shape[0] != most_recent.shape[0]
is_new = is_new or 

MLS = 'MLS\xc2\xae'
new_listings[MLS]

	
	






