import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from apps.partners.models import (
    FoodItem,
    MenuCategory,
    Partner,
    PartnerApplication,
    PartnerNotification,
    PartnerOrder,
    PartnerRestaurant,
)
from .services import DashboardService


@method_decorator(login_required(login_url="accounts:login"), name="dispatch")
class DashboardView(View):
    template_name = "dashboard/index.html"

    def get(self, request):
        stats = DashboardService.get_summary_statistics()
        sales_data = DashboardService.get_sales_overview_data()
        order_stats = DashboardService.get_order_statistics()
        recent_orders = DashboardService.get_recent_orders()
        recent_activities = DashboardService.get_recent_activities()

        # Update stats dynamically from models if partner records exist
        total_partners_count = PartnerRestaurant.objects.count()
        if total_partners_count > 0:
            stats["total_restaurants"]["value"] = str(total_partners_count)
            stats["total_restaurants"]["subtitle"] = (
                f"{PartnerRestaurant.objects.filter(is_online=True).count()} currently online"
            )

        context = {
            "page_title": "Admin Dashboard",
            "stats": stats,
            "sales_data_json": json.dumps(sales_data),
            "order_stats_json": json.dumps(order_stats),
            "recent_orders": recent_orders,
            "recent_activities": recent_activities,
            "active_menu": "dashboard",
        }
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url="accounts:login"), name="dispatch")
class DashboardSalesApiView(View):
    """API endpoint for asynchronously loading sales timeframe datasets."""

    def get(self, request):
        timeframe = request.GET.get("timeframe", "daily")
        sales_data = DashboardService.get_sales_overview_data()
        selected_data = sales_data.get(timeframe, sales_data["daily"])
        return JsonResponse({"status": "success", "data": selected_data})


@method_decorator(login_required(login_url="accounts:login"), name="dispatch")
class PartnerApplicationsView(View):
    """View to review, verify, approve and reject restaurant onboarding applications."""

    template_name = "dashboard/partner_applications.html"

    def get(self, request):
        status_filter = request.GET.get("status", "")
        qs = PartnerApplication.objects.all().order_by("-submission_date")

        total_count = qs.count()
        under_review_count = qs.filter(status=PartnerApplication.Status.UNDER_REVIEW).count()
        approved_count = qs.filter(status=PartnerApplication.Status.APPROVED).count()
        rejected_count = qs.filter(status=PartnerApplication.Status.REJECTED).count()

        if status_filter:
            qs = qs.filter(status=status_filter.upper())

        context = {
            "page_title": "Partner Applications",
            "applications": qs,
            "active_menu": "partner_applications",
            "status_filter": status_filter,
            "total_count": total_count,
            "under_review_count": under_review_count,
            "approved_count": approved_count,
            "rejected_count": rejected_count,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        app_id = request.POST.get("application_id")
        action = request.POST.get("action")  # 'approve' or 'reject'
        remarks = request.POST.get("admin_remarks", "").strip()

        app = get_object_or_404(PartnerApplication, application_id=app_id)

        if action == "approve":
            app.status = PartnerApplication.Status.APPROVED
            app.admin_remarks = remarks or "All documents verified successfully by compliance team."
            app.verified_at = timezone.now()
            if not app.restaurant_id:
                app.restaurant_id = "REST-842"
            app.save()

            # Ensure partner restaurant outlet exists
            PartnerRestaurant.objects.get_or_create(
                restaurant_id=app.restaurant_id,
                defaults={
                    "name": app.restaurant_name or "Royal Spice Kitchen",
                    "owner_name": app.owner_name or "Vikram Malhotra",
                    "mobile": app.mobile_number or "9876543210",
                    "email": app.email or "partner@spicebox.com",
                    "address": f"{app.address or ''}, {app.city or ''} - {app.pincode or ''}",
                    "fssai_number": app.fssai_number or "11223344556677",
                    "is_online": True,
                    "status": "ACTIVE",
                },
            )

            # Ensure partner account exists for API login
            if not Partner.objects.filter(mobile=app.mobile_number).exists():
                Partner.objects.create(
                    partner_id=f"PTR-{app.application_id[-4:]}",
                    name=app.owner_name,
                    mobile=app.mobile_number,
                    email=app.email,
                    password_hash=app.password_hash or "pbkdf2_sha256$1000000$default_pass",
                    restaurant_id=app.restaurant_id,
                    status="APPROVED",
                )

            messages.success(request, f"Application {app.application_id} approved successfully! Outlet {app.restaurant_id} is now active.")
        elif action == "reject":
            app.status = PartnerApplication.Status.REJECTED
            app.admin_remarks = remarks or "Application rejected due to document verification issues."
            app.verified_at = timezone.now()
            app.save()
            messages.warning(request, f"Application {app.application_id} has been rejected.")

        return redirect("dashboard:partner_applications")


@method_decorator(login_required(login_url="accounts:login"), name="dispatch")
class RestaurantsView(View):
    """View to manage registered restaurant outlets."""

    template_name = "dashboard/restaurants.html"

    def get(self, request):
        restaurants = PartnerRestaurant.objects.all().order_by("-created_at")
        total_count = restaurants.count()
        online_count = restaurants.filter(is_online=True).count()
        active_count = restaurants.filter(status="ACTIVE").count()

        context = {
            "page_title": "Restaurants & Outlets",
            "restaurants": restaurants,
            "active_menu": "restaurants",
            "total_count": total_count,
            "online_count": online_count,
            "active_count": active_count,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        rest_id = request.POST.get("restaurant_id")
        action = request.POST.get("action")  # 'toggle_status' or 'toggle_online'
        rest = get_object_or_404(PartnerRestaurant, restaurant_id=rest_id)

        if action == "toggle_status":
            rest.status = "PAUSED" if rest.status == "ACTIVE" else "ACTIVE"
            rest.save()
            messages.success(request, f"Restaurant {rest.name} status updated to {rest.status}.")
        elif action == "toggle_online":
            rest.is_online = not rest.is_online
            rest.save()
            messages.success(request, f"Restaurant {rest.name} online state toggled to {'ONLINE' if rest.is_online else 'OFFLINE'}.")

        return redirect("dashboard:restaurants")


@method_decorator(login_required(login_url="accounts:login"), name="dispatch")
class OrdersPipelineView(View):
    """View to monitor and manage live partner orders pipeline."""

    template_name = "dashboard/orders.html"

    def get(self, request):
        status_filter = request.GET.get("status", "")
        orders = PartnerOrder.objects.all().order_by("-created_at")

        counts = {
            "all": orders.count(),
            "new": orders.filter(status=PartnerOrder.Status.NEW).count(),
            "preparing": orders.filter(status=PartnerOrder.Status.PREPARING).count(),
            "ready": orders.filter(status=PartnerOrder.Status.READY_FOR_PICKUP).count(),
            "out_for_delivery": orders.filter(status=PartnerOrder.Status.OUT_FOR_DELIVERY).count(),
            "completed": orders.filter(status=PartnerOrder.Status.COMPLETED).count(),
        }

        if status_filter:
            orders = orders.filter(status=status_filter.upper())

        context = {
            "page_title": "Live Orders Pipeline",
            "orders": orders,
            "active_menu": "orders",
            "counts": counts,
            "status_filter": status_filter,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        order_id = request.POST.get("order_id")
        next_status = request.POST.get("next_status")
        order = get_object_or_404(PartnerOrder, order_id=order_id)

        if next_status in PartnerOrder.Status.values:
            order.status = next_status
            order.save()
            messages.success(request, f"Order {order.order_id} moved to {order.get_status_display()}.")

        return redirect("dashboard:orders")


@method_decorator(login_required(login_url="accounts:login"), name="dispatch")
class MenuManagementView(View):
    """View to review menu categories and food items."""

    template_name = "dashboard/menu.html"

    def get(self, request):
        categories = MenuCategory.objects.all()
        items = FoodItem.objects.all()

        context = {
            "page_title": "Menu & Categories",
            "categories": categories,
            "items": items,
            "active_menu": "menu",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        item_id = request.POST.get("item_id")
        item = get_object_or_404(FoodItem, item_id=item_id)
        item.available = not item.available
        item.save()
        messages.success(
            request,
            f"Item '{item.name}' availability set to {'In Stock' if item.available else 'Out of Stock'}.",
        )
        return redirect("dashboard:menu")
