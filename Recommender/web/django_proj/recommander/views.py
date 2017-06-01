# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse



def index(request):
    context = {}
    return render(request, 'recommander/index.html', context)

def main(request):
    context = {}
    qs = request.environ['QUERY_STRING']
    names = [i.split('=')[1] for i in qs.split('&')]
    return HttpResponse("Hello %s " % " ".join(names))

