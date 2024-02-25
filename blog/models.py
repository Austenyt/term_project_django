from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)
    body = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog_previews/', blank=True, null=True)
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
