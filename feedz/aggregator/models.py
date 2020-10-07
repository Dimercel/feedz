from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)


class Channel(models.Model):
    url = models.URLField(max_length=500, unique=True, null=False)
    name = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField()
    last_sync = models.DateTimeField()
    post_limit = models.PositiveSmallIntegerField(default=100)

    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)


class Post(models.Model):
    title = models.CharField(max_length=250, null=False)
    url = models.URLField(max_length=500, null=False)
    favorite = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    channel = models.ForeignKey(Channel, null=True, on_delete=models.CASCADE)


class Favorite(models.Model):
    url = models.URLField(max_length=500, null=False)
    title = models.CharField(max_length=250, null=False)
    category_name = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    channel = models.ForeignKey(Channel, null=True, on_delete=models.CASCADE)
