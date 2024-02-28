import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from config import settings
from users.forms import UserProfileForm, UserRegisterForm, UserAdminForm
from users.models import User


class UserListView(ListView):
    model = User
    extra_context = {
        'title': 'Пользователи'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_not_blocked=True)
        return queryset


class RegisterView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject='Поздравляем с регистрацией',
            message='Вы зарегистрировались на нашей платформе, добро пожаловать!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserAdminUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserAdminForm
    success_url = reverse_lazy('users:user_list')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.kwargs['pk'])


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'
    extra_context = {
        'title': 'Карточка пользователя'
    }


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('users:user_list')


@login_required
def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('goods:index'))
