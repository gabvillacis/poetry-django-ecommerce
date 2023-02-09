from .models import Category

def get_all_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}