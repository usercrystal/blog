from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView, TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
import json
import redis
from django.conf import settings

from .models import ArticleColumn1, ArticlePost1
from .forms import ArticleColumnForm, ArticlePostForm, CommentForm

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

# Create your views here.


class ArticleColumnView(View):
    user = get_user_model()

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArticleColumnView, self).dispatch(*args, **kwargs)

    @staticmethod
    def get(request):
        columns = ArticleColumn1.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, 'article/column/article_column.html',
                      {'columns': columns, 'column_form': column_form})

    @staticmethod
    def post(request):
        column = request.POST['column']
        columns = ArticleColumn1.objects.filter(user_id=request.user.id, column=column)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn1.objects.create(user=request.user, column=column)
            return HttpResponse('1')


class RenameArticleColumnView(View):
    user = get_user_model()

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RenameArticleColumnView, self).dispatch(*args, **kwargs)

    @staticmethod
    def get():
        return HttpResponse("0")

    @staticmethod
    def post(request):
        column_id = request.POST['column_id']
        column_name = request.POST['column_name']
        try:
            ArticleColumn1.objects.filter(id=column_id).update(column=column_name)
            return HttpResponse('1')
        except:
            return HttpResponse('0')


class DelArticleColumnView(View):
    user = get_user_model()

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DelArticleColumnView, self).dispatch(*args, **kwargs)

    @staticmethod
    def get():
        return HttpResponse("2")

    @staticmethod
    def post(request):
        column_id = request.POST['column_id']
        try:
            ArticleColumn1.objects.filter(id=column_id).delete()
            return HttpResponse('1')
        except:
            return HttpResponse('2')


class ArticlePostView(View):
    user = get_user_model()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArticlePostView, self).dispatch(*args, **kwargs)

    @staticmethod
    def get(request):
        article_columns = ArticleColumn1.objects.filter(user=request.user)
        article_post_form = ArticlePostForm()
        return render(request, 'article/column/article_post.html',
                      {'article_post_form': article_post_form, 'article_columns': article_columns})

    @staticmethod
    def post(request):
        article_post_form = ArticlePostForm(request.POST)
        if article_post_form.is_valid():
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse("1")
            except:
                return HttpResponse('2')
        else:
            return HttpResponse("3")


@method_decorator(cache_page(60 * 5), name='dispatch')
class ArticleListView(ListView):
    template_name = 'article/column/article_list.html'
    context_object_name = 'articles'
    model = ArticlePost1
    paginate_by = settings.ITEMS_PER_PAGE

    def get_queryset(self):
        articles = ArticlePost1.objects.filter(author=self.request.user)
        return articles


@method_decorator(cache_page(60*5), name='dispatch')
class ArticleDetailView(DetailView):
    model = ArticlePost1
    template_name = 'article/column/article_detail.html'

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ArticleDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        article = get_object_or_404(ArticlePost1, id=self.kwargs['id'], slug=self.kwargs['slug'])
        total_views = r.incr("article:{}:views".format(article.id))
        r.zincrby('article_ranking', 1, article.id)

        article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]
        article_ranking_id = [int(ranking_id) for ranking_id in article_ranking]
        most_viewed = list(ArticlePost1.objects.filter(id__in=article_ranking_id))
        most_viewed.sort(key=lambda x: article_ranking_id.index(x.id))
        context['article'] = article
        context['total_views'] = total_views
        context['most_viewed'] = most_viewed
        context['comments'] = article.comments.all()
        context['comment_form'] = CommentForm()
        return context


class DelArticleView(TemplateView):
    template_name = 'article/column/article_list.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(DelArticleView, self).dispatch(*args, **kwargs)

    @staticmethod
    def post(request):
        article_id = request.POST['article_id']
        try:
            ArticlePost1.objects.filter(id=article_id).delete()
            return HttpResponse("1")
        except:
            return HttpResponse("2")


class ReditArticleFormView(FormView):
    template_name = 'article/column/redit_article.html'
    form_class = ArticlePostForm

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_invalid(self, form):
        article_id = self.kwargs['article_id']
        article = ArticlePost1.objects.get(id=article_id)
        article_columns = self.request.user.article_column.all()
        this_article_column = article.column
        return render(self.request, 'article/column/redit_article.html', {
            'article': article,
            'article_columns': article_columns,
            'this_article_column': this_article_column
        })

    def form_valid(self, form):
        article_id = self.request['article_id']
        redit_article = ArticlePost1.objects.get(id=article_id)
        try:
            redit_article.column = self.request.user.article_column.get(
                id=self.request.POST['column_id']
            )
            redit_article.title = self.request.POST['title']
            redit_article.body = self.request.POST['body']
            redit_article.save()
            return HttpResponse('1')
        except:
            return HttpResponse('2')


@method_decorator(cache_page(60 * 5), name='dispatch')
class ArticleTitleListView(ListView):
    template_name = 'article/list/article_titles.html'
    model = ArticlePost1
    paginate_by = settings.ITEMS_PER_PAGE
    context_object_name = 'articles'

    def get_object(self):
        if self.kwargs:
            user = User.objects.get(username=self.kwargs['username'])
            articles = ArticlePost1.objects.filter(author=user)
        else:
            articles = ArticlePost1.objects.all()
        return articles

    def get_queryset(self):
        return self.get_object()


class LikeArticleView(View):
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        resp = super(LikeArticleView, self).dispatch(request, *args, **kwargs)
        if self.request.is_ajax():
            article_id = request.POST.get('id')
            action = request.POST.get('action')
            if article_id and action:
                try:
                    article = ArticlePost1.objects.get(id=article_id)
                    if action == "like":
                        article.user_like.add(request.user)
                        response_data = {"result": "OK"}
                    else:
                        article.user_like.remove(request.user)
                        response_data = {"result": "NO"}
                except:
                    response_data = {"result": "NO"}
            return HttpResponse(json.dumps(response_data),
                                content_type='application/json')
        else:
            return resp


class CommentFormView(FormView):
    template_name = 'article/column/article_detail.html'
    form_class = CommentForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        article = get_object_or_404(ArticlePost1, id=self.kwargs['id'], slug=self.kwargs['slug'])
        comment = form.save(commit=False)
        comment.article = article
        comment.commentator = user
        comment.save()
        self.success_url = article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        article = get_object_or_404(ArticlePost1, id=self.kwargs['id'], slug=self.kwargs['slug'])
        return render(self.request, 'article/column/article_detail.html', {
            'comment_form': form,
            'article': article,
        })


































