import random
import string

from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_resized import ResizedImageField


from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = ResizedImageField(
        'profile picture',
        size=[100, 100],
        crop=['middle', 'center'],
        upload_to='static/media/images/avatars/',
        null=True,
        blank=True
    )
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

    # youtube, twitter, facebook, instagram, patreon
    links = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=[]
    )

class Project(models.Model):
    INSTRUMENTS_CHOICES = (
        ('bass', 'Bass'),
        ('drums', 'Dass'),
        ('percussions', 'Percussions'),
        ('piano', 'Piano')
    )
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
    video_link = models.CharField("video link", max_length=100, blank=True)
    data = models.TextField("data")
    data_public = models.TextField("public version", blank=True)

    # rename to created
    created = models.DateTimeField("created", auto_now_add=True)
    modified = models.DateTimeField("last modified", auto_now=True)

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
        models.CharField(
            max_length=16,
            choices=INSTRUMENTS_CHOICES,
            blank=True),
        blank=True
    )
    tags = ArrayField(
        models.CharField(max_length=16, blank=True),
        blank=True
    )
    # (cover/lesson/backing track/composition..)
    category = models.CharField(max_length=20)
    # difficulty = models.IntegerField("difficulty")
    level = models.IntegerField("level", default=3)
    likes = models.IntegerField("likes", default=0)

    # revision history?

    class Meta:
        ordering = ["-created"]

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

