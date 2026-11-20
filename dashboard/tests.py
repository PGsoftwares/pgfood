from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from apps.partners.models import (
    FoodItem,
    MenuCategory,
    PartnerApplication,
    PartnerOrder,
    PartnerRestaurant,
)

User = get_user_model()


class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            email="dashadmin@pgfood.com",
            password="DashboardPassword123!",
            full_name="Dashboard Admin",
        )
        self.client.login(email="dashadmin@pgfood.com", password="DashboardPassword123!")

    def test_dashboard_login_required(self):
        anonymous_client = Client()
        response = anonymous_client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_dashboard_authenticated_success(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Food Delivery Admin Dashboard")
        self.assertContains(response, "Total Orders")
        self.assertContains(response, "Total Revenue")
        self.assertContains(response, "Restaurants")
        self.assertContains(response, "Delivery Fleet")
        self.assertContains(response, "Sales & Revenue Overview")
        self.assertContains(response, "Recent Food Delivery Orders")

    def test_sales_api_endpoint(self):
        response = self.client.get(reverse("dashboard:sales_api") + "?timeframe=weekly")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("categories", data["data"])
        self.assertIn("revenue", data["data"])

    def test_partner_applications_view(self):
        PartnerApplication.objects.create(
            application_id="APP-TEST-1",
            registration_id="REG-TEST-1",
            owner_name="Test Merchant",
            restaurant_name="Spice Villa",
            mobile_number="9800011122",
            email="merchant@test.com",
            status=PartnerApplication.Status.UNDER_REVIEW,
        )
        response = self.client.get(reverse("dashboard:partner_applications"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Partner Applications & Verification")
        self.assertContains(response, "Spice Villa")
        self.assertContains(response, "APP-TEST-1")

        # Test approve action
        post_resp = self.client.post(
            reverse("dashboard:partner_applications"),
            {
                "application_id": "APP-TEST-1",
                "action": "approve",
                "admin_remarks": "Approved by test compliance",
            },
        )
        self.assertEqual(post_resp.status_code, 302)
        app = PartnerApplication.objects.get(application_id="APP-TEST-1")
        self.assertEqual(app.status, PartnerApplication.Status.APPROVED)

    def test_restaurants_view(self):
        PartnerRestaurant.objects.create(
            restaurant_id="REST-TEST-1",
            name="Gourmet Grill",
            owner_name="Grill Master",
            mobile="9811223344",
            email="grill@test.com",
            address="123 Test St",
            is_online=True,
            status="ACTIVE",
        )
        response = self.client.get(reverse("dashboard:restaurants"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Restaurants & Outlet Management")
        self.assertContains(response, "Gourmet Grill")

        # Test toggle online
        post_resp = self.client.post(
            reverse("dashboard:restaurants"),
            {"restaurant_id": "REST-TEST-1", "action": "toggle_online"},
        )
        self.assertEqual(post_resp.status_code, 302)
        rest = PartnerRestaurant.objects.get(restaurant_id="REST-TEST-1")
        self.assertFalse(rest.is_online)

    def test_orders_pipeline_view(self):
        PartnerOrder.objects.create(
            order_id="#ORD-TEST-1",
            customer_name="Test Customer",
            amount=450.0,
            status=PartnerOrder.Status.NEW,
        )
        response = self.client.get(reverse("dashboard:orders"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Live Orders Management Pipeline")
        self.assertContains(response, "#ORD-TEST-1")

        # Test advance status
        post_resp = self.client.post(
            reverse("dashboard:orders"),
            {"order_id": "#ORD-TEST-1", "next_status": "PREPARING"},
        )
        self.assertEqual(post_resp.status_code, 302)
        order = PartnerOrder.objects.get(order_id="#ORD-TEST-1")
        self.assertEqual(order.status, "PREPARING")

    def test_menu_management_view(self):
        MenuCategory.objects.create(category_id="CAT-TEST-1", name="Desserts", status=True)
        FoodItem.objects.create(
            item_id="FOOD-TEST-1",
            name="Chocolate Cake",
            category="Desserts",
            price=150.0,
            available=True,
        )
        response = self.client.get(reverse("dashboard:menu"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Menu & Food Categories")
        self.assertContains(response, "Chocolate Cake")

        # Test toggle availability
        post_resp = self.client.post(
            reverse("dashboard:menu"),
            {"item_id": "FOOD-TEST-1"},
        )
        self.assertEqual(post_resp.status_code, 302)
        item = FoodItem.objects.get(item_id="FOOD-TEST-1")
        self.assertFalse(item.available)
