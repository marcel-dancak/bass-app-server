import os
import random
import string

from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_resized import ResizedImageField
# from django.utils import timezone

from django.contrib.auth.models import AbstractUser


def avatar_filename(instance, filename):
    return 'images/avatars/{0}{1}'.format(instance.pk, os.path.splitext(filename)[1])

class User(AbstractUser):
    avatar = ResizedImageField(
        'profile picture',
        size=[100, 100],
        crop=['middle', 'center'],
        upload_to=avatar_filename,
        null=True,
        blank=True
    )
    likes = ArrayField(
        models.CharField(max_length=8),
        blank=True,
        default=[]
    )
    bookmarks = ArrayField(
        models.CharField(max_length=8),
        blank=True,
        default=[]
    )

    subscribed = models.ManyToManyField("self", blank=True, symmetrical=False, related_name='subscribers')

    # link to profiles (youtube, twitter, facebook, instagram, patreon)
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
    CATEGORY_CHOICES = (
        ('Cover', 'Cover'),
        ('Lesson', 'Lesson'),
        ('Arrangement', 'Arrangement'),
        ('Original Composition', 'Original Composition'),
        ('Backing Track', 'Backing Track')
    )
    LEVEL_CHOICES = (
        (0, 'Very Easy'),
        (1, 'Easy'),
        (2, 'Easy/Medium'),
        (3, 'Medium'),
        (4, 'Medium/Hard'),
        (5, 'Hard'),
        (6, 'Very Hard')
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
        # blank=True,
        null=True
    )
    title = models.CharField("title", max_length=100, db_index=True, blank=False)
    artist = models.CharField("artist", max_length=100, db_index=True, blank=True)
    description = models.TextField("description", blank=True)
    video_link = models.CharField("video link", max_length=100, blank=True)
    data = models.TextField("data")
    public = models.BooleanField("public", default=False)

    created = models.DateTimeField("created", auto_now_add=True)
    # created = models.DateTimeField("created", default=timezone.now, blank=True)
    modified = models.DateTimeField("last modified", auto_now_add=True)
    # modified = models.DateTimeField("last modified", default=timezone.now, blank=True)

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
    category = models.CharField("category", max_length=20, choices=CATEGORY_CHOICES)
    level = models.IntegerField("difficulty", default=3, choices=LEVEL_CHOICES)
    likes = models.IntegerField("likes", default=0)

    # format = models.IntegerField("format", null=True)

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

