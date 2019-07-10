from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.views import LoginView

from .models import BlogTitle

# Create your views here.


class Blog_title(View):

    def get(self, request):
        blogs = BlogTitle.objects.all()
        return render(request, "blogs/titles.html", {"blogs": blogs})

# class Blog_content(View):
#     def get(self, request, blog_id):
#         content = get_object_or_404(BlogTitle, id=blog_id)
#         pub = content.publish
#         return render(request, blog/content.html, {'content': content, 'publish': pub})