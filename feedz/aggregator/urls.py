from django.urls import path

from . import views

urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('category/new/', views.CategoryCreate.as_view(), name='category-new'),
]
