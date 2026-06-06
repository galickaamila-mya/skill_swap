from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile


class CustomRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and (password1 != password2):
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ("phone", "city", "about", "avatar")

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "")
        clean_phone = phone.replace(" ", "").replace("-", "")
        if clean_phone and (not clean_phone.replace("+", "").isdigit()):
            raise forms.ValidationError("Телефон должен содержать только цифры.")
        if clean_phone and (
            not (clean_phone.startswith("+7") or clean_phone.startswith("8"))
        ):
            raise forms.ValidationError("Телефон должен начинаться с +7 или 8.")
        return phone


class AccountForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
