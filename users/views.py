from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden
from django.shortcuts import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, TemplateView
from common.views import TitleMixin
from users.forms import UserRegisterForm, UserProfileForm
from django.contrib import messages
from django.urls import reverse_lazy, reverse

from users.models import User, EmailVerification


# Create your views here.

class RegisterView(SuccessMessageMixin, TitleMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_message = 'Вы успешно зарегестрированы!'
    title = "Store - Регистрация"

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class LoginFormView(LoginView):
    model = User
    template_name = 'login.html'


class ProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('')
    template_name = 'profile.html'
    title = 'Store - Профиль'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().id != self.request.user.id:
            return HttpResponseForbidden("Вы не можете просматривать профиль другого пользователя.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Данные успешно изменены!')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))




class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение почты'
    template_name = 'email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified = True
            user.save()
            return super(EmailVerificationView,  self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))