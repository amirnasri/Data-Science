# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import os
import numpy as np
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import movies_data


# Views:

def index(request):
    context = {}
    movies_options = u''
    if movies_data.data:
        for movie in movies_data.data.movies_df['movie-title'].tolist():
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
    movies_data.load_movie_data()
    return HttpResponse('Data upload successful\n')


@csrf_exempt
def get_movie_data(request):
    movies_data.get_movie_info()
    movies_data.load_movie_data()
    return HttpResponse('Successfully downloaded movie info.\n')


@csrf_exempt
def load_movie_data(request):
    if movies_data.load_movie_data():
        return HttpResponse('Successfully loaded movie info.\n')
    else:
        return HttpResponse('Failed to load movie info.\n')


def test(request):
    context = {'request': None}
    return render(request, 'recommender/test.html', context)


def recommender(request):
    context = {}
    if not movies_data.data:
        context['img_urls'] = "No movie data found on the server."
        return JsonResponse(context)

    qs = request.environ['QUERY_STRING']
    names = [i.split('=')[1] for i in qs.split('&')]
    recom_movie_index = (np.argsort(movies_data.data.pp_sim[0, :]))[::-1][:5]
    recom_movie_id = pd.DataFrame({'MovieID': [movies_data.data.movie_index_to_ID[i] for i in recom_movie_index]})
    recom_movie_info = pd.merge(recom_movie_id, movies_data.data.movies_info, how='inner', on='MovieID')
    img_urls = ''
    print(recom_movie_id)
    for i in range(recom_movie_info.shape[0]):
        row = recom_movie_info.irow(i)
        img_urls += '<a href = "%s">' % row['movie-url'] + \
            '<img src="%s" style = "width:200px;height:300px;border:0">' % row['img-url'] + \
            '</a>'

    print(img_urls)
    context['img_urls'] = img_urls
    return JsonResponse(context)

