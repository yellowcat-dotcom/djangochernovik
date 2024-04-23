from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, unique=True,
                                verbose_name='Пользователь')
    father_name = models.CharField(max_length=50, verbose_name='Отчество')
    disciplines = models.ManyToManyField('Discipline', through='DisciplineTeacher', blank=True)

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name} {self.father_name}'

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Group(models.Model):
    number = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': False}, unique=True,
                                  verbose_name='Номер')

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Discipline(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название', db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('discipline', kwargs={'discipline_id': self.pk})

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'


class DisciplineTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель')
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, verbose_name='Дисциплина')

    def __str__(self):
        return f'{self.teacher} - {self.discipline}'

    class Meta:
        verbose_name = 'Дисциплина-Преподаватель'
        verbose_name_plural = 'Дисциплина-Преподаватель'


class Record(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='records',
                                   verbose_name='Дисциплина')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    group = models.ManyToManyField(Group, verbose_name='Группа')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Преподаватель')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def formatted_date(self):
        return timezone.localtime(self.date).strftime('%d.%m.%Y %H:%M')

    def __str__(self):
        return f'{self.discipline} - {self.group} - {self.formatted_date()}'

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-date']


class File(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='files', verbose_name='Описание')
    file = models.FileField(upload_to='files/%Y/%m/%d/', verbose_name='Файл')

    def __str__(self):
        return str(self.file)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
