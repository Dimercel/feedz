from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Category


class CategoryListView(TemplateView):
    template_name = 'aggregator/category_list.html'

    def get(self, request):
        all_categories = Category.objects.all()

        return render(request, self.template_name, context={
            'category_list': all_categories,
        })
