import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import urllib
import time
import os
import re
import numpy as np
import pickle

def extract_img_url(resp):
    bs = BeautifulSoup(resp.content, "lxml")
    base_url = 'http://www.imdb.com/'
    url_poster = base_url + bs.find("div", class_="poster").a['href']
    resp = requests.get(url_poster)
    bs = BeautifulSoup(resp.content, 'lxml')
    src_url = bs.find('meta', itemprop='image')['content']
    return src_url


def get_imdb_url(movie_title):
    search_url = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q=%s' % urllib.quote_plus(movie_title)
    res = requests.get(search_url)

    res_json = json.loads(res.content)
    movie_id = ''
    for k, v in res_json.iteritems():
        if k.startswith('title_popular'):
            for v_ in v:
                if 'id' in v_:
                    movie_id = v_['id']
                    break

    return 'http://www.imdb.com/title/%s/' % movie_id


def get_poster_imdb(url, title):
    """
    Args:
        url: imdb-url from the database
        title: movie title from data base
    return:
        tuple of imdb-url, image-url for the given movie
    """
    print("trying imdb for %s" % title)
    img_url = ''
    try:
        resp = requests.get(url)
        img_url = extract_img_url(resp)
    except:
        pass

    if img_url:
        return url, img_url

    # If imdb-url in the movie table is broken, search for the movie id
    # using imdb API
    url = get_imdb_url(title)
    resp = requests.get(url)
    return url, extract_img_url(resp)


tmdb_configuration = None
api_key = None
def get_poster_tmdb(title):
    print("trying tmdb for %s" % title)
    global tmdb_configuration, api_key

    if not tmdb_configuration:
        with open(os.path.join(data_folder, 'tmdb_api_key')) as f:
            api_key = f.readline().strip()
        resp = requests.get('https://api.themoviedb.org/3/configuration?api_key=%s' % api_key)
        tmdb_configuration = json.loads(resp.content)
    tmdb_secure_base_url = tmdb_configuration['images']['secure_base_url']
    url = 'https://api.themoviedb.org/3/search/movie?api_key=%s&query=%s' % (api_key, title)
    resp = requests.get(url)
    poster_path = json.loads(resp.content)['results'][0]['poster_path']
    url = '%s%s%s' % (tmdb_secure_base_url, 'w500', poster_path)
    return url


regex = re.compile('(.*[^\s])\s+\(.*\)')
def get_poster(imdb_url, title):
    while True:
        m = regex.search(title)
        if m:
            title = m.group(1)
        else:
            break

    img_url = ''
    imdb_url = ''
    try:
        img_url = get_poster_tmdb(title)
    except Exception as e:
        print('tmdb query failed with exception: %s' % e)
        try:
            imdb_url, img_url = get_poster_imdb(imdb_url, title)
        except:
            pass
    return imdb_url, img_url


def load_df_csv(filename):
    df = pd.read_csv(filename)
    df.index = df.icol(0)
    del df[df.columns[0]]
    df.index.name = None
    return df


def get_movie_info(incremental_save=True, resume=True):
    try:
        movies_df = load_df_csv(os.path.join(data_folder, 'movies_df.csv'))
    except IOError:
        print("Failed to load movie data.")
        return

    if resume:
        try:
            movies_info = load_df_csv(os.path.join(data_folder, 'movies_info.csv'))
        except IOError:
            movies_info = pd.DataFrame(columns=['MovieID', 'movie-title', 'movie-url', 'img-url'])

    for i in range(0, movies_df.shape[0]):
        if incremental_save and (i + 1) % 10 == 0:
            print(movies_info)
            movies_info.to_csv(os.path.join(data_folder, 'movies_info.csv'))
        #row = movies_df.iloc[i, :]
        row = movies_df.irow(i)

        # If resume is True, check if movie info is already
        # in the database
        movie_id = row['MovieID']
        if resume and any(movies_info['MovieID'] == movie_id):
            continue

        imdb_url = row['IMDb-URL']
        movie_title = row['movie-title']
        m = regex.search(movie_title)
        if m:
            movie_title = m.group(1)

        print("downloading %d, %s" % (i, movie_title))
        imdb_url, img_url = get_poster(imdb_url, movie_title)
        if not imdb_url:
            imdb_url = get_imdb_url(movie_title)

        movies_info_row = {}
        movies_info_row['MovieID'] = row['MovieID']
        movies_info_row['movie-title'] = movie_title
        movies_info_row['movie-url'] = imdb_url
        movies_info_row['img-url'] = img_url
        movies_info = movies_info.append(pd.DataFrame(movies_info_row, index=[0]), ignore_index=True)

        """
        img_file_name = "movie_posters/%d_img.jpg" % movies_df.loc[i, :]['MovieID']
        if not os.path.exists(img_file_name) or os.path.getsize(img_file_name) == 0:
            with open(img_file_name, "wb") as f1:
                try:
                    req = requests.get(img_url)
                    f1.write(req.content)
                except:
                    pass
            wait = True
        """
        time.sleep(1)

    movies_info.to_csv(os.path.join(data_folder, 'movies_info.csv'))


def load_pickle(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


def set_data_folder(folder):
    global data_folder
    data_folder = folder


class MovieData():
    def __init__(self):
        self.pp_sim = None
        self.movie_index_to_ID = None
        self.movies_df = None
        self.movies_info = None

def load_movie_data():
    global data
    try:
        data = MovieData()
        data.pp_sim = np.load(os.path.join(data_folder, 'pp_sim.npy'))
        data.movie_index_to_ID = load_pickle(os.path.join(data_folder, 'movie_index_to_ID.pkl'))
        data.movies_df = load_df_csv(os.path.join(data_folder, 'movies_df.csv'))
        data.movies_info = load_df_csv(os.path.join(data_folder, 'movies_info.csv'))
        print("Loaded movie data.")
        return True
    except IOError:
        data = None
        print("Failed to load movie data.")
        return False

# Default data folder
data_folder = 'data'
data = None
load_movie_data()
