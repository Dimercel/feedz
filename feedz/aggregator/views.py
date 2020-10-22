from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .forms import CreateChannelForm
from .models import Category, Channel


class CategoryListView(TemplateView):
    template_name = 'aggregator/category_list.html'

    def get(self, request):
        all_categories = Category.objects.all()

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
