from django.urls import path
from .views import AdminLoginView, AdminLogoutView, AdminPasswordChangeView, AdminProfileView

app_name = "accounts"

urlpatterns = [
    path("login/", AdminLoginView.as_view(), name="login"),
    path("logout/", AdminLogoutView.as_view(), name="logout"),
    path("profile/", AdminProfileView.as_view(), name="profile"),
    path("profile/change-password/", AdminPasswordChangeView.as_view(), name="change_password"),
]
