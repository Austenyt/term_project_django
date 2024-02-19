from django.urls import path
from .views import MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView

urlpatterns = [
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='update_mailing'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='delete_mailing'),
]
