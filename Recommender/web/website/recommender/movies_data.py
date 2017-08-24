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
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

encodings = [
    'ascii',
    'utf-8',
    'big5',
    'big5hkscs',
    'cp037',
    'cp424',
    'cp437',
    'cp500',
    'cp737',
    'cp775',
    'cp850',
    'cp852',
    'cp855',
    'cp856',
    'cp857',
    'cp860',
    'cp861',
    'cp862',
    'cp863',
    'cp864',
    'cp865',
    'cp866',
    'cp869',
    'cp874',
    'cp875',
    'cp932',
    'cp949',
    'cp950',
    'cp1006',
    'cp1026',
    'cp1140',
    'cp1250',
    'cp1251',
    'cp1252',
    'cp1253',
    'cp1254',
    'cp1255',
    'cp1256',
    'cp1257',
    'cp1258',
    'euc_jp',
    'euc_jis_2004',
    'euc_jisx0213',
    'euc_kr',
    'gb2312',
    'gbk',
    'gb18030',
    'hz',
    'iso2022_jp',
    'iso2022_jp_1',
    'iso2022_jp_2',
    'iso2022_jp_2004',
    'iso2022_jp_3',
    'iso2022_jp_ext',
    'iso2022_kr',
    'latin_1',
    'iso8859_2',
    'iso8859_3',
    'iso8859_4',
    'iso8859_5',
    'iso8859_6',
    'iso8859_7',
    'iso8859_8',
    'iso8859_9',
    'iso8859_10',
    'iso8859_13',
    'iso8859_14',
    'iso8859_15',
    'johab',
    'koi8_r',
    'koi8_u',
    'mac_cyrillic',
    'mac_greek',
    'mac_iceland',
    'mac_latin2',
    'mac_roman',
    'mac_turkish',
    'ptcp154',
    'shift_jis',
    'shift_jis_2004',
    'shift_jisx0213',
    'utf_16',
    'utf_16_be',
    'utf_16_le',
    'utf_7']


def extract_img_url(resp):
    bs = BeautifulSoup(resp.content, "lxml")
    base_url = 'http://www.imdb.com/'
    url_poster = base_url + bs.find("div", class_="poster").a['href']
    resp = requests.get(url_poster)
    bs = BeautifulSoup(resp.content, 'lxml')
    src_url = bs.find('meta', itemprop='image')['content']
    return src_url


def get_imdb_url(movie_title):
    movie_title_split = movie_title.split(',')
    if len(movie_title_split) == 2:
        movie_title = ' '.join(map(lambda s: s.strip(), movie_title_split[::-1]))
        print('new_title=%s' % movie_title)

    search_url = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q=%s' % urllib.quote_plus(movie_title)
    print('search_url: %s\n' % search_url)
    res = requests.get(search_url)

    res_json = json.loads(res.content)
    movie_id = ''
    for k, v in res_json.iteritems():
        if k.startswith('title_popular') or k.startswith('title_exact'):
            for v_ in v:
                if 'id' in v_:
                    movie_id = v_['id']
                    break
    if not movie_id:
        print('Could not find IMDB url')

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
    results = json.loads(resp.content)['results'][0]
    poster_path = results['poster_path']
    overview = results['overview']

    """
    for e in encodings:
        try:
            overview = overview.decode(e)
        except (UnicodeDecodeError, UnicodeEncodeError):
            continue
        print('encoding %s worked!' % e)
        break
    else:
        print('no encoding worked!')
        overview = overview.decode('utf-8', 'replace')

    #overview = overview.encode()

    """
    try:
        overview = overview.decode('ascii')
    except:
        overview = ''
    tmdb_id = results['id']

    url = 'https://api.themoviedb.org/3/movie/%s?api_key=%s' % (tmdb_id, api_key)
    resp = requests.get(url)
    imdb_id = json.loads(resp.content)['imdb_id']

    poster_url = '%s%s%s' % (tmdb_secure_base_url, 'w500', poster_path)
    return poster_url, imdb_id, overview


regex = re.compile('(.*[^\s])\s+\(.*\)')
def get_poster(imdb_url, title):
    img_url = ''
    overview = ''
    try:
        img_url, imdb_id, overview = get_poster_tmdb(title)
        imdb_url = 'http://www.imdb.com/title/%s/' % imdb_id
    except Exception as e:
        print('tmdb query failed with exception: %s' % e)
        try:
            imdb_url, img_url = get_poster_imdb(imdb_url, title)
        except:
            pass
    return imdb_url, img_url, overview


def load_df_csv(filename):
    df = pd.read_csv(filename)
    df.index = df.icol(0)
    del df[df.columns[0]]
    df.index.name = None
    return df


def get_movie_info(incremental_save=True, resume=True):
    """ For each movie-titles in 'movies_df' get
    the movie poster url and the imdb link.
    """
    try:
        movies_df = load_df_csv(os.path.join(data_folder, 'movies_df.csv'))
    except IOError:
        print("Failed to load movie data.")
        return

    if resume:
        try:
            movies_info = load_df_csv(os.path.join(data_folder, 'movies_info.csv'))
        except IOError:
            movies_info = pd.DataFrame(columns=['movie_id', 'movie_title', 'movie_url', 'img_url'])

    for i in range(0, movies_df.shape[0]):
        #row = movies_df.iloc[i, :]
        row = movies_df.irow(i)

        # If resume is True, check if movie info is already
        # in the database
        movie_id = row['movie_id']
        if resume and any(movies_info['movie_id'] == movie_id):
            continue

        imdb_url = ''
        try:
            imdb_url = row['IMDB_url']
        except KeyError:
            pass

        movie_title = row['movie_title']
        while True:
            m = regex.search(movie_title)
            if m:
                movie_title = m.group(1)
            else:
                break

        print("\ndownloading %d, %s" % (i, movie_title))
        imdb_url, img_url, overview = get_poster(imdb_url, movie_title)
        if not imdb_url:
            imdb_url = get_imdb_url(movie_title)

        movies_info_row = {}
        movies_info_row['movie_id'] = row['movie_id']
        movies_info_row['movie_title'] = row['movie_title']
        movies_info_row['movie_url'] = imdb_url
        movies_info_row['img_url'] = img_url
        movies_info_row['overview'] = overview
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
        if incremental_save and (i + 1) % 10 == 0:
            print(movies_info)
            movies_info.to_csv(os.path.join(data_folder, 'movies_info.csv'))
        time.sleep(1)

    movies_info.to_csv(os.path.join(data_folder, 'movies_info.csv'))


def get_movie_list():
    movie_list = data.movies_info['movie_title'].tolist()
    movie_list = sorted([t.decode('utf-8', 'ignore') for t in movie_list])
    i = 0
    while True:
        if movie_list[i][0] >= 'A':
            break
        i += 1
    return movie_list[i:] + movie_list[:i]

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
        self.movie_ID_to_index = None
        self.movies_df = None
        self.movies_info = None

def load_movie_data():
    """ Load movie data the global 'data' variable so
    that it is accessible to the importing modules.
    """
    global data
    try:
        data = MovieData()
        data.pp_sim = np.load(os.path.join(data_folder, 'pp_sim.npy'))
        data.movie_index_to_ID = load_pickle(os.path.join(data_folder, 'movie_index_to_ID.pkl'))
        data.movie_ID_to_index = load_pickle(os.path.join(data_folder, 'movie_ID_to_index.pkl'))
        data.movies_df = load_df_csv(os.path.join(data_folder, 'movies_df.csv'))
        data.movies_info = load_df_csv(os.path.join(data_folder, 'movies_info.csv'))
        print("Loaded movie data.")
        return True
    except IOError as e:
        data = None
        print("Failed to load movie data: %s" % e)
        return False


USER_MOVIE_NUM = 3
RECOM_MOVIE_NUM = 6
def get_recommendations(request_params):
    try:
        movies = [request_params.get('m%d' % i).replace('+', ' ') for i in range(1, USER_MOVIE_NUM + 1)]
    except:
        return

    ratings = []
    for i in range(0, USER_MOVIE_NUM):
        if movies[i]:
            ratings.append(int(request_params.get('r%d' % (i + 1))))
    if len(ratings) == 0:
        return
    ratings = np.array(ratings) - 3

    user_movie_titles = pd.DataFrame({'movie_title': movies})
    print('user_movie_titles: \n%s' % user_movie_titles)
    user_movie_info = pd.merge(user_movie_titles, data.movies_df, how='inner', on='movie_title')
    print('user_movie_info: \n%s' % user_movie_info)
    user_movie_ids = user_movie_info['movie_id']
    if len(user_movie_ids) == 0:
        return
    print('user_movie_ids: \n%s' % user_movie_ids)
    user_movie_indexes = np.array([data.movie_ID_to_index[i] for i in user_movie_ids])
    print('user_movie_indexes: \n%s' % user_movie_indexes)
    combined_scores = ratings.dot(data.pp_sim[user_movie_indexes])
    recom_movie_indexes = np.argsort(combined_scores)[::-1]
    recom_movie_indexes = [i for i in recom_movie_indexes if i not in user_movie_indexes][:RECOM_MOVIE_NUM]
    recom_movie_ids = pd.DataFrame({'movie_id': [data.movie_index_to_ID[i] for i in recom_movie_indexes]})
    recom_movie_titles = pd.merge(recom_movie_ids, data.movies_df, how='inner', on='movie_id')
    print('recom_movie_indexes: \n%s' % recom_movie_indexes)
    print('recom_movie_ids: \n%s' % recom_movie_ids)
    print('recom_movie_titles: \n%s' % recom_movie_titles)
    #recom_movie_info = pd.merge(recom_movie_ids, data.movies_info, how='inner', on='movie_id')
    recom_movie_info = pd.merge(recom_movie_titles, data.movies_info, how='inner', on='movie_title')
    del recom_movie_info['movie_id_x']
    del recom_movie_info['movie_id_y']
    print('recom_movie_info: \n%s' % recom_movie_info)
    return recom_movie_info


def main():
    load_movie_data()


def test_main():
    set_data_folder('../data')
    load_movie_data()
    request_params = {}

    request_params['m1'] = 'Babe+(1995)'
    request_params['m2'] = 'Twelve+Monkeys+(1995)'
    request_params['m3'] = 'Seven+(Se7en)+(1995)'
    request_params['r1'] = 5
    request_params['r2'] = 5
    request_params['r3'] = 5

    get_recommendations(request_params)


# Default data folder
data_folder = 'data'
data = None

if __name__ == '__main__':
    test_main()
else:
    main()