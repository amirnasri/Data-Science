from sqlite3 import dbapi2 as sq3
import os

def get_db(dbfile):
    sqlite_db = sq3.connect(dbfile)
    return sqlite_db

def init_db(dbfile, schema):
    """Creates the database tables."""
    db = get_db(dbfile)
    db.cursor().executescript(schema)
    db.commit()
    return db

def make_query(db, query):
	c = db.cursor()
	return c.execute(query).fetchall()

