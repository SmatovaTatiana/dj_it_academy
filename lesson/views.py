from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse  # возвращает ответ
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect

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


@login_required  # ограничиваем доступ
def detailed_material(request, y, m, d, slug):
    material = get_object_or_404(models.Material,
                                 publish__year=y,
                                 publish__month=m,
                                 publish__day=d,
                                 slug=slug)
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.material = material
            comment.save()
            return redirect(material)

    else:
        form = forms.CommentForm()

    return render(request, "materials/detailed_material.html",
                  {"material": material, 'form': form})


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
        form = forms.EmailMaterialForm()  # если не post запрос, создаем пустой объект формы

    return render(request,  # передаем запрос
                  "materials/share.html",  # передаем страничку
                  {'material': material, 'form': form, 'sent': sent})  # передаем контекст (материал и форму)


def create_material(request):
    if request.method == "POST":
        material_form = forms.MaterialForm(request.POST)
        if material_form.is_valid():
            new_material = material_form.save(commit=False)
            new_material.author = User.objects.first()
            new_material.slug = new_material.title.replace(" ", "-")
            new_material.save()

            return render(request, "materials/detailed_material.html",
                          {"material": new_material})

    else:
        material_form = forms.MaterialForm()

    return render(request,
                  'materials/create.html',
                  {'form': material_form})


def custom_login(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'],
                password=cd['password'],
            )
            if user is not None:  # используется None, а не if not user т.к. могут быть анонимные юзеры, юзер есть,
                # но прав нет и т.д. Если использовать if user, могут быть проблемы с незакончившими регистрацию и т.д.
                if user.is_active:  # флаг. При нормальной регистрации с уведомлением на почту
                    login(request, user)
                    # from request берутся данные о клиенте и говорится, что это он этот user, после этого он залогинен
                    return HttpResponse('logged in')
                else:
                    return HttpResponse('User not active')
            else:
                return HttpResponse('Bad credentials')

    else:
        form = forms.LoginForm()
    return render(request,
                  'login.html',  # в корне, т.к. к приложению напрямую не относится
                  {'form': form})


def profile(request):
    return render(request, "profile.html", {'user': request.user})


def register(request):
    if request.method == "POST":
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.save()
            models.Profile.objects.create(user=new_user)

            return render(request, "registration_complete.html",
                          {"user": new_user})

    else:
        form = forms.UserRegistrationForm()
        return render(request, "register.html", {'form': form})


def edit_profile(request):
    if request.method == "POST":
        user_form = forms.UserEditForm(request.POST, instance=request.user)
        profile_form = forms.ProfileEditForm(request.POST,
                                             instance=request.user.profile,
                                             files=request.FILES)
        if all((user_form.is_valid(), profile_form.is_valid())):
            user_form.save()
            if not profile_form.cleaned_data['photo']:
                profile_form.cleaned_data['photo'] = request.user.profile.photo
            profile_form.save()
            return render(request, "profile.html", {'user': request.user})

    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(request.POST, instance=request.user.profile)

    return render(request, "edit_profile.html", {'user_form': user_form,
                                                 'profile_form': profile_form})
