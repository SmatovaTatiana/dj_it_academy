from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name = 'lesson'
urlpatterns = [
    path('', views.all_materials, name='all_materials'),
    path('<int:y>/<int:m>/<int:d>/<slug:slug>/', views.detailed_material, name='detailed_material'),
    path('<int:material_id>/share/', views.share_material, name='share_material'),    # когда дело имеем с формами, нужен / в конце первого параметра
    path('create/', views.create_material, name='create_material'),
    path('login/', views.custom_login, name='login'),
#    path('login/', auth_views.LoginView.as_view(), name='login'),
#    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
