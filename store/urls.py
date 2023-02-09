from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/<int:cat_id>/products/', views.get_products_by_category, name='get_products_by_category'),
    path('products/<int:prod_id>', views.get_product_detail, name='get_product_detail'),
    path('signup/', views.signup, name='signup'),
    path('success-signup/', views.success_signup, name='success_signup'),
    path('signin/', views.do_signin, name='signin'),
    path('logout/', views.do_logout, name='logout')
]