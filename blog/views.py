from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, AddPost, EditPost, SearchForm
from django.utils import timezone
from django.contrib.postgres.search import SearchVector


def detail_view(request, slug, id):
    """This view redirects user to post details"""
    post = get_object_or_404(Post, slug=slug, id=id)
    return render(request, 'detail.html', {'post': post})


def about(request):
    """This is about page"""
    return render(request, 'about.html')


def dashboard(request):
    """This is main page"""
    posts = Post.objects.all()
    return render(request, 'dashboard.html', {'section': 'dashboard', 'posts': posts})


def register(request):
    """This view is for user registration"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем новый объект пользователя, но пока его не сохраняем
            new_user = user_form.save(commit=False)
            # Устанавливаем выбранный пароль
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Сохраняем объект пользователя
            new_user.save()
            return render(request, 'registration/registration_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html',
                  {'user_form': user_form})


@login_required
def add_post(request):
    """This view is for adding posts (if user is authenticated)"""
    if request.method == 'POST':
        form = AddPost(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author_id = request.user.id
            new_post.save()
            return HttpResponse('<h2>Post successfully added. <h2>')
    else:
        form = AddPost()
    return render(request, 'add_post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    """This views lets users to edit their posts"""
    try:
        post = get_object_or_404(Post, id=post_id)
    except BaseException:
        return HttpResponse('<h1>Oops something happened<h1>')
    if post.author != request.user:
        return HttpResponse('<h2>You can`t edit this post because you aren`t an author')
    if request.method == 'POST':
        print(request.POST)
        form = EditPost(request.POST)
        if form.is_valid():
            post.title = request.POST.__getitem__('title')
            post.body = request.POST.__getitem__('body')
            post.publish = timezone.now()
            post.save()
            return HttpResponse('<h1>Post successfully changed.<h1>')
        return HttpResponse('<h1>Form is invalid<h1>')
    else:
        return render(request, 'edit_post.html', {'form': EditPost})


def post_search(request):
    """
        This view is for searching post via query-word.
        Returns posts with query_word in body or in title
    """
    form = SearchForm
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)
    return render(request, 'search.html', {'form': form, 'query': query, 'results': results})