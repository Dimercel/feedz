from datetime import datetime
from time import mktime

import feedparser

from .models import Post


def sync_feed(channel):
    d = feedparser.parse(channel.url)
    for item in d.entries:
        if Post.objects.filter(title=item.title, channel=channel).exists():
            break

        Post.objects.create(
            title=item.title,
            url=item.link,
            favorite=False,
            published=datetime.fromtimestamp(mktime(item.updated_parsed)),
            channel=channel,
        )

    channel.last_sync = datetime.utcnow()
    channel.save()

    post_count = Post.objects.filter(channel=channel).count()
    if post_count > channel.post_limit:
        to_delete = (Post.objects.all().order_by('created_at')
                     [:post_count - channel.post_limit])
        to_delete.delete()
