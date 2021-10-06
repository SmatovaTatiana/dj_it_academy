from django.contrib import admin
from . import models

# Register your models here.

# admin.site.register(models.Material)
admin.site.register(models.Comment)  # регистрируем модель
admin.site.register(models.Profile)


@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'material_tape', 'publish')
    list_filter = ('material_tape', 'created')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title', )}
    ordering = ('material_tape', 'title')
