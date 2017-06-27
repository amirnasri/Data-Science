import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import urllib


url_cache = {}

def extract_img_url(resp):
    bs = BeautifulSoup(resp.content, "lxml")
    base_url = 'http://www.imdb.com/'
    url_poster = base_url + bs.find("div", class_="poster").a['href']
    resp = requests.get(url_poster)
    bs = BeautifulSoup(resp.content, 'lxml')
    src_url = bs.find('meta', itemprop='image')['content']
    return src_url


def get_poster_imdb(url, movie_title):
    print("trying %s, %s" % (url, movie_title))
    src_url = ''
    try:
        resp = requests.get(url)
        src_url = extract_img_url(resp)
    except:
        pass

    if src_url:
        return src_url

    # If imdb-url in the movie table is broken, search for the movie id
    # using imdb API
    search_url = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q=%s' % urllib.quote_plus(movie_title)
    res = requests.get(search_url)

    res_json = json.loads(res.content)
    movie_id = ''
    for k, v in res_json.iteritems():
        if k.startswith('title'):
            for v_ in v:
                if 'id' in v_:
                    movie_id = v_['id']
                    break

    url = 'http://www.imdb.com/title/%s/' % movie_id
    resp = requests.get(url)
    return extract_img_url(resp)

# Load movie table
movies_df = pd.read_csv('ml-100k/u.item', delimiter='|', engine='python', header=None)
# Movie table columns as provided in the ReadMe file
columns = ' MovieID | movie title | release date | video release date |' \
              'IMDb URL | unknown | Action | Adventure | Animation |'\
              'Children | Comedy | Crime | Documentary | Drama | Fantasy |'\
              'Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |'\
              'Thriller | War | Western'.split('|')

movies_df.columns = ["-".join(i.strip().split()) for i in columns]
movies_df.head()

import time

movies_df.loc[:, 'img_url'] = None
for i in range(4, 10):#movies_df.shape[0]):
    movie_url = movies_df.iloc[i, :]['IMDb-URL']
    movie_title = movies_df.iloc[i, :]['movie-title']
    img_url = get_poster_imdb(movie_url, movie_title)
    movies_df.loc[i, 'img_url'] = img_url
    print img_url
    time.sleep(1)

movies_df.to_pickle('movies_df.pkl')
print(movies_df)