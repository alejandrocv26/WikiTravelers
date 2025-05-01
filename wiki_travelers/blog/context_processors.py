from .models import Country

def navbar_context(request):
    return {'cat_menu': Country.objects.all(), }