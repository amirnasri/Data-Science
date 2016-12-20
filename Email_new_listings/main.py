import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import dbutils
import sys
import time
import datetime

def read_table(t):
	rows = t.find_all('tr')
	if rows is None:
		return None
	#get_str = lambda s: s.strip() if s is not None else s
	def get_str(s):
		if s is None:
			return None
		if s.string is None:
			if s.a is None or s.a.string is None:
				return None
			else:
				return s.a.string.strip()
		else:
			return s.string.strip()

	first_row = rows[0].find_all('th')
	headers = None
	if len(first_row) != 0:
		headers = map(get_str, first_row)
		rows = rows[1:]

	body = []
	for r in rows:
		body.append(map(get_str, r.find_all('td')))
	df = pd.DataFrame(body)
	if headers is not None:
		df.columns = headers
	for c in df.columns:
		if c.startswith('MLS'):
			break
	df = df[df[c].notnull()]
	df.dropna(axis=1, how='any', inplace=True)
	return df


if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf8')

	# Get current timestamp
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


	# Get new listings
	req = requests.get('http://bccondos.net/821-cambie')
	soup = BeautifulSoup(req.content, 'html.parser')
	table = soup.find_all('table')[4]
	new_listings = read_table(table)
	new_listings.date = st
	print new_listings

	# Get most recently stored listings from db
	db = dbutils.get_db('./listings.db')
	#q_res = make_query(db, 'select * from t2;')
	try:
		prev_active = pd.read_sql_query("select * from active_listings", db)
	except BaseException:
		new_listings.to_sql('active_listings', db, if_exists = 'replace')
		dbutils.make_query(db, "drop table if exists 'past_listings'")
		sys.exit(0)

	if 'index' in prev_active.columns:
		del prev_active['index']

	is_new = True
	try:
		is_new = not (new_listings == prev_active).all().all()
	except ValueError:
		pass

	print is_new
	if is_new:
	#	email(most_recent, new_listings)
		new_listings.to_sql('active_listings', db, if_exists='replace')
		prev_active.to_sql('past_listings', db, if_exists='append')


	
	






