from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


def detail_view(request, slug, id):
    post = get_object_or_404(Post, slug=slug, id=id)
    return render(request, 'detail.html', {'post': post})


def main_page(request):
    pass


def about(request):
    return render(request, 'about.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'section': 'dashboard'})