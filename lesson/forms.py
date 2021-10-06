from django import forms  # импортируем базовый класс для форм
from . import models
from django.contrib.auth.models import User


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


# форма для комментариев
class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('name', 'body')


# форма для регистрации
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Pass', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Pass2', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('bad password')
        return cd['password']
