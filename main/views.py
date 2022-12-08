from django.shortcuts import render


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
    context = {}
    return render(request, 'main/create_shop.html', context)
 
