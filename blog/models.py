from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# two models: Post and User (built-in)
class Post(models.Model):
    """This is Post model. It stores posts and authors are User models instances.
    Foreign key connects User and Post tables"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, default=title, unique=id)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ('publish', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Function for redirecting to post detail view"""
        return reverse('post_detail', args=[self.slug, self.id])