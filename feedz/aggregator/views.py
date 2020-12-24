from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .feed import sync_feed
from .forms import CreateChannelForm, UpdateChannelForm
from .models import Category, Channel, Favorite, Post


def navigation_items(user):
    categories = Category.objects.filter(user=user)

    return [(c.name, c.channel_set.order_by('name')) for c in categories]


class CategoryListView(TemplateView, LoginRequiredMixin):
    template_name = 'aggregator/category_list.html'

    def get(self, request, *args, **kwargs):
        own_categories = Category.objects.filter(user=request.user)

        return render(request, self.template_name, context={
            'category_list': own_categories,
        })


class CategoryCreate(CreateView, LoginRequiredMixin):
    model = Category
    fields = ['name']
    template_name = 'aggregator/category_new.html'

    def post(self, request, *args, **kwargs):
        new_category = Category(
            name=request.POST['name'],
            user=request.user
        )

        new_category.save()

        return redirect('category-list')


class CategoryUpdate(UpdateView, LoginRequiredMixin):
    model = Category
    fields = ['name']
    template_name = 'aggregator/category_update.html'


class ChannelCreate(CreateView, LoginRequiredMixin):
    model = Channel
    form_class = CreateChannelForm
    template_name = 'aggregator/channel_new.html'

    def post(self, request, *args, **kwargs):
        form = CreateChannelForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            new_channel = Channel.objects.create(
                url=data.get('url'),
                name=data.get('name'),
                post_limit=data.get('post_limit'),
                category=data.get('category'),
                last_seen=timezone.now(),
                last_sync=timezone.now()
            )

            sync_feed(new_channel)
        else:
            return render(request, self.template_name, {'form': form})

        return redirect('channel-new')


class ChannelView(TemplateView, LoginRequiredMixin):
    model = Channel
    template_name = 'aggregator/channel_view.html'

    def get(self, request, pk):
        model = get_object_or_404(Channel, pk=pk)
        sync_date = model.last_sync
        if datetime.now(timezone.utc) - sync_date > settings.MIN_SYNC_TIME_DELTA:
            sync_feed(model)

        return render(request, self.template_name, context={
            'channel': model,
            'nav_items': navigation_items(request.user),
            'posts': model.never_seen_posts().order_by('-published')[:model.post_limit]
        })

    def post(self, request, pk):
        if 'date' in request.POST:
            model = get_object_or_404(Channel, pk=pk)

            DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
            try:
                model.last_seen = datetime.strptime(request.POST['date'], DATE_FORMAT)
            except ValueError:
                return HttpResponse(model.last_seen.strftime(DATE_FORMAT))

            model.save()

        return HttpResponse(model.last_seen.strftime(DATE_FORMAT))


class ChannelUpdate(UpdateView, LoginRequiredMixin):
    model = Channel
    form_class = UpdateChannelForm
    template_name = 'aggregator/channel_update.html'


class ChannelDelete(DeleteView, LoginRequiredMixin):
    model = Channel
    success_url = reverse_lazy('home')

    def post(self, request, pk, *args, **kwargs):
        own_categories = request.user.category_set.values('id')

        # Удаляемый канал должен принадлежать пользователю
        if pk in list(Channel.objects
                      .filter(category_id__in=own_categories)
                      .values_list('id', flat=True)):

            return super().post(request, pk, *args, **kwargs)

        return HttpResponseRedirect(self.success_url)


class FavoriteListView(TemplateView, LoginRequiredMixin):
    model = Favorite
    template_name = 'aggregator/favorite_list.html'

    def get(self, request):
        favorites = {}
        for item in Favorite.objects.order_by('updated_at').all():
            cat_name = item.category_name
            if cat_name in favorites:
                favorites[cat_name].append(item)
            else:
                favorites[cat_name] = [item]

        return render(request, self.template_name, {
            'favorites': favorites,
            'nav_items': navigation_items(request.user),
        })


class FavoriteDelete(DeleteView, LoginRequiredMixin):
    model = Favorite
    success_url = reverse_lazy('favorite-list')


@login_required()
@require_GET
def all_categories(request):
    nav_items = navigation_items(request.user)

    return render(request, 'pages/home.html', context={
        'cat_info': nav_items,
        'nav_items': nav_items
    })


@login_required()
@require_POST
def add_favorite(request, channel_id):
    post_id = request.POST.get('post_id')

    if post_id:
        post = Post.objects.get(pk=post_id)
        channel = Channel.objects.select_related().get(pk=channel_id)

        if post:
            Favorite.objects.create(
                url=post.url,
                title=post.title,
                category_name="{} >> {}".format(channel.category.name,
                                                channel.name),
                channel=channel
            )

            return HttpResponse('added')

    return HttpResponse('error')
