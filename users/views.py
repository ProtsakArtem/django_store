from django.shortcuts import render, HttpResponseRedirect

from products.models import Cart, Product
from users.models import User
from users.forms import UserDataForm, UserRegisterForm, UserProfileForm
from django.contrib import auth, messages
from django.urls import reverse

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрированы!')
            return HttpResponseRedirect(reverse('users:login'))
        # else:
        #     username = request.POST['username']
        #     password = request.POST['password']
        # content = {"title": "Store - Регистрация", 'form': form}
    else:
        form = UserRegisterForm()
    content = {"title": "Store - Регистрация", 'form': form}
    return render(request, 'register.html', context=content)

def login(request):
    if request.method == 'POST':
        form = UserDataForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserDataForm()
    content = {"title": "Store - Вход", 'form': form}
    return render(request, 'login.html', context=content)

def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            print("valid profile")
            form.save()
            messages.success(request, 'Данные успешно изменены!')
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)

    content = {"title": "Store - Профиль", 'form': form, 'carts': Cart.objects.filter(user=request.user).all()}
    return render(request, 'profile.html', context=content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def add_product_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    carts = Cart.objects.filter(user=request.user, product=product)
    if carts.exists():
        cart = carts.first()
        cart.quantity += 1
        cart.save()
    else:
        Cart.objects.create(user=request.user, product=product, quantity=1)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def remove_product_from_cart(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))