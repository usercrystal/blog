from django.contrib import admin
from .models import ArticleColumn1

# Register your models here.


class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column', 'time_created', 'user')
    list_filter = ('column', )


admin.site.register(ArticleColumn1, ArticleColumnAdmin)
