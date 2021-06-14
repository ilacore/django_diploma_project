from django.db import models
from django.urls import reverse
from django.conf import settings
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import AbstractBaseUser

User = settings.AUTH_USER_MODEL

# Create your models here.

"""class User(models.Model):
    username = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    is_enabled = models.BooleanField(default=True)
    email = models.EmailField()
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username"""


class Post(models.Model):
    is_enabled = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'self', on_delete=models.PROTECT, blank=True, null=True, default=''
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    class Meta:
        ordering = ['parent_id', 'created_at']

    def display_text(self):
        short = " ".join(self.text.split()[0:5])
        if len(short) > 20:
            short = self.text[:20] + "..."
        return short

    display_text.short_description = 'Text'

    def __str__(self):
        space = " "
        return f'{space.join(self.text.split()[0:5])} ({str(self.created_at)})'

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])


class Item(models.Model):
    video = EmbedVideoField()
