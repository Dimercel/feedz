from calendar import timegm
from datetime import datetime, timezone

import feedparser
import pytz
from django.db.models import Max

from .models import Post


def sync_feed(channel):
    data = feedparser.parse(channel.url)
    last_date = (Post.objects
                 .filter(channel=channel)
                 .aggregate(last_date=Max('published')))
    last_date = last_date['last_date']
    for item in data.entries:
        entry_upd = datetime.utcfromtimestamp(
            timegm(item.updated_parsed)).replace(tzinfo=pytz.UTC)

        if (last_date and entry_upd > last_date) or last_date is None:
            Post.objects.create(
                title=item.title[:250],
                url=item.link,
                favorite=False,
                published=entry_upd,
                channel=channel,
            )

    channel.last_sync = datetime.now(timezone.utc)
    channel.save()

    # Со временем посты накапливаются, мы должны удалять "старые" в
    # соответствии с ограничением
    post_count = Post.objects.filter(channel=channel).count()
    if post_count > channel.post_limit:
        beyound_limit = (Post.objects.filter(channel=channel).order_by('published')
                         [:post_count - channel.post_limit])
        beyound_limit.delete()
