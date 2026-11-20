from django.urls import path
from .views import (
    DashboardSalesApiView,
    DashboardView,
    MenuManagementView,
    OrdersPipelineView,
    PartnerApplicationsView,
    RestaurantsView,
)

app_name = "dashboard"

urlpatterns = [
    path("", DashboardView.as_view(), name="index"),
    path("api/sales-data/", DashboardSalesApiView.as_view(), name="sales_api"),
    path("partner-applications/", PartnerApplicationsView.as_view(), name="partner_applications"),
    path("restaurants/", RestaurantsView.as_view(), name="restaurants"),
    path("orders/", OrdersPipelineView.as_view(), name="orders"),
    path("menu/", MenuManagementView.as_view(), name="menu"),
]
