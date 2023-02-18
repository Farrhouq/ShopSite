from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Q, F
from django.http import HttpResponseRedirect
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.views.generic import ListView, FormView, View
import datetime


# Create your views here.


def filter_by_slug(username, shop_slug):
    user = User.objects.get(username=username)
    shops = []
    for shop in user.shops:
        if shop.get_slug() == shop_slug:
            shops.append(shop)
    return shops


def get_by_slug(username, shop_slug):
    user = User.objects.get(username=username)
    for shop in user.shops.all():
        if shop.get_slug() == shop_slug:
            return shop


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "main/landing-page.html")


def my_cart(request):
    carts = [cart for cart in request.user.carts.all() if cart.products.count() != 0]
    context = {"carts": carts}
    return render(request, "main/general_cart.html", context)


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("signup")
    context = {}
    # messages.info(request, 'You have been logged in!')
    return render(request, "main/dashboard.html", context)


def signin(request):
    next = request.GET.get("next")

    context = {"next": next}
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            next = request.POST.get("next")
            if next != "None":
                return redirect(next)
            return redirect("dashboard")
        else:
            if not User.objects.filter(email=email).exists():
                context.update(
                    {
                        "title": "username",
                        "message": "username does not exist.",
                        "POST": "true",
                    }
                )
            else:
                context.update(
                    {
                        "title": "password",
                        "message": "incorrect password.",
                        "POST": "true",
                    }
                )
    return render(request, "main/signin.html", context)


def signup(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
    context = {"form": form}
    return render(request, "main/signup.html", context)


def signout(request):
    logout(request)
    return redirect("signin")


@login_required(login_url="signin")
def create_shop(request):
    if request.method == "POST":
        shop_name = request.POST.get("shop_name").rstrip().upper()
        shop_picture = request.FILES.get("shop_picture")
        shop_category = request.POST.get("shop_category")
        if request.user.shops.filter(name=shop_name).exists():
            messages.error(
                request, "A shop of this name already exists on this account."
            )
        else:
            Store.objects.create(
                name=shop_name,
                owner=request.user,
                picture=shop_picture,
                category=shop_category,
            )
            return redirect("my_shops", request.user.username)
    return render(request, "main/create_shop.html", {})


@login_required(login_url="signin")
def your_shops(request, username):
    user = User.objects.get(username=username)
    if not user == request.user:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        # return redirect('dashboard')
    # user = request.user
    shops = user.shops.all()  # type: ignore
    search_query = request.GET.get("q") if request.GET.get("q") != None else ""
    if search_query != "":
        shops = shops.filter(Q(name__icontains=search_query))
        if shops.count() == 0:
            messages.info(request, "You have no such shops.")
        else:
            messages.success(
                request, f'Search results for "{search_query}" found: {shops.count()}'
            )
    elif search_query == "" and shops.count() == 0:
        messages.error(request, "You don't have any shops")
    context = {"shops": shops, "search_query": search_query}
    return render(request, "main/my_shops.html", context)


@login_required(login_url="signin")
def edit_shop(request, username, shop_slug):
    shop = request.user.shops.get(name=shop_slug)
    shop = get_by_slug(username, shop_slug)
    if request.method == "POST":
        shop_slug = request.POST.get("shop_slug")
        shop_picture = request.FILES.get("shop_picture")
        if shop_slug:
            shop.name = shop_slug
        if shop_picture:
            shop.picture = shop_picture
        shop.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def shop(request, username, shop_slug):
    user = User.objects.get(username=username)
    # shop = user.shops.get(name=shop_slug)
    shop = get_by_slug(username, shop_slug)  # type: ignore
    context = {}
    # cart = request.user.carts.get(store=shop)

    has_cart = False
    user_cart_products = []
    if request.user.is_authenticated:
        has_cart = request.user.carts.filter(store=shop).exists()

    if has_cart:
        user_cart_products = request.user.carts.get(store=shop).products.all()
    context["user_cart_products"] = "user_cart_products"
    context["my_slug"] = "beans"

    search_query = request.GET.get("q") if request.GET.get("q") != None else ""
    store_products = shop.products.all()  # type: ignore
    if search_query != "":
        store_products = shop.products.filter(  # type: ignore
            Q(name__icontains=search_query)
        )
        if store_products.count() == 0:
            messages.info(
                request,
                "No search results found. Check your spelling or try a different search.",
            )
        else:
            messages.success(request, f"Search Results found: {store_products.count()}")

    context = {
        "products": store_products,
        "shop": shop,
        "user_cart_products": user_cart_products,
        "has_cart": has_cart,
        "cart": cart,
    }
    user = request.user
    try:
        context["cart_product_count"] = user.carts.get(store=shop).products.count()
    except:
        context["cart_product_count"] = 0
    return render(request, "main/shop.html", context)


@login_required(login_url="signin")
def add_product(request, username, shop_slug):
    user = User.objects.get(username=username)
    # shop = user.shops.get(name=shop_slug)
    shop = get_by_slug(username, shop_slug)  # type: ignore
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            n = int(request.POST.get("n"))
            details = {}
            for i in range(1, n + 1):
                detail = request.POST.get("det_" + str(i))
                value = request.POST.get("val_" + str(i))
                if detail != "" and value != "":
                    details[detail] = value
            product.product_details = details
            product.store = shop
            product.save()
            messages.success(
                request, f'The product "{product.name}" was added successfully!'
            )
            return redirect("shop", username, shop_slug)
        else:
            messages.error(request, "An error occurred!")
    context = {"form": form, "shop": shop}
    return render(request, "main/add_product.html", context)


@login_required(login_url="signin")
def edit_product(request, username, shop_slug, product_id):
    user = User.objects.get(username=username)
    # shop = user.shops.get(name=shop_slug)
    shop = get_by_slug(username, shop_slug)  # type:ignore
    product = shop.products.get(id=product_id)
    form = ProductForm(instance=product)
    dict_tuple = []
    i = 0
    if product.product_details is not None:
        for key in product.product_details:
            i += 1
            dict_tuple.append((key, product.product_details[key], i))
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            n = int(request.POST.get("n"))
            details = {}
            for i in range(1, n + 1):
                detail = request.POST.get("det_" + str(i))
                value = request.POST.get("val_" + str(i))
                if detail != "" and value != "":
                    details[detail] = value
            product.product_details = details
            product.save()
            form.save()
            messages.success(
                request,
                f'The product "{request.POST.get("name")}" was changed successfully!',
            )
            return redirect("shop", product.store.owner, product.store.name)
    context = {"form": form, "product": product, "dict_tuple": dict_tuple}
    return render(request, "main/edit_product.html", context)


# @login_required(login_url='signin')
def view_shops(request):
    shops = Store.objects.all()
    search_query = request.GET.get("q") if request.GET.get("q") != None else ""
    if search_query != "":
        shops = Store.objects.filter(
            Q(name__icontains=search_query) | Q(category__icontains=search_query)
        )
        if shops.count() == 0:
            messages.info(
                request,
                "No such shops found. Check your spelling or try a different search.",
            )
        else:
            messages.success(
                request, f'Search results for "{search_query}" found: {shops.count()}'
            )
    elif search_query == "" and shops.count() == 0:
        messages.error(request, "No shops available")
    context = {"shops": shops, "search_query": search_query}
    return render(request, "main/all_shops.html", context)


def view_products(request):
    products = Product.objects.all()
    not_searching = True
    search_query = request.GET.get("q") if request.GET.get("q") != None else ""
    if search_query != "":
        not_searching = False
        products = Product.objects.filter(Q(name__icontains=search_query))
        if products.count() == 0:
            messages.info(
                request,
                "No such products found. Check your spelling or try a different search.",
            )
        else:
            messages.success(
                request,
                f'Search results for "{search_query}" found: {products.count()}',
            )
    elif search_query == "" and products.count() == 0:
        messages.info(request, "No such products available")
    context = {
        "products": products,
        "search_query": search_query,
        "not_searching": not_searching,
    }
    return render(request, "main/all_products.html", context)


@login_required(login_url="signin")
def delete_shop(request, username, shop_slug):
    user = User.objects.get(username=username)
    try:
        # shop = user.shops.get(name=shop_slug)
        shop = get_by_slug(username, shop_slug)  # type: ignore
        shop.delete()
        messages.success(request, f'The shop "{shop.name}" was deleted successfully!')
    except:
        pass
    return redirect("my_shops", user.username)


@login_required(login_url="signin")
def cart(request, username, shop_slug):
    page = "cart"
    user = User.objects.get(username=username)
    # shop = user.shops.get(name=shop_slug)
    shop = get_by_slug(username, shop_slug)  # type: ignore
    cart = request.user.carts.get(store=shop)
    cart_products = cart.products.all()

    search_query = request.GET.get("q") if request.GET.get("q") != None else ""
    if search_query != "":
        cart_products = [
            product
            for product in cart.products.all()
            if search_query in product.product.name
        ]
        if len(cart_products) == 0:
            messages.info(
                request,
                "No search results found. Check your spelling or try a different search.",
            )
        else:
            messages.success(request, f"Search results found: {len(cart_products)}")

    cart_product_count = len(cart_products)
    total_price = cart.calc_price()

    context = {
        "products": cart_products,
        "cart_product_count": cart_product_count,
        "total": total_price,
        "page": page,
        "cart": cart,
        "shop": shop,
    }
    return render(request, "main/cart.html", context)


@login_required(login_url="signin")
def add_to_cart(request, username, shop_slug, product_id):
    user = User.objects.get(username=username)
    # shop = user.shops.get(name=shop_slug)
    shop = get_by_slug(username, shop_slug)  # type: ignore
    product = shop.products.get(id=product_id)
    if request.user == shop.owner:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

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
            messages.success(
                request,
                f'The product "{order.product.name}" was added successfully to your cart.',
            )

    else:
        order = ProductOrder.objects.create(cart=cart, product=product, quantity=1)
        cart.products.add(order)
        messages.success(
            request,
            f'The product "{order.product.name}" was added successfully to your cart.',
        )

    # return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return redirect("cart", username, shop_slug)


@login_required(login_url="signin")
def decrease_order_quantity(request, store_name, pk):
    order = ProductOrder.objects.get(id=pk)
    if not order.cart.user == request.user:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    if order.quantity > 1:
        order.quantity -= 1
        order.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    # return redirect('cart', order.cart.store.owner.username, order.cart.store.name)


@login_required(login_url="signin")
def remove_from_cart(request, username, shop_slug, product_id):
    user = User.objects.get(username=username)
    # shop = user.shops.get(name=shop_slug)
    shop = get_by_slug(username, shop_slug)  # type: ignore
    product = shop.products.get(id=product_id)
    try:
        cart = request.user.carts.get(store=product.store)
    except:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    product_order = ProductOrder.objects.get(cart=cart, product=product)

    if product_order in cart.products.all():
        # if product_order.quantity > 1:
        #     product_order.quantity -= 1
        #     product_order.save()
        # else:
        cart.products.remove(product_order)
        messages.success(
            request, f'The product "{product.name}" was removed from your cart.'
        )

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    # return redirect('cart', user.username, shop.name)


@login_required(login_url="signin")
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.store.owner != request.user:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    product.delete()
    messages.success(
        request, f'The product "{product.name}" was deleted successfully! '
    )
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def preview(request, username, shop_slug, product_id):
    user = User.objects.get(username=username)
    # shop = user.shops.get(name=shop_slug)
    shop = get_by_slug(username, shop_slug)  # type: ignore
    product = shop.products.get(id=product_id)  # type: ignore
    images = [
        product.image,
        product.image_2,
        product.image_3,
        product.image_4,
        product.image_5,
        product.image_6,
    ]
    in_cart = False
    quantity = 0

    order_pk = 0
    if request.user.is_authenticated and request.user.carts.filter(store=shop).exists():
        for product_order in request.user.carts.get(store=shop).products.all():
            if product_order.product == product:
                in_cart = True
                order_pk = product_order.pk
                quantity = product_order.quantity
                break
    context = {
        "shop": shop,
        "product": product,
        "images": images,
        "in_cart": in_cart,
        "quantity": quantity,
        "order_pk": order_pk,
    }
    return render(request, "main/preview.html", context)


@login_required(login_url="signin")
def place_order(request, username, shop_slug):
    user = User.objects.get(username=username)
    # shop = user.shops.get(name=shop_slug)
    shop = get_by_slug(username, shop_slug)
    products = request.GET.get("products")
    context = {}
    from_cart = False
    if products == "*cart":
        try:
            cart = request.user.carts.get(store=shop)
            products = cart.products.all()
            context["cart_price"] = cart.calc_price()
            from_cart = True
        except:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        products = ProductOrder.objects.filter(id=int(products))
        context["cart_price"] = (
            products.first().product.price * products.first().quantity
            if products.first().product.price is not None
            else 0
        )

    if request.method == "POST":
        this_user = request.user
        this_username = (
            request.POST.get("name")
            if request.POST.get("name") != ""
            else request.user.username
        )
        location_details = {}

        hostel = request.POST.get("hostel")
        room_number = request.POST.get("room_number")
        location = request.POST.get("location")

        location_details.update(
            {"hostel": hostel, "room_number": room_number, "location": location}
        )

        order = Order.objects.create(
            user=this_user,
            user_name=this_username,
            store=shop,
            location_details=location_details,
        )
        for product in products:
            order.products_ordered.add(product)
        order.save()

        if from_cart:
            cart.products.clear()
        messages.success(
            request,
            "Your order has been placed successfully. You will receive a notice shortly about the delivery time.",
        )
        Notification.objects.create(
            to=shop.owner,
            message=f"You have a new order at {shop.name}!",
            type="NEW ORDER",
            details={"shop_slug": shop_slug, "order_pk": order.pk},
        )
        return redirect("shop", username, shop_slug)

    context.update({"shop": shop, "products": products})
    return render(request, "main/place_order.html", context)


# Class based counterpart immediately below. Why function-based views are sometimes easier to use.
def orders(request, username):
    user = request.user
    orders = user.orders_placed.all()
    if user.username != username:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(request, "main/my_orders.html", {"orders": orders})


# class Orders(ListView):
#     model = Order
#     template_name = "main/my_orders.html"
#     context_object_name = "orders"

#     def get_queryset(self):
#         # return self.request.user.orders_placed.all() # -> Does the same thing as the three lines below but more secure.
#         username = self.kwargs["username"]
#         queryset = User.objects.get(username=username).orders_placed.all()
#         return queryset


def order(request, username, pk):
    try:
        order = request.user.orders_placed.get(id=pk)
    except:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    if request.GET.get("from") is not None:
        notification_from_id = int(request.GET.get("from"))
        notification_from = Notification.objects.get(id=notification_from_id)
        # Check if the notification is for the user.
        if not notification_from.to == request.user:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        notification_from.is_read = True
        notification_from.save()

    context = {
        "order": order,
        "cart_price": order.calc_price(),
        "hostel": order.location_details["hostel"],
        "room_number": order.location_details["room_number"],
        "location": order.location_details["hostel"],
    }

    return render(request, "main/order.html", context)


def shop_orders(request, username, shop_slug):
    # shop = User.objects.get(username=username).shops.get(name=shop_slug)
    shop = get_by_slug(username, shop_slug)
    orders = shop.get_unprocessed_orders()

    return render(request, "main/shop_orders.html", {"orders": orders})


def process_order(request, username, shop_slug, pk):
    shop = get_by_slug(username, shop_slug)


    order = shop.orders.get(id=pk)
    notification_from_id = (
        request.GET.get("from") if request.GET.get("from") is not None else ""
    )

    if request.GET.get("from") is not None:
        notification_from_id = int(request.GET.get("from"))
        notification_from = Notification.objects.get(id=notification_from_id)
        # Check if the notification is for the user.
        if not notification_from.to == request.user:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        notification_from.is_read = True
        notification_from.save()

    if request.method == "POST":
        delivery_date = request.POST.get("delivery_date")
        order.delivery_date = delivery_date
        order.save()
        _delivery_date = delivery_date.split("-")
        print(delivery_date)
        string_time = datetime.date(
            day=int(_delivery_date[2]),
            month=int(_delivery_date[1]),
            year=int(_delivery_date[0]),
        ).strftime("%A, %B %d, %Y")
        Notification.objects.create(
            to=order.user,
            message=f"Your order to {shop.name} has been processed successfully. Delivery date is {string_time}",
            type="ORDER UPDATE",
            details={"order_pk": pk},
        )
        messages.success(
            request,
            f"""You have successfully processed {order.user_name}\'s order for delivery on {order.delivery_date}.
             Please make sure you deliver your products to your customers on time.""",
        )
        return redirect("shop", username, shop_slug)

    context = {"order": order, 
        "hostel":order.location_details['hostel'],
        "room_number":order.location_details['room_number'],
        "location":order.location_details['location'],
        }
    return render(request, "main/process_order.html", context)
