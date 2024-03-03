from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog
from blog.services import get_cached_articles_for_blog


class BlogListView(LoginRequiredMixin, ListView):
    """
        Представление для отображения списка статей блога.
    """
    model = Blog
    extra_context = {
        'title': 'Статьи блога'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['article'] = get_cached_articles_for_blog(self.request.GET.get('pk'))
        return context_data


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
        Представление для создания новой статьи блога.
    """
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Создать статью'
    }

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
        Представление для редактирования статьи блога.
    """
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Редактировать статью'
    }

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_view', args=[self.kwargs.get('pk')])


class BlogDetailView(LoginRequiredMixin, DetailView):
    """
        Представление для отображения деталей статьи блога.
    """
    model = Blog
    extra_context = {
        'title': 'Просмотр статьи'
    }

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.object = None

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
        Представление для удаления статьи блога.
    """
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
    extra_context = {
        'title': 'Удаление статьи'
    }
