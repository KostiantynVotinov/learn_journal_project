"""Визначення регулярних виразів URL-адрес"""

from django.urls import path, include

from . import views

app_name = 'users'

urlpatterns = [
    # Додати уставні URL auth (автефікації)
    path("", include("django.contrib.auth.urls")),
    # Сторінка регистрації.
    path("register/", views.register, name="register"),
]