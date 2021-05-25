from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, AddPost, EditPost
from django.utils import timezone


def detail_view(request, slug, id):
    post = get_object_or_404(Post, slug=slug, id=id)
    return render(request, 'detail.html', {'post': post})


def main_page(request):
    pass


def about(request):
    return render(request, 'about.html')


# @login_required
def dashboard(request):
    posts = Post.objects.all()
    return render(request, 'dashboard.html', {'section': 'dashboard', 'posts': posts})


def register(request):
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