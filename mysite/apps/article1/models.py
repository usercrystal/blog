from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from slugify import slugify

# Create your models here.


class ArticleColumn1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_column')
    column = models.CharField(max_length=200)
    time_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticlePost1(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article')
    title = models.CharField(max_length=200)
    column = models.ForeignKey(ArticleColumn1, on_delete=models.CASCADE, related_name='article_column')
    slug = models.SlugField(max_length=500)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    user_like = models.ManyToManyField(User, related_name='articles_like', blank=True)

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)  # 建立数据库索引

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ArticlePost1, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.id, self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(ArticlePost1, on_delete=models.CASCADE, related_name='comments')
    commentator = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='已注销', related_name='commentators')
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {0} on {1}'.format(self.commentator.username, self.article)