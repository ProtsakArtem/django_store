from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User
from django import forms
from users.tasks import send_email_verification

class UserDataForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4", 'placeholder': "Введите имя пользователя"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control py-4", 'placeholder':"Введите пароль"}))
    class Meta:
        model = User
        fields = ("username", "password")


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4", 'placeholder': "Введите имя"}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control py-4", 'placeholder': "Введите фамилию"}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control py-4", 'placeholder': "Введите никнейм"}))
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': "form-control py-4", 'placeholder': "Введите email"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "form-control py-4", 'placeholder': "Введите пароль"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "form-control py-4", 'placeholder': "Повторите пароль"}))
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=True)
        send_email_verification.delay(user.id)
        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4", "readonly": True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control py-4", "readonly": True}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': "custom-file-input"}), required=False)
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "image")