from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ValidationError


class OauthUser(models.Model):
    author = models.ForeignKey(User, verbose_name='用户', blank=True, null=True,
                               on_delete=models.CASCADE)
    type = models.CharField(blank=False, null=False, max_length=50)
    email = models.CharField(max_length=50, null=True, blank=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    def __str__(self):
        return self.author.username

    class Meta:
        ordering = ['-created_time']


class OauthConfig(models.Model):
    TYPE = (
        ('github', 'GitHub'),
    )
    type = models.CharField('类型', max_length=10, choices=TYPE, default='a')
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    # 查询是否该第三方账户已绑定本网站账号
    # def clean(self):
    #     if OAuthConfig.objects.filter(type=self.type).exclude(id=self.id).count():
    #         raise ValidationError(_(self.type + '已经存在'))

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'oauth配置'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
