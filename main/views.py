from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('signup')
    context = {}
    return render(request, 'main/dashboard.html', context)


def signin(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            if not User.objects.filter(email=email).exists():
                context.update(
                    {'title': 'username', 'message': 'username does not exist.', 'POST': 'true'})
            else:
                context.update(
                    {'title': 'password', 'message': 'incorrect password.', 'POST': 'true'})

    return render(request, 'main/signin.html', context)


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    context = {'form': form}
    return render(request, 'main/signup.html', context)


def signout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def create_shop(request):
    if request.method == "POST":
        shop_name = request.POST.get('shop_name').rstrip().upper()
        Store.objects.create(name=shop_name, owner=request.user)
        return redirect('my_shops')

    context = {}
    return render(request, 'main/create_shop.html', context)

all_shops = False

@login_required(login_url='signin')
def your_shops(request):
    user = request.user
    shops = user.shops.all()
    search_query = request.GET.get('q') if request.GET.get('q') != None else ''
    if search_query != '':
        shops = shops.filter(Q(name__icontains=search_query))
        if shops.count() == 0:
            messages.info(
                request, "You have no such shops.")
        else:
            messages.success(
                request, f'Search results for "{search_query}" found: {shops.count()}')
    elif search_query == '' and shops.count() == 0:
        messages.error(request, "You don't have any shops")
    context = {'shops': shops, 'search_query': search_query}
    return render(request, 'main/my_shops.html', context)


@login_required(login_url='signin')
def shop(request, pk):
    all_shops = True
    if request.META.get('HTTP_REFERER') == 'http://127.0.0.1:8000/my_shops':
        all_shops = False
    context = {}
    search_query = request.GET.get('q') if request.GET.get('q') != None else ''
    page = "shop"
    shop = Store.objects.get(id=pk)
    user_cart_products = []
    if shop.owner != request.user:
        user_cart_products = request.user.carts.get(store=shop).products.all()
    context['user_cart_products'] = user_cart_products
    store_products = shop.products.all()  # type: ignore
    if search_query != '':
        store_products = Product.objects.filter(
            Q(name__icontains=search_query))
        if store_products.count() == 0:
            messages.info(
                request, "No search results found. Check your spelling or try a different search.")
        else:
            messages.success(
                request, f"Search Results found: {store_products.count()}")

    context = {'products': store_products, "page": page, 'shop': shop, 'all_shops':all_shops, 'user_cart_products':user_cart_products}
    user = request.user
    try:
        context['cart_product_count'] = user.carts.get(store=shop).products.count()
    except:
        context['cart_product_count'] = 0
    return render(request, 'main/shop.html', context)


@login_required(login_url='signin')
def add_product(request, store_id):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = request.user.shops.get(id=store_id)
            product.save()
            messages.success(
                request, f'The product "{product.name}" was added successfully!')
            return redirect('shop', store_id)
        else:
            messages.error(request, 'An error occurred!')
    context = {'form': form}
    return render(request, 'main/add_product.html', context)


@login_required(login_url='signin')
def edit_product(request, product_id):
    page = 'edit'
    product = Product.objects.get(id=product_id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'The product "{request.POST.get("name")}" was changed successfully!')
            return redirect('shop', product.store.pk)
    context = {'form': form, 'page': page}
    return render(request, 'main/edit_product.html', context)


@login_required(login_url='signin')
def view_shops(request):
    shops = Store.objects.all()
    search_query = request.GET.get('q') if request.GET.get('q') != None else ''
    if search_query != '':
        shops = Store.objects.filter(Q(name__icontains=search_query))
        if shops.count() == 0:
            messages.info(
                request, "No such shops found. Check your spelling or try a different search.")
        else:
            messages.success(
                request, f'Search results for "{search_query}" found: {shops.count()}')
    elif search_query == '' and shops.count() == 0:
        messages.error(request, "No shops available")
    context = {'shops': shops, 'search_query': search_query}
    return render(request, 'main/all_shops.html', context)


@login_required(login_url='signin')
def delete_shop(request, pk):
    shop = Store.objects.get(id=pk)
    if shop.owner != request.user:
        return redirect('my_shops')
    shop.delete()
    messages.success(
        request, f'The shop "{shop.name}" was deleted successfully!')
    return redirect('my_shops')


@login_required(login_url='signin')
def cart(request, store_id):
    page = 'cart'
    store = Store.objects.get(id=store_id)
    cart = request.user.carts.get(store=store)
    cart_products = cart.products.all()

    cart_product_count = cart_products.count()
    total_price = cart.calc_price()

    context = {'products': cart_products,
               'cart_product_count': cart_product_count, 'total': total_price, 'page': page}
    return render(request, 'main/cart.html', context)


@login_required(login_url='signin')
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = request.user.carts.get(store=product.store)
    except:
        cart = Cart.objects.create(user=request.user, store=product.store)

    cart.products.add(product)
    return redirect('shop', product.store.pk)


@login_required(login_url='signin')
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = request.user.carts.get(store=product.store)
    except:
        cart = Cart.objects.create(user=request.user, store=product.store)

    cart.products.remove(product)
    return redirect('cart', product.store.pk)


def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.store.owner != request.user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    product.delete()
    messages.success(
        request, f'The product "{product.name}" was deleted successfully! ')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
