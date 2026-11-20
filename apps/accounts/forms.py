from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


class AdminLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "admin@pgfood.com",
                "autocomplete": "email",
                "autofocus": "autofocus",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
                "id": "password-field",
            }
        ),
    )
    remember_me = forms.BooleanField(
        label="Remember me on this device",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "id": "remember-me-checkbox",
            }
        ),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise ValidationError(
                    "Invalid email address or password. Please check your credentials.",
                    code="invalid_login",
                )
            if not self.user_cache.is_active:
                raise ValidationError(
                    "This account has been deactivated. Please contact the administrator.",
                    code="inactive",
                )
            if not self.user_cache.is_staff and not self.user_cache.is_superuser:
                raise ValidationError(
                    "Access denied. You do not have administrator permissions.",
                    code="unauthorized",
                )

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "email", "mobile_number", "profile_image"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter full name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter email address",
                }
            ),
            "mobile_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+91 98765 43210",
                }
            ),
            "profile_image": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                    "id": "profile-image-input",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email address is already in use by another account.")
        return email


class AdminPasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        label="Current Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter current password",
                "id": "current-password-field",
            }
        ),
    )
    new_password = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new password (min. 8 characters)",
                "id": "new-password-field",
            }
        ),
    )
    confirm_new_password = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm new password",
                "id": "confirm-password-field",
            }
        ),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")
        if not self.user.check_password(current_password):
            raise ValidationError("The current password entered is incorrect.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                self.add_error("confirm_new_password", "The two new passwords do not match.")
            else:
                try:
                    validate_password(new_password, self.user)
                except ValidationError as error:
                    self.add_error("new_password", error)

        return cleaned_data
