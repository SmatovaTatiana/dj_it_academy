from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from . import models
from . import forms

# Create your views here.
# константы выносим в начало файла
SUBJECT = ' {name} Wants to share material "{title}" with you.'
BODY = ("{title} at {uri}. {name} shared material with you. Please take "
        "a look at it. {name} has provided "
        "next comment: {comment} ")


def all_materials(request):
    materials = models.Material.objects.all()
    return render(request, "materials/all_materials.html",
                  {'materials': materials})


def detailed_material(request, y, m, d, slug):
    material = get_object_or_404(models.Material,
                                 publish__year=y,
                                 publish__month=m,
                                 publish__day=d,
                                 slug=slug)
    return render(request, "materials/detailed_material.html",
                  {"material": material})


# обработчик формы отправки почты


def share_material(request, material_id):
    material = get_object_or_404(models.Material, id=material_id)

    sent = False  # инициализируем флаг, используется при отправке формы

    if request.method == "POST":  # проверяем метод
        form = forms.EmailMaterialForm(request.POST)  # получаем объект формы из запроса
        if form.is_valid():  # валидируем форму:
            cd = form.cleaned_data  # работаем с данными, прошедшими валидацию
            uri = request.build_absolute_uri(
                material.get_absolute_url(),
            )
            subject = SUBJECT.format(name=cd['name'],
                                     title=material.title)
            body = BODY.format(title=material.title,
                               uri=uri,
                               name=cd['name'],
                               comment=cd['comment'],
                               )
            send_mail(subject, body, 'admin@my.com', [cd['to_email'], ])
            sent = True  # добавляем флаг, используется при отправке формы
    else:
        form = forms.EmailMaterialForm()    # если не post запрос, создаем пустой объект формы

    return render(request,    # передаем запрос
                  "materials/share.html",    # передаем страничку
                  {'material': material, 'form': form})    # передаем контекст (материал и форму)
