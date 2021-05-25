from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views


# here are all urls used in project
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('about', views.about),
    path('<slug:slug>/<int:id>', views.detail_view, name='post_detail'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('add_post/', views.add_post, name='add_post'),
    re_path(r'edit_post/(?P<post_id>[0-9]+)/', views.edit_post, name='edit_post'),
    path('search/', views.post_search, name='post_search'),
]