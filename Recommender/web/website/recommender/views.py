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
from django.views.decorators.csrf import csrf_exempt
import subprocess

def load_recom_data():
    global recom_data
    try:
        recom_data = RecomData()
        recom_data.pp_sim = np.load('data/pp_sim.npy')
        recom_data.movie_index_to_ID = load_pickle('data/movie_index_to_ID.pkl')
        recom_data.movies_df = pd.read_pickle('data/movies_df.pkl')
        print("Loaded recom data.")
    except IOError:
        recom_data = None
        print("Failed to load recom data.")

        # recom_movie_index = np.argsort(pp_sim[0, :])[::-1][:5]
    # recom_movie_df = pd.merge(recom_movie_id_df, movies_df, how='inner', on='MovieID')


def load_pickle(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


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
    if recom_data:
        for movie in recom_data.movies_df['movie-title'].tolist():
            try:
                movies_options += u'<option> %s </option>' % movie
            except UnicodeDecodeError:
                pass
    context['movie_options'] = movies_options
    return render(request, 'recommender/index.html', context)


@csrf_exempt
def upload_data(request):
    body = request.read()
    with open('data/result.tar.gz', 'w') as f:
        f.write(body)
    os.chdir('data')
    subprocess.check_call('tar -xzvf result.tar.gz'.split())
    os.chdir('..')
    load_recom_data()
    return HttpResponse('Data upload successful\n')


def test(request):
    context = {'requesty':d}
    return render(request, 'recommender/test.html', context)


def recommender(request):
    context = {}
    if not recom_data:
        context['img_urls'] = "No movie data found on the server."
        return JsonResponse(context)

    qs = request.environ['QUERY_STRING']
    names = [i.split('=')[1] for i in qs.split('&')]
    #return HttpResponse("Hello %s " % " ".join(names))
    #context = {'a':int(request.GET['r1'])}
    url_list = []
    recom_movie_index = (np.argsort(recom_data.pp_sim[0, :]))[::-1][:5]
    recom_movie_id_df = pd.DataFrame({'MovieID': [recom_data.movie_index_to_ID[i] for i in recom_movie_index]})
    recom_movie_df = pd.merge(recom_movie_id_df, recom_data.movies_df, how='inner', on='MovieID')

    img_urls = ''
    for url in recom_movie_df['IMDb-URL'].tolist():
        img_urls += '<a href = "%s">' % url + \
            '<img src="%s" style = "width:200px;height:300px;border:0">' % get_poster_imdb(url) + \
            '</a>'

    print(img_urls)
    context['img_urls'] = img_urls
    #context['cwd'] = cwd
    #context['ls_output'] = os.listdir('data')
    #return render(request, 'recommander/recom_result.html', context)

    return JsonResponse(context)


class RecomData():
    def __init__(self):
        self.pp_sim = None
        self.movie_index_to_ID = None
        self.movies_df = None


url_cache = {}

recom_data = None
load_recom_data()



d = dir()