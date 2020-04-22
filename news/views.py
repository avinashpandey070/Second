from django.shortcuts import render, get_object_or_404, redirect
from app1.models import Main
from news.models import News
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat

# Create your views here.

def news_detail(request, word):
    site = Main.objects.get(pk=2)
    news = News.objects.filter(name=word)
    return render(request, 'front/news_detail.html', {'news': news, 'site': site})


def news_list(request):
    news = News.objects.all()
    return render(request, 'back/news_lists.html', {'news': news})


def news_add(request):
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
    cat = SubCat.objects.all()
    if request.method == 'POST':
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstextshort = request.POST.get('newstextshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')

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
                    b = News(name=newstitle, short_text=newstextshort, body_text=newstxt, date=today, time=time,
                             picname=filename, picurl=url, writer='-', catname=newsname, catid=newsid, show=0)
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
    try:
        b = News.objects.get(pk=pk)
        fs = FileSystemStorage()
        fs.delete(b.picname)
        b.delete()
    except:
        error = 'Something wrong'
        return render(request, 'back/error.html', {'error': error})
    return redirect(news_list)

def news_edit(request, pk):
    news = News.objects.get(pk=pk)
    return render(request, 'back/news_edit.html', {'news':news})