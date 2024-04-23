from django.db.models import Count

from file_sharing.models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        disciplines = Discipline.objects.all()
        context['menu'] = menu
        context['disciplines'] = disciplines
        if 'discipline_selected' not in context:
            context['discipline_selected'] = 0
        return context
