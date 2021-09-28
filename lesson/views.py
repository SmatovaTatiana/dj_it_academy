from django.shortcuts import render, get_object_or_404
from . import models
# Create your views here.


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
