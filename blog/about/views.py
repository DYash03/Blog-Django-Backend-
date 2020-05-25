from django.shortcuts import render
from . models import Author
# Create your views here.


def author(request, slug):
    auth = Author.objects.get(slug=slug)
    auth = {"auth": auth}
    return render(request, 'about/author.html', auth)


def about(request):
    auth = Author.objects.all()
    auth = {"auth": auth}
    return render(request, 'about/about.html', auth)
