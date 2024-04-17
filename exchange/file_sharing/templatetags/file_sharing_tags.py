from django import template
from file_sharing.models import *

register = template.Library()


# функция для простого тега
@register.simple_tag(name='getdisciplines')
def get_disciplines(filter=None):
    if not filter:
        return Discipline.objects.all()
    else:
        return Discipline.objects.filter(pk=filter)


@register.inclusion_tag('file_sharing/list_disciplines.html')
def show_disciplines(sort=None, discipline_selected=0):
    if not sort:
        disciplines = Discipline.objects.all()
    else:
        disciplines = Discipline.objects.order_by(sort)
    return {"disciplines": disciplines, 'discipline_selected': discipline_selected}