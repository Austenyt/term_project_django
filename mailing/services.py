from django.core.cache import cache

from config import settings
from mailing.models import Mailing


def get_mailings(product_pk):
    if settings.CACHE_ENABLED:
        key = f'mailing_list{product_pk}'
        mailing_list = cache.get(key)
        if mailing_list is None:
            mailing_list = Mailing.objects.filter(product_pk=product_pk)
            cache.set(key, mailing_list)
    else:
        mailing_list = Mailing.objects.filter(product_pk=product_pk)

    return mailing_list
