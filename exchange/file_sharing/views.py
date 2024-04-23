from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404
from .models import Record, Discipline
from django.views.generic import ListView, DetailView

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


class RecordHome(ListView):
    model = Record
    template_name = 'file_sharing/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # получение уже сформированного контекста для шаблона
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['discipline_selected'] = 0
        # c_def = self.get_user_context(title='Главная страница')
        # # объединение двух словарей
        # context = dict(list(context.items()) + list(c_def.items()))
        return context


# def index(request):
#     posts = Record.objects.all()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'discipline_selected': 0,
#     }
#     return render(request, 'file_sharing/index.html', context=context)


def about(request):
    return render(request, 'file_sharing/about.html', {'menu': menu, 'title': 'О сайте'})


def addpage(request):
    return HttpResponse('addpage')


def contact(request):
    return HttpResponse('contact')


def login(request):
    return HttpResponse('login')


class ShowPost(DetailView):
    model = Record
    template_name = 'file_sharing/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # получение уже сформированного контекста для шаблона
        context['menu'] = menu
        context['title'] = context['post']
        return context


# def show_post(request, post_slug):
#     post = get_object_or_404(Record, slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.description,
#         'discipline_selected': post.discipline_id,
#     }
#     return render(request, 'file_sharing/post.html', context=context)


class RecordDiscipline(ListView):
    model = Record
    template_name = 'file_sharing/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Record.objects.filter(discipline__slug=self.kwargs['discipline_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # получение уже сформированного контекста для шаблона
        context['menu'] = menu
        context['title'] = 'Дисциплина - ' + str(context['posts'][0].discipline)
        context['discipline_selected'] = context['posts'][0].discipline_id
        return context


# def show_discipline(request, discipline_id):
#     posts = Record.objects.filter(discipline_id=discipline_id)
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'discipline_selected': discipline_id,
#     }
#     return render(request, 'file_sharing/index.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
