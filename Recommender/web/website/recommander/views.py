# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import os
import numpy as np
import pandas as pd
import pickle
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
import urllib


def load_pickle(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

url_cache = {}
cwd = os.getcwd()
pp_sim = np.load('data/pp_sim.npy')
movie_index_to_ID = load_pickle('data/movie_index_to_ID.pkl')
#movies_df = pd.read_csv('data/movies_df.csv')
movies_df = pd.read_pickle('data/movies_df.pkl')
#movies_df.index = movies_df.iloc[:, 0]
#del movies_df[movies_df.columns[0]]
#recom_movie_index = np.argsort(pp_sim[0, :])[::-1][:5]
#recom_movie_df = pd.merge(recom_movie_id_df, movies_df, how='inner', on='MovieID')
print movies_df['IMDb-URL']



def extract_img_url(resp):
    bs = BeautifulSoup(resp.content, "lxml")
    base_url = 'http://www.imdb.com/'
    url_poster = base_url + bs.find("div", class_="poster").a['href']
    resp = requests.get(url_poster)
    bs = BeautifulSoup(resp.content, 'lxml')
    src_url = bs.find('meta', itemprop='image')['content']
    return src_url


def get_poster_imdb(url, movie_title):

    src_url = ''
    try:
        resp = requests.get(url)
        src_url = extract_img_url(resp)
    except:
        pass

    if src_url:
        url_cache[url] = src_url
        return src_url

    print(url, movie_title)
    # If imdb-url in the movie table is broken, search for the movie id
    # using imdb API
    try:
        search_url = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q=%s' % urllib.quote_plus(movie_title)
        print(search_url)
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
        print('final url: %s' % url)
        resp = requests.get(url)
        src_url = extract_img_url(resp)
        url_cache[url] = src_url
    except IOERROR:
        pass
    return src_url
    
"""
def get_poster_imdb(url):
    if url in url_cache:
        return url_cache[url]
    try:
        resp = requests.get(url)
        bs = BeautifulSoup(resp.content, "lxml")
        base_url = 'http://www.imdb.com/'
        url_poster = base_url + bs.find("div", class_="poster").a['href']
        resp = requests.get(url_poster)
        bs = BeautifulSoup(resp.content, 'lxml')
        src_url = bs.find('meta', itemprop='image')['content']
        url_cache[url] = src_url
        return src_url
    except:
        return ""
"""

def index(request):
    context = {}
    movies_options = u''
    print movies_df
    for movie in movies_df['movie-title'].tolist():
        try:
            movies_options += u'<option> %s </option>' % movie
        except UnicodeDecodeError:
            pass
    context['movie_options'] = movies_options
    return render(request, 'recommander/index.html', context)

def test(request):
    context = {}
    return render(request, 'recommander/test.html', context)

def recommander(request):
    qs = request.environ['QUERY_STRING']
    names = [i.split('=')[1] for i in qs.split('&')]
    #return HttpResponse("Hello %s " % " ".join(names))
    #context = {'a':int(request.GET['r1'])}
    context = {}
    url_list = []
    recom_movie_index = (np.argsort(pp_sim[0, :]))[::-1][:5]
    recom_movie_id_df = pd.DataFrame({'MovieID': [movie_index_to_ID[i] for i in recom_movie_index]})
    recom_movie_df = pd.merge(recom_movie_id_df, movies_df, how='inner', on='MovieID')

    movie_urls = recom_movie_df[['IMDb-URL', 'movie-title']].to_records()
    img_urls = ''
    for _, url, title in movie_urls:
        img_urls += '<a href = "%s">' % url + \
            '<img src="%s" style = "width:200px;height:300px;border:0">' % get_poster_imdb(url, title) + \
            '</a>'

    print(img_urls)
    context['img_urls'] = img_urls
    #context['cwd'] = cwd
    #context['ls_output'] = os.listdir('data')
    #return render(request, 'recommander/recom_result.html', context)

    return JsonResponse(context)
