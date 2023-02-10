from django.shortcuts import render, redirect
from .models import *
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import datetime
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .cart_session import ShoppingCartSession
import json
from django.http import JsonResponse
from django.db import transaction

# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'catalog.html', {'product_list': products})

def get_products_by_category(request, cat_id):
    products = Product.objects.filter(categories__in=[cat_id])
    return render(request, 'catalog.html', {'product_list': products})

def get_product_detail(request, prod_id):
    try:
        product = Product.objects.get(pk=prod_id)
        return render(request, 'product_detail.html', {'product': product})
    except Product.DoesNotExist:
        return render(request, '404.html')    

def signup(request):    
    if request.method == "POST":        
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            username = sign_up_form.cleaned_data['username']
            password = sign_up_form.cleaned_data['password1']
            first_name = sign_up_form.cleaned_data['first_name']
            last_name = sign_up_form.cleaned_data['last_name']
            email = sign_up_form.cleaned_data['email']
            country = sign_up_form.cleaned_data['country']
            city = sign_up_form.cleaned_data['city']
            address = sign_up_form.cleaned_data['address']
            cellphone = sign_up_form.cleaned_data['cellphone']
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "El username ingresado ya está siendo utilizado!")
            else:            
                new_user = User(
                    username=username,
                    password=make_password(password),
                    is_superuser=False,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    is_staff=False,
                    is_active=True,
                    date_joined=datetime.datetime.now()
                )
                new_user.save()
                
                address = Address(user=new_user,
                                  country=country,
                                  city=city,
                                  address=address,
                                  cellphone=cellphone)                
                address.save()
                                
                return redirect('success_signup')
    else:
        sign_up_form = SignUpForm()        
    
    return render(request, 'signup.html', {'sign_up_form': sign_up_form})

def success_signup(request):
    return render(request, 'success_signup.html')

def do_signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Usuario o contraseña inválidos.")
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
    
    auth_form = AuthenticationForm()
    return render(request, "signin.html", context={'signin_form': auth_form})

def do_logout(request): 
    logout(request)    
    return redirect('index')

def add_to_cart(request):
    cart = ShoppingCartSession(request)
    
    payload = json.loads(request.body)
    product_id = int(payload.get('product_id'))
    quantity = int(payload.get('quantity'))
    
    try:
        existing_product = Product.objects.get(pk=product_id)
        cart.add(existing_product.id, quantity=quantity)
        return JsonResponse(status=200, data={'result': True, 'message': 'OK', 'count_items': cart.__len__()})
    except Product.DoesNotExist:
        return JsonResponse(status=400, data={'result': False, 'message': 'El producto no existe.'})
    
def remove_from_cart(request):
    cart = ShoppingCartSession(request)
    
    payload = json.loads(request.body)
    product_id = int(payload.get('product_id'))
    
    cart.delete(product_id)
    return JsonResponse(status=200, data={'result': True, 'message': 'OK', 'count_items': cart.__len__()})

def get_shopping_cart(request):
    cart = ShoppingCartSession(request)    
    return render(request, 'cart.html', {'cart': cart.get_cart_detail(), 'cart_items': cart.__len__(), 'cart_total': cart.get_total()})

@transaction.atomic
def create_order(request):
    cart = ShoppingCartSession(request)  
    
    if cart.__len__() == 0:
        messages.error(request, "No ha añadido items en el carrito, está vacío.")
    else:
        try:
            
            address = Address.objects.get(user=request.user)            
            order = Order(  user=request.user,
                            address=address,
                            total_amount=cart.get_total())
            order.save()

            for item in cart.get_cart_detail():
                order_item = OrderItem( order=order,
                                        product=item['product'],
                                        quantity=item['quantity'])
                order_item.save()
                
            cart.clear()
            return JsonResponse(data={"order_id": order.id}, status=201)
        except Exception as error:
            return JsonResponse(data={"error_msg": "Opps, su pedido no pudo ser ingresado. " + repr(error)}, status=500)