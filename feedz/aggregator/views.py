from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .models import Category


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


class CategoryUpdate(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'aggregator/category_update.html'
