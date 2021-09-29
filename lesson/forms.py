from django import forms  # импортируем базовый класс для форм


class EmailMaterialForm(forms.Form):  # класс унаследуем от спец.класса
    name = forms.CharField(max_length=255)             # имя отправителя
    to_email = forms.EmailField()                      # кому
    comment = forms.CharField(required=False,          # комментарий. Необязательное поле
                              widget=forms.Textarea)
# виджет - спец.функционал, кот. позволяет интерактивные взаимодействия
