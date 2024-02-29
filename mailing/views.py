from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy

from blog.models import Blog
from .models import Mailing, Client, Message
from .forms import MailingForm, ClientForm, MessageForm


class IndexView(TemplateView):  # Главная страница
    template_name = 'mailing/index.html'
    extra_context = {
        'title': 'Сервис отправки сообщений в рассылке'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['article_list'] = Blog.objects.order_by('?')[:3]
        context['object_list'] = Mailing.objects.all()

        unique_clients_count = Client.objects.all().values('email').distinct().count()
        context['unique_clients_count'] = unique_clients_count

        active_mailings_count = Mailing.objects.filter(is_active=True).count()
        context['active_mailings_count'] = active_mailings_count

        return context


class ContactsView(View):
    template_name = 'mailing/contacts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': 'Контакты'})

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')

        return render(request, self.template_name, {'title': 'Контакты'})


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты'
    }


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    context_object_name = 'client'
    extra_context = {
        'title': 'Карточка клиента'
    }


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Добавить клиента'
    }


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Редактировать клиента'
    }


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Удаление клиента'
    }


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    extra_context = {
        'title': 'Рассылки'
    }
    permission_required = 'mailing.can_view_mailing_list'

    def test_func(self):
        return self.request.user.is_authenticated  # Метод для определения авторизации пользователя

    def handle_no_permission(self):
        return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
        # на страницу авторизации при попытке доступа без авторизации


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'
    extra_context = {
        'title': 'Детали рассылки'
    }

    def test_func(self):
        return self.request.user.is_authenticated  # Метод для определения авторизации пользователя

    def handle_no_permission(self):
        return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
        # на страницу авторизации при попытке доступа без авторизации


class MailingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {
        'title': 'Добавить рассылку'
    }

    permission_required = 'mailing.can_deactivate_mailing'

    def form_valid(self, form):
        form.instance.time = form.cleaned_data['time']  # Присваиваем дату и время рассылки из формы
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {
        'title': 'Редактировать рассылку'
    }

    permission_required = 'mailing.can_deactivate_mailing'

    def test_func(self):
        return self.request.user.is_authenticated  # Метод для определения авторизации пользователя

    def handle_no_permission(self):
        return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
        # на страницу авторизации при попытке доступа без авторизации

    def form_valid(self, form):
        form.instance.time = form.cleaned_data['time']  # Присваиваем дату и время рассылки из формы
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {
        'title': 'Удаление рассылки'
    }


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {
        'title': 'Сообщения для рассылок'
    }

    def test_func(self):
        return self.request.user.is_authenticated  # Метод для определения авторизации пользователя

    def handle_no_permission(self):
        return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
        # на страницу авторизации при попытке доступа без авторизации


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'
    extra_context = {
        'title': 'Детали сообщения'
    }


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')
    extra_context = {
        'title': 'Создать сообщение'
    }

    def test_func(self):
        return self.request.user.is_authenticated  # Метод для определения авторизации пользователя

    def handle_no_permission(self):
        return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
        # на страницу авторизации при попытке доступа без авторизации


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')
    extra_context = {
        'title': 'Редактировать сообщение'
    }

    def test_func(self):
        return self.request.user.is_authenticated  # Метод для определения авторизации пользователя

    def handle_no_permission(self):
        return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
        # на страницу авторизации при попытке доступа без авторизации


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    successful_url = reverse_lazy('mailing:index')
    extra_context = {
        'title': 'Удаление сообщения'
    }
