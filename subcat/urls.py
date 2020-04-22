from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url('panel/subcategory/lists/', views.subcat_list, name='subcat_list'),
    url('panel/subcategory/add/', views.subcat_add, name='subcat_add'),
]