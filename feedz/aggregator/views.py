from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .forms import CreateChannelForm, UpdateChannelForm
from .models import Category, Channel


class CategoryListView(TemplateView):
    template_name = 'aggregator/category_list.html'

    def get(self, request, *args, **kwargs):
        all_categories = Category.objects.filter(user=request.user)

        return render(request, self.template_name, context={
            'category_list': all_categories,
        })


class CategoryCreate(CreateView):
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


class CategoryUpdate(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'aggregator/category_update.html'


class ChannelCreate(CreateView):
    model = Channel
    form_class = CreateChannelForm
    template_name = 'aggregator/channel_new.html'

    def post(self, request, *args, **kwargs):
        form = CreateChannelForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Channel.objects.create(
                url=data.get('url'),
                name=data.get('name'),
                post_limit=data.get('post_limit'),
                category=data.get('category'),
                last_seen=timezone.now(),
                last_sync=timezone.now()
            )
        else:
            return HttpResponse(f'Error in form: {form.errors}')

        return redirect('channel-new')


class ChannelUpdate(UpdateView):
    model = Channel
    form_class = UpdateChannelForm
    template_name = 'aggregator/channel_update.html'


def all_categories(request):
    categories = Category.objects.filter(user=request.user)
    cat_with_channels = [(c.name, c.channel_set.all()) for c in categories]
    return render(request, 'pages/home.html', context={
        'cat_info': cat_with_channels,
        'nav_items': cat_with_channels,
    })
