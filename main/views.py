from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.

def dashboard(request):
    context = {}
    return render(request, 'main/dashboard.html', context)


def signin(request):
    context = {}
    return render(request, 'main/signin.html', context)


def signup(request):
    context = {}
    return render(request, 'main/signup.html', context)


def create_shop(request):
    if request.method == "POST":
        shop_name = request.POST.get('shop_name')
        Store.objects.create(name=shop_name, owner=request.user)
        return redirect('dashboard')

    context = {}
    return render(request, 'main/create_shop.html', context)


def your_shops(request):
    user = request.user
    shops = user.shops.all()
    context = {'shops':shops}
    return render(request, 'main/my_shops.html', context)


def shop(request, pk):
    shop = Store.objects.get(id=pk)
    context = {}
    return render(request, 'main/shop.html', context)
 
