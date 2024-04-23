from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404
from .models import Record, Discipline

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


def index(request):
    posts = Record.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница',
        'discipline_selected': 0,
    }
    return render(request, 'file_sharing/index.html', context=context)


def about(request):
    return render(request, 'file_sharing/about.html', {'menu': menu, 'title': 'О сайте'})


def addpage(request):
    return HttpResponse('addpage')


def contact(request):
    return HttpResponse('contact')


def login(request):
    return HttpResponse('login')


def show_post(request, post_slug):
    post = get_object_or_404(Record, slug=post_slug)
    context = {
        'post': post,
        'menu': menu,
        'title': post.description,
        'discipline_selected': post.discipline_id,
    }
    return render(request, 'file_sharing/post.html', context=context)


def show_discipline(request, discipline_id):
    posts = Record.objects.filter(discipline_id=discipline_id)

    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница',
        'discipline_selected': discipline_id,
    }
    return render(request, 'file_sharing/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
