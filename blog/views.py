from django.shortcuts import render
from django.http import HttpResponse


def detail_view(request):
    return HttpResponse('<h1>It works</h1>')


def main_page(request):
    pass


def about(request):
    pass
