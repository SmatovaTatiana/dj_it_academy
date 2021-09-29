from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Material(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
# уникальный двух полей: пара слаг и дата д.б. уникальны

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_created=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='user_materials')

    MATERIAL_TYPE = [
        ('theory', 'Theoretical Materials'),
        ('practice', 'Practical Materials'),
    ]

    material_tape = models.CharField(max_length=255,
                                     choices=MATERIAL_TYPE,
                                     default='theory')

    def get_absolute_url(self):
        return reverse('lesson:detailed_material',
                        args=[self.publish.year,
                              self.publish.month,
                              self.publish.day,
                              self.slug])


"""    def __str__(self):
        return self.title  # для отображения названий материалов в админке
# отключили, т.к. настроили в админке"""
