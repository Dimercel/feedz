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

    path('channel/<int:channel_id>/favorite/',
         login_required(views.add_favorite),
         name='add-favorite'),

    path('channel/<int:pk>/',
         login_required(views.ChannelView.as_view()),
         name='channel-view'),

    path('channel/<int:pk>/update/',
         login_required(views.ChannelUpdate.as_view()),
         name='channel-update'),

    path('channel/<int:pk>/delete/',
         login_required(views.ChannelDelete.as_view()),
         name='channel-delete'),

    path('favorite/',
         login_required(views.FavoriteListView.as_view()),
         name='favorite-list'),

    path('favorite/<int:pk>/delete/',
         login_required(views.FavoriteDelete.as_view()),
         name='favorite-delete'),
]
