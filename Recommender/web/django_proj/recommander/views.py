# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse



def index(request):
    context = {}
    return render(request, 'recommander/index.html', context)

def main(request):
    qs = request.environ['QUERY_STRING']
    names = [i.split('=')[1] for i in qs.split('&')]
    #return HttpResponse("Hello %s " % " ".join(names))
    context = {'request': request}
    context = {'a':int(request.GET['r1'])}
    return render(request, 'recommander/main.html', context)

