from django.db.models import Count
from django.core.cache import cache

from file_sharing.models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 5
    def get_user_context(self, **kwargs):
        context = kwargs
        # подключаем механизм кеширования
        disciplines = cache.get('disciplines')
        if not disciplines:
            disciplines = Discipline.objects.all()
            cache.set('disciplines', disciplines, 60)
        # disciplines = Discipline.objects.all() так было ДО кеширования
        context['menu'] = menu
        context['disciplines'] = disciplines
        if 'discipline_selected' not in context:
            context['discipline_selected'] = 0
        return context