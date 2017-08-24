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


def index(request):
    """ Main page presenting the user with a drop-down menu
     to choose three movies and rate them a score between 1 to 5.
    """
    context = {}
    movies_options = u''
    try:
        if movies_data.data:
            for movie in movies_data.data.movies_df['movie_title'].tolist():
                try:
                    movies_options += u'<option> %s </option>' % movie
                except UnicodeDecodeError:
                    pass
    except:
        pass
    context['movie_options'] = movies_options
    response = render(request, 'recommender/index.html', context)
    response['Cache-Control'] = 'no-cache'
    return response

@csrf_exempt
def upload_data(request):
    """ Called by spark.py to upload the result of spark script
    onto the server. spark.py used the following command to upload
    the data:
    curl -T result.tar.gz amirnasri.ca/recommender/upload_data

    The uploaded file 'result.tar.gz' has a flat structure (no folders)
    and should be extracted to './data'.
    """
    body = request.read()
    if not os.path.exists('data'):
        os.mkdir('data')
    with open('data/result.tar.gz', 'w') as f:
        f.write(body)
    os.chdir('data')
    subprocess.check_call('tar -xzvf result.tar.gz'.split())
    os.chdir('..')
    return load_movie_data(request)


@csrf_exempt
def get_movie_data(request):
    """ Get movie poster url and imdb links and then
    load them so they can be accessed by 'recommender' view

        Command: curl http://amirnasri.ca/recommender/get_movie_data
    """
    movies_data.get_movie_info()
    movies_data.load_movie_data()
    return HttpResponse('Successfully downloaded movie info.\n')


@csrf_exempt
def load_movie_data(request):
    """ Load movie data in the 'data' folder

        Command: curl http://amirnasri.ca/recommender/load_movie_data
    """
    if movies_data.load_movie_data():
        return HttpResponse('Successfully loaded movie info.\n')
    else:
        return HttpResponse('Failed to load movie info.\n')


def recommender(request):
    context = {}
    if not movies_data.data:
        context['img_urls'] = "No movie data found on the server."
        return JsonResponse(context)
    cmd = ''
    try:
        cmd = request.GET.get('cmd')
    except:
        pass

    if cmd:
        if cmd == 'get_movie_list':
            movie_list = ['']
            movie_list.extend(movies_data.get_movie_list())
            movie_list = ''.join(['<option>%s</option>' % i for i in movie_list])
            context['movie_list'] = movie_list
            return JsonResponse(context)
        return

    #qs = request.environ['QUERY_STRING']
    #names = [i.split('=')[1] for i in qs.split('&')]
    recom_movie_info = movies_data.get_recommendations(request.GET)
    if recom_movie_info is None\
            or len(recom_movie_info) == 0:
        return JsonResponse(context)

    recom_movie_info.overview = [i if isinstance(i, str) else '' for i in recom_movie_info.overview]

    results = []
    for i in range(recom_movie_info.shape[0]):
        row = recom_movie_info.irow(i)
        results.append(dict(row))

    context['results'] = results
    print(context)
    jr = JsonResponse(context)
    return jr


def test(request):
    context = {'request': None}
    return render(request, 'recommender/test.html', context)