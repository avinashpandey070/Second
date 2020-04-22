from django.shortcuts import render,get_object_or_404,redirect
from app1.models import Main
from news.models import News


def home(request):
    #sitename='Mysite | Home'
    #site=Main.objects.filter(pk=2)
    site = Main.objects.get(pk=2)
    news = News.objects.all()
    return render(request, 'front/hom.html',{'site':site,'news':news})
def about(request):
    site = Main.objects.get(pk=2)
    return render(request, 'front/about.html',{'site':site})
def panel(request):
    return render(request,'back/home.html')
