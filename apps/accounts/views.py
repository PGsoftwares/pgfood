from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .forms import AdminLoginForm, AdminPasswordChangeForm, AdminProfileForm


class AdminLoginView(View):
    template_name = "authentication/login.html"

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return redirect("dashboard:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = AdminLoginForm(request=request)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AdminLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            remember_me = form.cleaned_data.get("remember_me")
            if remember_me:
                # 30 days session
                request.session.set_expiry(2592000)
            else:
                # Session expires on browser close
                request.session.set_expiry(0)

            messages.success(request, f"Welcome back, {user.full_name}!")
            next_url = request.GET.get("next") or request.POST.get("next")
            if next_url and next_url.startswith("/"):
                return redirect(next_url)
            return redirect("dashboard:index")

        return render(request, self.template_name, {"form": form})


class AdminLogoutView(View):
    """Secure logout view supporting both POST and GET with redirect."""

    def post(self, request):
        logout(request)
        messages.info(request, "You have been logged out securely.")
        return redirect("accounts:login")

    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out securely.")
        return redirect("accounts:login")


@method_decorator(login_required(login_url="accounts:login"), name="dispatch")
class AdminProfileView(View):
    template_name = "profile/profile.html"

    def get(self, request):
        form = AdminProfileForm(instance=request.user)
        return render(request, self.template_name, {"form": form, "active_tab": "profile"})

    def post(self, request):
        # Support avatar deletion
        if request.POST.get("action") == "delete_avatar":
            if request.user.profile_image:
                request.user.profile_image.delete(save=False)
                request.user.profile_image = None
                request.user.save(update_fields=["profile_image"])
                messages.success(request, "Profile image removed successfully.")
            return redirect("accounts:profile")

        form = AdminProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile details have been updated successfully.")
            return redirect("accounts:profile")

        return render(request, self.template_name, {"form": form, "active_tab": "profile"})


@method_decorator(login_required(login_url="accounts:login"), name="dispatch")
class AdminPasswordChangeView(View):
    template_name = "profile/change_password.html"

    def get(self, request):
        form = AdminPasswordChangeForm(user=request.user)
        return render(request, self.template_name, {"form": form, "active_tab": "security"})

    def post(self, request):
        form = AdminPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            request.user.set_password(new_password)
            request.user.save()
            # Maintain active session so admin is not logged out
            update_session_auth_hash(request, request.user)
            messages.success(request, "Your password has been changed successfully.")
            return redirect("accounts:change_password")

        return render(request, self.template_name, {"form": form, "active_tab": "security"})
