from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from .forms import AccountForm, CustomRegisterForm, ProfileForm
from .models import Profile


def register(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("user:profile")
    else:
        form = CustomRegisterForm()
    return render(request, "user/register.html", {"form": form})


@login_required
def profile_view(request):
    user_profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён.")
            return redirect("user:profile")
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, "user/profile.html", {"form": form, "profile": user_profile})


@login_required
def account_settings(request):
    account_form = AccountForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "account":
            account_form = AccountForm(request.POST, instance=request.user)
            if account_form.is_valid():
                account_form.save()
                messages.success(request, "Данные аккаунта обновлены.")
                return redirect("user:account_settings")
        elif action == "password":
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Пароль успешно изменён.")
                return redirect("user:account_settings")
    return render(
        request,
        "user/account_settings.html",
        {"account_form": account_form, "password_form": password_form},
    )
