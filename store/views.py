from django.shortcuts import render, redirect
from .models import Product
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import datetime
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate

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
                    is_staff=True,
                    is_active=True,
                    date_joined=datetime.datetime.now()
                )
                new_user.save()                
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