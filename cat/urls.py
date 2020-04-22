from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url('panel/category/lists/', views.cat_list, name='cat_list'),
    url('panel/category/add/', views.cat_add, name='cat_add'),
]
