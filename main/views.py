from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.http import HttpResponseRedirect
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('signup')
    context = {'username': request.user.username}
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
        if request.user.shops.filter(name=shop_name).exists():
            messages.error(
                request, "A shop of this name already exists on this account.")
        else:
            Store.objects.create(name=shop_name, owner=request.user)
            return redirect('my_shops', request.user.username)
    return render(request, 'main/create_shop.html', {})


@login_required(login_url='signin')
def your_shops(request, username):
    user = User.objects.get(username=username)
    if not user == request.user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return redirect('dashboard')
    # user = request.user
    shops = user.shops.all()  # type: ignore
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
def edit_shop(request, username, shop_name):
    shop = request.user.shops.get(name=shop_name)
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        if shop_name:
            shop.name = shop_name
        shop.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def shop(request, username, shop_name):
    user = User.objects.get(username=username)
    shop = user.shops.get(name=shop_name)  # type: ignore
    context = {}
    # cart = request.user.carts.get(store=shop)

    has_cart = False
    user_cart_products = []
    if request.user.is_authenticated:
        has_cart = request.user.carts.filter(store=shop).exists()

    if has_cart:
        user_cart_products = request.user.carts.get(store=shop).products.all()
    context['user_cart_products'] = user_cart_products

    search_query = request.GET.get('q') if request.GET.get('q') != None else ''
    store_products = shop.products.all()  # type: ignore
    if search_query != '':
        store_products = shop.products.filter(  # type: ignore
            Q(name__icontains=search_query))
        if store_products.count() == 0:
            messages.info(
                request, "No search results found. Check your spelling or try a different search.")
        else:
            messages.success(
                request, f"Search Results found: {store_products.count()}")

    context = {'products': store_products, 'shop': shop,
               'user_cart_products': user_cart_products, 'has_cart': has_cart, 'cart': cart}
    user = request.user
    try:
        context['cart_product_count'] = user.carts.get(
            store=shop).products.count()
    except:
        context['cart_product_count'] = 0
    return render(request, 'main/shop.html', context)


@login_required(login_url='signin')
def add_product(request, username, shop_name):
    user = User.objects.get(username=username)
    shop = user.shops.get(name=shop_name)  # type: ignore
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # n = int(request.POST.get('n'))
            # for i in range(n):
            #     detail = request.POST.get('det_'+str(i))
            #     value = request.POST.get('val_'+str(i))
            #     product.product_details[detail] = value
            product.store = shop
            product.save()
            messages.success(
                request, f'The product "{product.name}" was added successfully!')
            return redirect('shop', username, shop_name)
        else:
            messages.error(request, 'An error occurred!')
    context = {'form': form, 'shop': shop}
    return render(request, 'main/add_product.html', context)


@login_required(login_url='signin')
def edit_product(request, username, shop_name, product_id):
    user = User.objects.get(username=username)
    shop = user.shops.get(name=shop_name)  # type:ignore
    product = shop.products.get(id=product_id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            if request.FILES.get('product_picture') is not None:
                product.image = request.FILES.get('product_picture')
                product.save()
            # n = int(request.POST.get('n'))
            # for i in range(n):
            #     detail = request.POST.get('det_'+str(i))
            #     value = request.POST.get('val_'+str(i))
            #     product.product_details[detail] = value
            form.save()
            messages.success(
                request, f'The product "{request.POST.get("name")}" was changed successfully!')
            return redirect('shop', product.store.pk)
    context = {'form': form, 'product': product}
    return render(request, 'main/edit_product.html', context)


# @login_required(login_url='signin')
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
def delete_shop(request, username, shop_name):
    user = User.objects.get(username=username)
    try:
        shop = user.shops.get(name=shop_name)  # type: ignore
        shop.delete()
        messages.success(
            request, f'The shop "{shop.name}" was deleted successfully!')
    except:
        pass
    return redirect('my_shops', user.username)


@login_required(login_url='signin')
def cart(request, username, shop_name):
    page = 'cart'
    user = User.objects.get(username=username)
    shop = user.shops.get(name=shop_name)  # type: ignore
    cart = request.user.carts.get(store=shop)
    cart_products = cart.products.all()

    search_query = request.GET.get('q') if request.GET.get('q') != None else ''
    if search_query != '':
        cart_products = cart.products.filter(  # type: ignore
            Q(name__icontains=search_query))
        if cart_products.count() == 0:
            messages.info(
                request, "No search results found. Check your spelling or try a different search.")
        else:
            messages.success(
                request, f"Search results found: {cart_products.count()}")

    cart_product_count = cart_products.count()
    total_price = cart.calc_price()

    context = {'products': cart_products,
               'cart_product_count': cart_product_count,
               'total': total_price, 'page': page,
               'cart': cart, 'shop': shop}
    return render(request, 'main/cart.html', context)


@login_required(login_url='signin')
def add_to_cart(request, username, shop_name, product_id):
    user = User.objects.get(username=username)
    shop = user.shops.get(name=shop_name)  # type: ignore
    product = shop.products.get(id=product_id)
    if request.user == shop.owner:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    try:
        cart = request.user.carts.get(store=product.store)
    except:
        cart = Cart.objects.create(user=request.user, store=product.store)

    if ProductOrder.objects.filter(cart=cart, product=product).exists():
        order = ProductOrder.objects.get(cart=cart, product=product)

        if order in cart.products.all():
            if order.product.stock is not None and order.quantity < order.product.stock:
                order.quantity += 1
                order.save()
        else:
            order.quantity = 1
            order.save()
            cart.products.add(order)

    else:
        order = ProductOrder.objects.create(
            cart=cart, product=product, quantity=1)
        cart.products.add(order)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return redirect('cart', username, shop_name)


@login_required(login_url='signin')
def decrease_order_quantity(request, store_name, pk):
    order = ProductOrder.objects.get(id=pk)
    if not order.cart.user == request.user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if order.quantity > 1:
        order.quantity -= 1
        order.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return redirect('cart', order.cart.store.owner.username, order.cart.store.name)


@login_required(login_url='signin')
def remove_from_cart(request, username, shop_name, product_id):
    user = User.objects.get(username=username)
    shop = user.shops.get(name=shop_name)  # type: ignore
    product = shop.products.get(id=product_id)
    try:
        cart = request.user.carts.get(store=product.store)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    product_order = ProductOrder.objects.get(cart=cart, product=product)

    if product_order in cart.products.all():
        if product_order.quantity > 1:
            product_order.quantityk -= 1 
            product_order.save()
        else:
            cart.products.remove(product_order)
            messages.success(request, f'The product "{product.name}" was removed from your cart.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return redirect('cart', user.username, shop.name)


@login_required(login_url='signin')
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.store.owner != request.user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    product.delete()
    messages.success(
        request, f'The product "{product.name}" was deleted successfully! ')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def preview(request, username, shop_name, product_id):
    user = User.objects.get(username=username)
    shop = user.shops.get(name=shop_name)  # type: ignore
    product = shop.products.get(id=product_id)  # type: ignore
    context = {'shop': shop, 'product': product}
    return render(request, 'main/preview.html', context)


@login_required(login_url='signin')
def orders(request, shop_name):
    store = Store.objects.get(name=shop_name)
    orders = Store.orders.all()  # type: ignore
    context = {'store': store, 'orders': orders}

    return render(request, 'main/orders.html', context)


@login_required(login_url='signin')
def place_order(request, username, shop_name):
    user = User.objects.get(username=username)
    shop = user.shops.get(name=shop_name)
    products = request.GET.get('products')
    if products == '*cart':
        try:
            cart = request.user.carts.get(store=shop)
            products = cart.products.all()
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    pickup_stations = PickupStation.objects.all()

    if request.method == 'POST':
        this_user = request.user
        this_username = request.POST.get('username')
        pickup_station = request.POST.get('pickup_station')
        Order.objects.create(
            user=this_user, username=this_username, products_ordered=products, 
            pickup_station=pickup_station, store=shop
        )
        messages.success(request, "Your order has been placed successfully.")
        return redirect('shop', username, shop_name)

    context = {'shop': shop, 'pickup_stations': pickup_stations,'products': products}
    return render(request, 'main/place_order.html', context)
