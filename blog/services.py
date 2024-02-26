from django.core.cache import cache

from blog.models import Blog
from config import settings


def get_cached_articles_for_blog(self, *args, **kwargs):
    if settings.CACHE_ENABLED:
        key = 'blog_list'
        blog_list = cache.get(key)
        if blog_list is None:
            blog_list = Blog.objects.filter(is_published=True)
            cache.set(key, blog_list)
    else:
        blog_list = Blog.objects.filter(is_published=True)

    return blog_list
