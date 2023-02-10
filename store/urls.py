from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/<int:cat_id>/products/', views.get_products_by_category, name='get_products_by_category'),
    path('products/<int:prod_id>', views.get_product_detail, name='get_product_detail'),
    path('signup/', views.signup, name='signup'),
    path('success-signup/', views.success_signup, name='success_signup'),
    path('signin/', views.do_signin, name='signin'),
    path('logout/', views.do_logout, name='logout'),
    path('add-item/', views.add_to_cart, name='add_to_cart'),
    path('remove-item/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.get_shopping_cart, name='cart'),
    path('orders/', views.create_order, name='create_order')
]