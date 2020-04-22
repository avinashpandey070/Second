from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url('news/(?P<word>.*)/', views.news_detail, name='news_detail'),
    url('panel/news/lists', views.news_list, name='news_lists'),
    url('panel/news/add', views.news_add, name='news_add'),
    url('panel/news/del/(?P<pk>\d+)', views.news_delete, name='news_delete'),
    url('panel/news/edit/(?P<pk>\d+)', views.news_edit, name='news_edit'),
]
