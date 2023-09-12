from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Category, Post, Author, Subscription
from .filters import PostFilter
from .forms import NewsForm, ArticlesForm
from django.contrib.auth.models import User, Group
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect


class PostList(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now', 'is_author'] = datetime.utcnow(), self.request.user.groups.filter(name='Авторы').exists()
        return context


class NewsList(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Post.objects.filter(type_post="NW")
        return context


class ArticlesList(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Post
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Post.objects.filter(type_post="AR")
        return context


class SearchResults(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    raise_exception = True
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class NewsDetail(LoginRequiredMixin, DetailView):
    raise_exception = True
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'

    def get_queryset(self, *, object_list=None, **kwargs):
        return super().get_queryset().filter(type_post=Post.news)


class ArticlesDetail(LoginRequiredMixin, DetailView):
    raise_exception = True
    model = Post
    template_name = 'articles_detail.html'
    context_object_name = 'post'

    def get_queryset(self, *, object_list=None, **kwargs):
        return super().get_queryset().filter(type_post=Post.article)


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post')
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        news_detail = form.save(commit=False)
        news_detail.type_post = 'NW'
        return super().form_valid(form)


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post')
    raise_exception = True
    form_class = ArticlesForm
    model = Post
    template_name = 'articles_create.html'

    def form_valid(self, form):
        news_detail = form.save(commit=False)
        news_detail.type_post = 'AR'
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post')
    raise_exception = True
    form_class = NewsForm
    model = Post
    ordering = '-time_in'
    template_name = 'news_update.html'


class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post')
    raise_exception = True
    form_class = ArticlesForm
    model = Post
    template_name = 'articles_update.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    raise_exception = True
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    raise_exception = True
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('articles')


@login_required
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='Авторы')
    if not user.groups.filter(name='Авторы').exists():
        group.user_set.add(user)
        Author.objects.create(author=user)
    return redirect('/posts/news/')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)

        action = request.POST.get('action')
        if action == 'subscribe':
            Subscription.objects.create(user=request.user, to_category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                to_category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                to_category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

# class IndexView(View):
#     def get(self, request):
#         printer.delay(10)
#         hello.delay()
#         return HttpResponse('Hello!')