from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserUpdateView, generate_new_password, UserListView, UserDetailView, \
    UserDeleteView, UserCreateView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='user_create'),
    path('profile/', UserUpdateView.as_view(), name='user_update'),
    path('users', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/user_delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
]
