from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('category/',
         login_required(views.CategoryListView.as_view()),
         name='category-list'),

    path('category/new/',
         login_required(views.CategoryCreate.as_view()),
         name='category-new'),

    path('category/<pk>/update/',
         login_required(views.CategoryUpdate.as_view()),
         name='category-update'),

    path('channel/new/',
         login_required(views.ChannelCreate.as_view()),
         name='channel-new'),

    path('channel/<int:pk>/update/',
         login_required(views.ChannelUpdate.as_view()),
         name='channel-update'),
]
