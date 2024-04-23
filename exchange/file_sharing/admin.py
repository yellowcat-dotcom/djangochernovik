import datetime

from django.contrib import admin
from django.forms import TextInput
from django.template.defaultfilters import truncatechars
from django.utils.text import slugify
from transliterate import translit

from .models import *


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('user__first_name', 'user__last_name')
    list_display_links = ('full_name',)

    # отображение имени преподавателя
    def full_name(self, obj):
        return f'{obj.user.last_name} {obj.user.first_name} {obj.father_name}'

    full_name.short_description = 'ФИО'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('number',)
    search_fields = ('number',)


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}



class DisciplineTeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'discipline')
    list_filter = ('teacher',)
    list_display_links = ('teacher', 'discipline')
    search_fields = ('teacher__user__first_name', 'teacher__user__last_name', 'discipline__name')


class FileAdmin(admin.ModelAdmin):
    list_display = ('file',)


class FileInline(admin.StackedInline):  # (admin.StackedInline)
    model = File
    extra = 1


class RecordAdmin(admin.ModelAdmin):
    inlines = [FileInline]
    fields = ('discipline', 'group', 'description')
    list_display = ('discipline', 'teacher', 'date', 'get_group', 'short_description', 'display_files', 'slug')
    search_fields = ('discipline__name',)
    list_display_links = ('discipline', 'teacher', 'date', 'get_group', 'short_description')
    list_filter = ('discipline', 'group', 'date')


    # Отображение группы
    def get_group(self, obj):
        return ', '.join([str(group) for group in obj.group.all()])

    # отображение описания
    def short_description(self, obj):
        return truncatechars(obj.description, 20)

    def display_files(self, obj):
        return ", ".join([file.__str__() for file in obj.files.all()])

# метод для сохранения с автоматическим составлением слага
    def save_model(self, request, obj, form, change):
        if request.user.is_authenticated and hasattr(request.user, 'teacher'):
            obj.teacher = request.user.teacher

            # Получение текущей даты и времени
            current_datetime = datetime.datetime.now()

            # Транслитерация имени преподавателя на латиницу
            teacher_name = f"{translit(obj.teacher.user.last_name, 'ru', reversed=True)}-{translit(obj.teacher.user.first_name, 'ru', reversed=True)}-{translit(obj.teacher.father_name, 'ru', reversed=True)}"
            teacher_name = teacher_name.replace("'", "")
            # Транслитерация имени дисциплины на латиницу
            discipline_slug = slugify(translit(obj.discipline.name, 'ru', reversed=True))

            # Создание уникального слага на основе даты, времени, имени дисциплины и преподавателя
            if obj.discipline:
                date_slug = current_datetime.strftime('%Y-%m-%d')

                time_slug = current_datetime.strftime('%H-%M-%S')
                slug_text = f"{date_slug}-{time_slug}-{discipline_slug}_{teacher_name}"
                obj.slug = slug_text

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return qs
            elif hasattr(request.user, 'teacher'):
                return qs.filter(teacher=request.user.teacher)
        return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher' and request.user.is_authenticated and hasattr(request.user, 'teacher'):
            kwargs['queryset'] = Teacher.objects.filter(id=request.user.teacher.id)
            kwargs['initial'] = request.user.teacher.id
        elif db_field.name == 'discipline' and request.user.is_authenticated and hasattr(request.user, 'teacher'):
            kwargs['queryset'] = Discipline.objects.filter(disciplineteacher__teacher=request.user.teacher)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    get_group.short_description = 'Группы'
    short_description.short_description = 'Описание'


# Register your models here.
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(DisciplineTeacher, DisciplineTeacherAdmin)
# admin.site.register(File, FileAdmin)
admin.site.register(Record, RecordAdmin)

admin.site.site_header = 'Привет преподаватель!'
admin.site.index_title = 'Добро пожаловать в файлообменник'
