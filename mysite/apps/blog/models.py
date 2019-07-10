from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class BlogTitle(models.Model):
    title = models.EmailField(max_length=300)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
