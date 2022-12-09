from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.http import HttpResponse

# Create your views here.


def dashboard(request):

    if not request.user.is_authenticated:
        return HttpResponse('<h1 style="color:red">You are not authenticated. Use the django admin to login for now, Bernard. Also use it to add products so that you can see how it looks.</h1>')

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
        return redirect('my_shops')

    context = {}
    return render(request, 'main/create_shop.html', context)


def your_shops(request):
    user = request.user
    shops = user.shops.all()
    context = {'shops': shops}
    return render(request, 'main/my_shops.html', context)


def shop(request, pk):
    search_query = request.GET.get('q') if request.GET.get('q') != None else ''

    page = "shop"
    shop = request.user.shops.get(id=pk)
    store_products = shop.products.all()

    store_products = Product.objects.filter(Q(name__icontains=search_query))
    if search_query is not '':
        if store_products.count() == 0:
            messages.info(
                request, "No search results found. Check your spelling or try a different search.")
        else:
            messages.success(
                request, f"Search Results found: {store_products.count()}")

    context = {'products': store_products, "page": page, 'shop': shop}
    return render(request, 'main/shop.html', context)
