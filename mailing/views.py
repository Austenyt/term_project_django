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


class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Клиенты'
    }

    # def get_queryset(self):
    #     return super().get_queryset().filter(
    #         category_id=self.kwargs.get('pk'),
    #         owner=self.request.user
    #     )

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super().get_context_data(*args, **kwargs)
    #     category_item = Category.objects.get(pk=self.kwargs.get('pk'))
    #     context_data['category_pk'] = category_item.pk
    #     context_data['title'] = f'Категория с товарами {category_item.name}'
    #     return context_data


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    context_object_name = 'client'

    # def product_detail_view(request, product_id):
    #     product = Product.objects.get(pk=product_id)
    #     versions = product.get_versions()  # Получаем все версии продукта
    #     context = {
    #         'product': product,
    #         'versions': versions,  # Передаем версии продукта в контекст
    #     }
    #     return render(request, 'product_list.html', context)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Добавить клиента'
    }

    # def test_func(self):
    #     return self.request.user.is_authenticated  # Метод для определения авторизации пользователя
    #
    # def handle_no_permission(self):
    #     return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
    #     # на страницу авторизации при попытке доступа без авторизации


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    # permission_required = ['goods.can_unpublish_product', 'goods.can_change_product_description', 'goods.can_change_product_category']

    # def test_func(self):
    #     return self.request.user.is_authenticated  # Метод для определения авторизации пользователя
    #
    # def handle_no_permission(self):
    #     return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
    #     # на страницу авторизации при попытке доступа без авторизации
    #
    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.object.owner != self.request.user:
    #         raise Http404
    #     return self.object
    #
    # def get_success_url(self):
    #     return reverse('goods:product_update', args=[self.kwargs.get('pk')])
    #
    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
    #     if self.request.method == 'POST':
    #         formset = VersionFormset(self.request.POST, instance=self.object)
    #     else:
    #         formset = VersionFormset(instance=self.object)
    #
    #     context_data['formset'] = formset
    #     return context_data
    #
    # def form_valid(self, form):
    #     context_data = self.get_context_data()
    #     formset = context_data['formset']
    #     self.object = form.save()
    #
    #     if formset.is_valid():
    #         formset.instance = self.object
    #         formset.save()
    #     return super().form_valid(form)


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    # def test_func(self):
    #     return self.request.user.is_authenticated  # Метод для определения авторизации пользователя
    #
    # def handle_no_permission(self):
    #     return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
    #     # на страницу авторизации при попытке доступа без авторизации


class MailingListView(ListView):
    model = Mailing
    extra_context = {
        'title': 'Рассылки'
    }

    # template_name = 'mailing_list.html'
    # context_object_name = 'mailings'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['mailings'] = get_mailings(self.object.pk)
    #     return context


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')
    extra_context = {
        'title': 'Добавить рассылку'
    }

    def form_valid(self, form):
        form.instance.time = form.cleaned_data['time']  # Присваиваем дату и время рассылки из формы
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    # permission_required = ['goods.can_unpublish_product', 'goods.can_change_product_description', 'goods.can_change_product_category']

    def form_valid(self, form):
        form.instance.time = form.cleaned_data['time']  # Присваиваем дату и время рассылки из формы
        return super().form_valid(form)


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MessageListView(ListView):
    model = Message

    # template_name = 'mailing_list.html'
    # context_object_name = 'mailings'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['messages'] = get_messages(self.object.pk)
    #     return context


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')
    # permission_required = ['goods.can_unpublish_product', 'goods.can_change_product_description', 'goods.can_change_product_category']


class MessageDeleteView(DeleteView):
    model = Message
    successful_url = reverse_lazy('mailing:index')
