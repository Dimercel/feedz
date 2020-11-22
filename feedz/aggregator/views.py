from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .feed import sync_feed
from .forms import CreateChannelForm, UpdateChannelForm
from .models import Category, Channel


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
            return HttpResponse(f'Error in form: {form.errors}')

        return redirect('channel-new')


class ChannelView(TemplateView, LoginRequiredMixin):
    model = Channel
    template_name = 'aggregator/channel_view.html'

    def get(self, request, pk, *args, **kwargs):
        model = get_object_or_404(Channel, pk=pk)

        categories = Category.objects.filter(user=request.user)
        nav_items = [(c.name, c.channel_set.all()) for c in categories]

        return render(request, self.template_name, context={
            'channel': model,
            'nav_items': nav_items,
            'posts': model.never_seen_posts().order_by('-published')[:model.post_limit]
        })

    def post(self, request, pk, *args, **kwargs):
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


@login_required()
def all_categories(request):
    categories = Category.objects.filter(user=request.user)
    cat_with_channels = [(c.name, c.channel_set.all()) for c in categories]

    return render(request, 'pages/home.html', context={
        'cat_info': cat_with_channels,
        'nav_items': cat_with_channels,
    })
