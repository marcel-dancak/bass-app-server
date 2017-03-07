import random
import string

from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField


from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    youtube_username = models.CharField("youtube username", max_length=100, blank=True)
    likes = ArrayField(
        models.CharField(max_length=8),
        blank=True,
        default=[]
    )
    favourites = ArrayField(
        models.CharField(max_length=8),
        blank=True,
        default=[]
    )
    subscribers = models.ManyToManyField("self", blank=True) 

"""
class Profile(models.Model):
    youtube_username = models.CharField("youtube username", max_length=100, blank=True)
    likes = ArrayField(
        models.CharField(max_length=10),
        blank=True
    )
    favourites = ArrayField(
        models.CharField(max_length=10),
        blank=True
    )
"""

class Project(models.Model):
    id = models.CharField(
        "id",
        max_length=8,
        primary_key=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="user",
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.CharField("title", max_length=100, db_index=True, blank=False)
    artist = models.CharField("artist", max_length=100, db_index=True, blank=True)
    description = models.TextField("description", blank=True)
    youtube_link = models.CharField("youtube hash", max_length=100, blank=True)
    data = models.TextField("data")
    data_public = models.TextField("public version")
    timestamp = models.DateTimeField("time stamp", auto_now_add=True)

    # rename to genres
    genres = ArrayField(
        models.CharField(max_length=16, blank=True),
        db_index=True,
        blank=True
    )
    playing_styles = ArrayField(
        models.CharField(max_length=16, blank=True),
        db_index=True,
        blank=True
    )
    tracks = ArrayField(
        models.CharField(max_length=16, blank=True),
        blank=True
    )
    tags = ArrayField(
        models.CharField(max_length=16, blank=True),
        blank=True
    )
    # category: (cover/lesson/..)
    # difficulty = models.IntegerField("difficulty")
    level = models.IntegerField("level", default=3)
    likes = models.IntegerField("likes", default=0)

    # pinax-likes
    # revision history?

    class Meta:
        ordering = ["timestamp"]

    def __unicode__(self):
        return self.id

    def _random_id(self):
        return "".join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for x in range(8))

    def save(self, *args, **kwargs):
        if not self.id:
            random_id = self._random_id()
            while Project.objects.filter(id=random_id).exists():
                random_id = self._random_id()
            self.id = random_id
        return super(Project, self).save(*args, **kwargs)


# class FavouriteProjects(models.Model):
#     project = models.ForeignKey(
#         Project,
#         verbose_name="project",
#         on_delete=models.CASCADE
#     )
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         verbose_name="user",
#         on_delete=models.CASCADE
#     )