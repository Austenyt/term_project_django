from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('blog_list', BlogListView.as_view(), name='blog_list'),
    path('blog_view/<int:pk>/', BlogDetailView.as_view(), name='blog_view'),
    path('blog/blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/blog_update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/blog_delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]
