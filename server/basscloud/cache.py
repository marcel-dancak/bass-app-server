from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse

from basscloud.catalog.models import Project


def index_key(key):
    return key+':_index'

def version_key(key, version):
    return key+':'+version

def clear_cache(key):
    print('CLEAR CACHE')
    index = cache.get(index_key(key))
    print(index)
    if index:
        keys = [version_key(key, v) for v in index]
        keys.append(index_key(key))
        cache.delete_many(keys)
        print('delete', keys)


@receiver(post_save, sender=Project)
def project_edited(sender, instance, **kwargs):
    print('Project Edited')
    clear_cache(reverse('catalog:projects'))
    clear_cache(reverse('catalog:author_projects', args=[instance.user.pk]))
    key = reverse('app:project_data', args=[instance.pk])+'.json/'
    print(key)
    cache.delete(key)
