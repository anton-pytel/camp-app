"""camp_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from camper.views import (
    index, pages,
    login_view, register_user_view, register_child_view,
    profile_view, password_reset_request
)
from django.contrib.auth.views import (
    LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)


urlpatterns = [
    path('camp-admin/', admin.site.urls),
    path('', index, name='tabor home'),
    re_path('gallery.html', pages, name='gallery'),
    path('login/', login_view, name="login"),
    path('register-user/', register_user_view, name="register"),
    path('register/', register_child_view, name="register-child"),
    path('profile/', profile_view, name="profile"),
    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),
    path('password_change/',
         PasswordChangeView.as_view(template_name='pass_reset/password_change.html'),
         name='password_change'),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(template_name='pass_reset/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/',
         password_reset_request,
         name='password_reset'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='pass_reset/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='pass_reset/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(template_name='pass_reset/password_reset_complete.html'),
         name='password_reset_complete'),
    re_path(r'^cms/', include('cms.urls')),
] \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
