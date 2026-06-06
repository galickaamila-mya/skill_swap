from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy
from .views import account_settings, profile_view, register

app_name = "user"
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", LoginView.as_view(template_name="user/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", profile_view, name="profile"),
    path("account/", account_settings, name="account_settings"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="user/password_reset.html",
            email_template_name="user/password_reset_email.html",
            success_url=reverse_lazy("user:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="user/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="user/password_reset_confirm.html",
            success_url=reverse_lazy("user:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="user/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
