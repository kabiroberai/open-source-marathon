# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, 'src/index.html')


def search(request):
    q: str = request.GET.get('q')
    if q is None:
        return redirect('index')
    q = q.strip()
    if q == "":
        return redirect('index')
    return HttpResponse(f"You searched for '<strong>{ request.GET.get('q') }</strong>'")
