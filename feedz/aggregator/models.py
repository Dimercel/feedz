from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name=_('name'))

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    @classmethod
    def get_absolute_url(cls):
        return reverse('category-list')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')


class Channel(models.Model):
    url = models.URLField(max_length=500, unique=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField()
    last_sync = models.DateTimeField()
    post_limit = models.PositiveSmallIntegerField(default=100)

    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('channel-update', args=[str(self.id)])


class Post(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField(max_length=500)
    favorite = models.BooleanField(default=False)
    published = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    channel = models.ForeignKey(Channel, null=True, on_delete=models.CASCADE)


class Favorite(models.Model):
    url = models.URLField(max_length=500)
    title = models.CharField(max_length=250)
    category_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    channel = models.ForeignKey(Channel, null=True, on_delete=models.CASCADE)
