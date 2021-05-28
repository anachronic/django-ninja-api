from django.contrib import admin
from django.urls import path, include
from conf.api import api
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='intranet/registration/login.html'),
        name='login',
    ),
]
