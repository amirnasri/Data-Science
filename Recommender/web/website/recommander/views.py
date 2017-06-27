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


def load_pickle(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

url_cache = {}
cwd = os.getcwd()
pp_sim = np.load('data/pp_sim.npy')
movie_index_to_ID = load_pickle('data/movie_index_to_ID.pkl')
movies_df = pd.read_pickle('data/movies_df.pkl')
#recom_movie_index = np.argsort(pp_sim[0, :])[::-1][:5]
#recom_movie_df = pd.merge(recom_movie_id_df, movies_df, how='inner', on='MovieID')

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
    recom_movie_index = reversed(np.argsort(pp_sim[0, :]))[:5]
    recom_movie_id_df = pd.DataFrame({'MovieID': [movie_index_to_ID[i] for i in recom_movie_index]})
    recom_movie_df = pd.merge(recom_movie_id_df, movies_df, how='inner', on='MovieID')

    img_urls = ''
    for url in recom_movie_df['IMDb-URL'].tolist():
        img_urls += '<a href = "%s">' % url + \
            '<img src="%s" style = "width:200px;height:300px;border:0">' % get_poster_imdb(url) + \
            '</a>'

    context['img_urls'] = img_urls
    #context['cwd'] = cwd
    #context['ls_output'] = os.listdir('data')
    #return render(request, 'recommander/recom_result.html', context)

    return JsonResponse(context)
