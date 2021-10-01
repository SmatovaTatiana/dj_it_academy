from django import forms  # импортируем базовый класс для форм
from . import models


class EmailMaterialForm(forms.Form):  # класс унаследуем от спец.класса
    name = forms.CharField(max_length=255)             # имя отправителя
    to_email = forms.EmailField()                      # кому
    comment = forms.CharField(required=False,          # комментарий. Необязательное поле
                              widget=forms.Textarea)
# виджет - спец.функционал, кот. позволяет интерактивные взаимодействия


class MaterialForm(forms.ModelForm):
    class Meta:
        model = models.Material
        fields = ('title', 'body', 'material_tape')

# форма для авторизации пользователей
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
