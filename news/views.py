from django.shortcuts import render, get_object_or_404, redirect
from app1.models import Main
from news.models import News
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
from trending.models import Trending
from random import randint
import random

# Create your views here.

def news_detail(request, word):
    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    shownews = News.objects.filter(name=word)
    popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    tagname = News.objects.get(name=word).tag
    trending = Trending.objects.all().order_by('-pk')[ :5]
    tag = tagname.split(',')
    try :
        mynews = News.objects.get(name=word)
        mynews.show = mynews.show + 1
        mynews.save()
    except:
        print("Can't Add Show")

    return render(request, 'front/news_detail.html',
                  {'site':site,'news':news,'cat':cat,'subcat':subcat,
                   'lastnews':lastnews,'shownews':shownews,'popnews':popnews,'popnews2':popnews2,
                   'tag':tag,'trending':trending})

def news_detail_short(request, pk):
    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    shownews = News.objects.filter(rand=pk)
    popnews = News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    tagname = News.objects.get(rand=pk).tag
    trending = Trending.objects.all().order_by('-pk')[ :5]
    tag = tagname.split(',')
    try :
        mynews = News.objects.get(rand=pk)
        mynews.show = mynews.show + 1
        mynews.save()
    except:
        print("Can't Add Show")

    return render(request, 'front/news_detail.html',
                  {'site':site,'news':news,'cat':cat,'subcat':subcat,
                   'lastnews':lastnews,'shownews':shownews,'popnews':popnews,'popnews2':popnews2,
                   'tag':tag,'trending':trending})


def news_list(request):
    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser': perm = 1
    if perm == 0:
        news = News.objects.filter(writer=request.user)
    elif perm == 1:
        news =News.objects.all()

    return render(request, 'back/news_list.html', {'news': news})


def news_add(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    if len(str(day)) == 1:
        day = '0' + str(day)
    if len(str(month)) == 1:
        month = '0' + str(month)
    today = str(year) + '/' + str(month) + '/' + str(day)
    time = str(now.hour) + ':' + str(now.minute)
    date = str(year) + str(month) + str(day)
    randint = str(random.randint(1000,9999))
    rand = date + randint
    rand = int(rand)
    while len(News.objects.filter(rand=rand)) != 0 :
        randint = str(random.randint(1000, 9999))
        rand = date + randint
        rand = int(rand)
    cat = SubCat.objects.all()
    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstextshort = request.POST.get('newstextshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')
        tag = request.POST.get('tag')

        if newstitle == '' or newscat == '' or newstextshort == '' or newstxt == '':
            error = 'All field required'
            return render(request, 'back/error.html', {'error': error})
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)
            if str(myfile.content_type).startswith('image'):
                if myfile.size < 2000000:
                    newsname = SubCat.objects.get(pk=newsid).name
                    ocatid = SubCat.objects.get(pk=newsid).catid
                    b = News(name=newstitle, short_text=newstextshort, body_text=newstxt, date=today, time=time,
                             picname=filename, picurl=url, writer=request.user, catname=newsname, catid=newsid, show=0,
                             ocatid=ocatid,tag=tag,rand=rand)
                    b.save()
                    count = len(News.objects.filter(ocatid=ocatid))
                    b = Cat.objects.get(pk=ocatid)
                    b.count = count
                    b.save()
                    return redirect(news_list)
                else:
                    fs = FileSystemStorage()
                    fs.delete(filename)
                    error = 'your file size is more than 2MB '
                    return render(request, 'back/error.html', {'error': error})
            else:
                fs = FileSystemStorage()
                fs.delete(filename)
                error = 'your file is not an image'
                return render(request, 'back/error.html', {'error': error})
        except:
            error = 'Please choose an image'
            return render(request, 'back/error.html', {'error': error})

    return render(request, 'back/news_add.html', {'cat':cat})

def news_delete(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end
    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser': perm = 1
    if perm == 0:
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user) :
            error = 'Acess denied'
            return render(request, 'back/error.html', {'error': error})
    try:
        b = News.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(b.picname)
        ocatid = News.objects.get(pk=pk).ocatid
        b.delete()

        count = len(News.objects.filter(ocatid=ocatid))
        m = Cat.objects.get(pk=ocatid)
        m.count = count
        m.save()

    except:
        error = 'Something wrong'
        return render(request, 'back/error.html', {'error': error})
    return redirect('news_list')

def news_edit(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end
    perm = 0
    for i in request.user.groups.all():
        if i.name == 'masteruser': perm = 1
    if perm == 0:
        a = News.objects.get(pk=pk).writer
        if str(a) != str(request.user) :
            error = 'Acess denied'
            return render(request, 'back/error.html', {'error': error})
    if len(News.objects.filter(pk=pk)) == 0:
        error = 'News not found'
        return render(request, 'back/error.html', {'error': error})
    news = News.objects.get(pk=pk)
    cat = SubCat.objects.all()
    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstextshort = request.POST.get('newstextshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')
        tag = request.POST.get('tag')

        if newstitle == '' or newscat == '' or newstextshort == '' or newstxt == '':
            error = 'All field required'
            return render(request, 'back/error.html', {'error': error})
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)
            if str(myfile.content_type).startswith('image'):
                if myfile.size < 2000000:
                    newsname = SubCat.objects.get(pk=newsid).name
                    b = News.objects.get(pk=pk)

                    fss = FileSystemStorage()
                    fss.delete(b.picname)

                    b.name = newstitle
                    b.short_text = newstextshort
                    b.body_text = newstxt
                    b.picname = filename
                    b.picurl = url
                    b.catname = newsname
                    b.catid = newsid
                    b.tag = tag
                    b.act = 0
                    b.save()
                    return redirect(news_list)
                else:
                    fs = FileSystemStorage()
                    fs.delete(filename)
                    error = 'your file size is more than 2MB '
                    return render(request, 'back/error.html', {'error': error})
            else:
                fs = FileSystemStorage()
                fs.delete(filename)
                error = 'your file is not an image'
                return render(request, 'back/error.html', {'error': error})
        except:
            newsname = SubCat.objects.get(pk=newsid).name
            b = News.objects.get(pk=pk)

            b.name = newstitle
            b.short_text = newstextshort
            b.body_text = newstxt
            b.catname = newsname
            b.catid = newsid
            b.tag = tag
            b.act = 0
            b.save()
            return redirect(news_list)

    return render(request, 'back/news_edit.html', {'pk':pk,'news':news,'cat':cat})

def news_all_show(request,word):

    catid = Cat.objects.get(name=word).pk
    allnews = News.objects.filter(ocatid=catid)

    site = Main.objects.get(pk=2)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]

    return render(request, 'front/all_news.html', {'site':site, 'news':news, 'cat':cat, 'subcat':subcat, 'lastnews':lastnews, 'popnews':popnews, 'popnews2':popnews2, 'trending':trending, 'lastnews2':lastnews2, 'allnews':allnews})

def news_publish(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    # login check end
    news = News.objects.get(pk=pk)
    news.act = 1
    news.save()
    return redirect('news_list')