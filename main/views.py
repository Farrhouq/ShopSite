from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.http import HttpResponse
from .forms import *

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
    search_query = request.GET.get('q') if request.GET.get('q') != None else ''
    if search_query != '':
        shops = shops.filter(Q(name__icontains=search_query))
        if shops.count() == 0:
            messages.info(
                request, "No shops found. Check your spelling or try a different search.")
        else:
            messages.success(
                request, f'Search results for "{search_query}" found: {shops.count()}')
    context = {'shops': shops}
    return render(request, 'main/my_shops.html', context)


def shop(request, pk):
    search_query = request.GET.get('q') if request.GET.get('q') != None else ''
    page = "shop"
    shop = Store.objects.get(id=pk)
    store_products = shop.products.all()
    if search_query != '':
        store_products = Product.objects.filter(Q(name__icontains=search_query))
        if store_products.count() == 0:
            messages.info(
                request, "No search results found. Check your spelling or try a different search.")
        else:
            messages.success(
                request, f"Search Results found: {store_products.count()}")

    context = {'products': store_products, "page": page, 'shop': shop}
    if shop.owner == request.user:
        return render(request, 'main/shop.html', context)
    return render(request, 'main/shop_.html', context)


def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=True)
            messages.success(
                request, f'The product "{product.name}" was added successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'An error occurred!')
    context = {'form': form}
    return render(request, 'main/add.html', context)


def edit_product(request, pk):
    page = 'edit'
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'The product {request.POST.get("name")} was changed successfully!')
            return redirect('shop')
    context = {'form': form, 'page': page}
    return render(request, 'main/edit.html', context)


def view_shops(request):
    shops = Store.objects.all()
    search_query = request.GET.get('q') if request.GET.get('q') != None else ''
    if search_query != '':
        shops = Store.objects.filter(Q(name__icontains=search_query))
        if shops.count() == 0:
            messages.info(
                request, "No shops found. Check your spelling or try a different search.")
        else:
            messages.success(
                request, f'Search results for "{search_query}" found: {shops.count()}')
    context = {'shops': shops}
    return render(request, 'main/all_shops.html', context)


def delete_shop(request, pk):
    shop = Store.objects.get(id=pk)
    if shop.owner != request.user:
        return redirect('my_shops')
    shop.delete()
    messages.success(
        request, f'The shop "{shop.name}" was deleted successfully!')
    return redirect('my_shops')


def cart(request):
    page = 'cart'
    cart = request.user.cart
    cart_products = cart.products.all()
    products = []

    cart_product_count = cart_products.count()
    total_price = cart.calc_price()

    context = {'products': cart_products,
               'cart_product_count': cart_product_count, 'total': total_price, 'page': page}
    return render(request, 'cart.html', context)


def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    cart = request.user.cart
    cart.products.add(product)
    return redirect('home')


def remove_from_cart(request, pk):
    product = Product.objects.get(id=pk)
    cart = request.user.cart
    cart.products.remove(product)
    return redirect('cart')
