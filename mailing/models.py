from django.db import models


# Модель для Клиента сервиса
class Client(models.Model):
    email = models.EmailField(verbose_name='Email клиента')
    full_name = models.CharField(max_length=100, verbose_name='Полное имя')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


# Модель для Сообщения для рассылки
class Message(models.Model):
    # mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    subject = models.CharField(max_length=255, verbose_name='Тема')
    body = models.TextField(verbose_name='Текст сообщения')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


# Модель для Рассылки
class Mailing(models.Model):
    TIME_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )

    STATUS_CHOICES = (
        ('ready', 'Готово к отправке'),
        ('pending', 'В работе'),
    )

    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    time = models.DateTimeField(verbose_name='Время рассылки')
    frequency = models.CharField(max_length=10, choices=TIME_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=10, default='ready', choices=STATUS_CHOICES, verbose_name='Статус рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Тема сообщения')

    def frequency_display(self):
        for choice in self.TIME_CHOICES:
            if choice[0] == self.frequency:
                return choice[1]
        return None

    def __str__(self):
        return f"{self.frequency_display()} рассылка в {self.time}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


# Модель для Логов рассылки
class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    timestamp = models.TimeField(auto_now_add=True, verbose_name='Временная метка')
    status = models.CharField(max_length=20, verbose_name='Статус')
    server_response = models.TextField(blank=True, verbose_name='Ответ сервера')

    def __str__(self):
        return f"Лог рассылки {self.mailing} - {self.timestamp}"

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'
