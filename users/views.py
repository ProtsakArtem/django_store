from django.shortcuts import render

# Create your views here.
def register(request):
    content = {"title": "Store - Регистрация"}
    return render(request, 'register.html', context=content)

def login(request):
    content = {"title": "Store - Вход"}
    return render(request, 'login.html', context=content)