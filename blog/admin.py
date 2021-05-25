from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Administration panel. Posts sorted by publish date"""
    list_display = ('title', 'slug', 'author', 'publish')
    date_hierarchy = 'publish'