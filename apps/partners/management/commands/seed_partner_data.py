import hashlib
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.partners.models import (
    Partner, PartnerApplication, PartnerRestaurant, MenuCategory,
    FoodItem, AddonGroup, PartnerOrder, PartnerOffer, SupportTicket,
    PartnerNotification, SettlementRecord, CustomerReview
)


def hash_pwd(pwd: str) -> str:
    return hashlib.sha256(pwd.encode("utf-8")).hexdigest()


class Command(BaseCommand):
    help = "Seed initial partner app data conforming to API documentation"

    def handle(self, *args, **options):
        # 1. Partner Account
        partner, _ = Partner.objects.update_or_create(
            partner_id="PTR-9842",
            defaults={
                "name": "Vikram Malhotra",
                "mobile": "9876543210",
                "email": "vikram@spicebox.com",
                "password_hash": hash_pwd("Password@123"),
                "restaurant_id": "REST-842",
                "status": "APPROVED",
            }
        )

        # 2. Partner Applications
        PartnerApplication.objects.update_or_create(
            application_id="APP-PG-2026-9842",
            defaults={
                "registration_id": "REG-2026-9842",
                "owner_name": "Vikram Malhotra",
                "mobile_number": "9876543210",
                "email": "vikram@spicebox.com",
                "password_hash": hash_pwd("Password@123"),
                "restaurant_name": "Royal Spice Kitchen",
                "restaurant_type": "Fine Dining",
                "description": "Authentic North Indian curries and Mughlai delicacies",
                "cuisines": ["North Indian", "Biryani", "Mughlai"],
                "logo_url": "https://cdn.pgpartner.com/restaurants/logo_842.png",
                "cover_image_url": "https://cdn.pgpartner.com/restaurants/cover_842.jpg",
                "address": "Shop 14, Ground Floor, Phoenix Mall",
                "area": "Koramangala 5th Block",
                "city": "Bengaluru",
                "state": "Karnataka",
                "pincode": "560095",
                "landmark": "Near Sony World Junction",
                "latitude": 12.9352,
                "longitude": 77.6245,
                "fssai_number": "11223344556677",
                "fssai_cert_url": "https://cdn.pgpartner.com/docs/fssai_cert.pdf",
                "pan_number": "ABCDE1234F",
                "pan_doc_url": "https://cdn.pgpartner.com/docs/pan_card.jpg",
                "gst_number": "29ABCDE1234F1Z5",
                "license_doc_url": "https://cdn.pgpartner.com/docs/trade_license.pdf",
                "account_holder_name": "Royal Spice Kitchen Pvt Ltd",
                "account_number": "50200049281734",
                "ifsc_code": "HDFC0001234",
                "bank_name": "HDFC Bank",
                "branch": "Koramangala Branch",
                "bank_status": "PENNY_DROP_SUCCESS",
                "status": PartnerApplication.Status.APPROVED,
                "admin_remarks": "All documents verified successfully by compliance team.",
                "restaurant_id": "REST-842",
                "verified_at": timezone.now(),
            }
        )

        # Additional Application: UNDER_REVIEW (ready for admin approval in dashboard!)
        PartnerApplication.objects.update_or_create(
            application_id="APP-PG-2026-9843",
            defaults={
                "registration_id": "REG-2026-9843",
                "owner_name": "Sneha Roy",
                "mobile_number": "9812345678",
                "email": "sneha@bengalcrust.com",
                "password_hash": hash_pwd("Sneha@2026"),
                "restaurant_name": "Bengal Crust & Bakery",
                "restaurant_type": "Bakery & Desserts",
                "description": "Artisanal sour doughs, pastries and Bengali sweet fusions",
                "cuisines": ["Bakery", "Desserts", "Cafe"],
                "logo_url": "https://cdn.pgpartner.com/restaurants/logo_843.png",
                "cover_image_url": "https://cdn.pgpartner.com/restaurants/cover_843.jpg",
                "address": "45/A, Indiranagar 100ft Road",
                "area": "Indiranagar",
                "city": "Bengaluru",
                "state": "Karnataka",
                "pincode": "560038",
                "landmark": "Opposite Metro Pillar 84",
                "latitude": 12.9716,
                "longitude": 77.6412,
                "fssai_number": "11998877665544",
                "fssai_cert_url": "https://cdn.pgpartner.com/docs/fssai_843.pdf",
                "pan_number": "BENGP9843K",
                "pan_doc_url": "https://cdn.pgpartner.com/docs/pan_843.jpg",
                "gst_number": "29BENGP9843K1Z9",
                "license_doc_url": "https://cdn.pgpartner.com/docs/license_843.pdf",
                "account_holder_name": "Bengal Crust Enterprise",
                "account_number": "9180200394821",
                "ifsc_code": "ICIC0000104",
                "bank_name": "ICICI Bank",
                "branch": "Indiranagar Branch",
                "bank_status": "PENNY_DROP_SUCCESS",
                "status": PartnerApplication.Status.UNDER_REVIEW,
                "admin_remarks": "Pending compliance document review.",
                "restaurant_id": "",
                "submission_date": timezone.now(),
            }
        )

        # 3. Restaurant Outlet
        working_days = {day: (day != "Sunday") for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
        working_days["Sunday"] = True
        PartnerRestaurant.objects.update_or_create(
            restaurant_id="REST-842",
            defaults={
                "name": "Royal Spice Kitchen",
                "outlet_id": "#PG-842",
                "owner_name": "Vikram Malhotra",
                "mobile": "9876543210",
                "email": "vikram.malhotra@spicebox.com",
                "address": "Shop 14, Ground Floor, Phoenix Mall, Koramangala, Bangalore - 560095",
                "logo_url": "https://cdn.pgpartner.com/restaurants/logo_842.png",
                "cover_image_url": "https://cdn.pgpartner.com/restaurants/cover_842.jpg",
                "rating": 4.5,
                "total_reviews": 348,
                "fssai_number": "11223344556677",
                "is_online": True,
                "status": "ACTIVE",
                "working_days": working_days,
                "opening_time": "10:00",
                "closing_time": "23:30",
                "has_break_time": True,
                "break_start_time": "15:30",
                "break_end_time": "17:00",
                "order_alerts_sound": True,
                "sound_volume": "High",
                "payout_whatsapp_updates": True,
                "marketing_offers": False,
            }
        )

        # 4. Categories
        MenuCategory.objects.update_or_create(
            category_id="CAT-1",
            defaults={"name": "Main Course", "image_url": "https://cdn.pgpartner.com/categories/main_course.png", "item_count": 18, "status": True}
        )
        MenuCategory.objects.update_or_create(
            category_id="CAT-2",
            defaults={"name": "Biryani & Rice", "image_url": "https://cdn.pgpartner.com/categories/biryani.png", "item_count": 8, "status": True}
        )

        # 5. Food Items
        FoodItem.objects.update_or_create(
            item_id="FOOD-101",
            defaults={
                "name": "Paneer Butter Masala",
                "description": "Rich tomato butter gravy with soft cottage cheese cubes",
                "category": "Main Course",
                "food_type": "veg",
                "price": 280.0,
                "prep_time_minutes": 15,
                "available": True,
                "rating": 4.8,
                "image_url": "https://cdn.pgpartner.com/dishes/paneer_butter_masala.jpg"
            }
        )
        FoodItem.objects.update_or_create(
            item_id="FOOD-106",
            defaults={
                "name": "Chicken Dum Biryani",
                "description": "Aromatic basmati rice cooked with spiced chicken and saffron",
                "category": "Biryani & Rice",
                "food_type": "non-veg",
                "price": 340.0,
                "prep_time_minutes": 20,
                "available": True,
                "rating": 4.9,
                "image_url": "https://cdn.pgpartner.com/dishes/biryani.jpg"
            }
        )

        # 6. Addon Groups
        AddonGroup.objects.update_or_create(
            group_id="GRP-1",
            defaults={
                "group_name": "Choose Portion Size (Variant)",
                "required": True,
                "min_selection": 1,
                "max_selection": 1,
                "options": [
                    {"id": "OPT-1", "name": "Half Portion", "price": 0.0},
                    {"id": "OPT-2", "name": "Full Portion", "price": 140.0}
                ]
            }
        )

        # 7. Orders
        PartnerOrder.objects.update_or_create(
            order_id="#ORD-1234",
            defaults={
                "status": PartnerOrder.Status.NEW,
                "customer_name": "Rahul Sharma",
                "customer_phone": "+91 98765 01234",
                "amount": 540.0,
                "prep_minutes": 20,
                "items": [
                    {"name": "Butter Chicken", "qty": 1, "price": 320.0, "addons": "Extra Butter"},
                    {"name": "Garlic Naan", "qty": 2, "price": 110.0, "addons": ""}
                ],
                "bill_summary": {
                    "itemTotal": 500.0,
                    "gstAndRestaurantTaxes": 25.0,
                    "packagingCharges": 15.0,
                    "totalBill": 540.0
                },
                "payment": {
                    "type": "UPI Online",
                    "status": "PAID",
                    "transactionId": "UPI-26309184"
                },
                "delivery_partner": {
                    "name": "Suresh Kumar",
                    "phone": "+91 91234 56789",
                    "status": "ON_THE_WAY"
                },
                "instructions": "Make it less spicy and pack extra mint chutney.",
                "order_time_str": "Just now",
            }
        )

        PartnerOrder.objects.update_or_create(
            order_id="#ORD-1233",
            defaults={
                "status": PartnerOrder.Status.PREPARING,
                "customer_name": "Priya Patel",
                "amount": 780.0,
                "prep_minutes": 20,
                "items": [
                    {"name": "Paneer Tikka", "qty": 1, "price": 380.0},
                    {"name": "Dal Makhani", "qty": 1, "price": 400.0}
                ],
                "order_time_str": "12 mins ago"
            }
        )

        PartnerOrder.objects.update_or_create(
            order_id="#ORD-1232",
            defaults={
                "status": PartnerOrder.Status.READY_FOR_PICKUP,
                "customer_name": "Amit Saxena",
                "amount": 420.0,
                "pickup_otp": "4921",
                "delivery_partner": {
                    "name": "Ramesh Verma",
                    "phone": "+91 98888 12345",
                    "arrivedAtCounter": True
                },
                "items": [{"name": "Chicken Roll", "qty": 2, "price": 420.0}],
                "order_time_str": "25 mins ago"
            }
        )

        PartnerOrder.objects.update_or_create(
            order_id="#ORD-1230",
            defaults={
                "status": PartnerOrder.Status.COMPLETED,
                "customer_name": "Deepa Nair",
                "amount": 450.0,
                "items": [{"name": "Veg Biryani", "qty": 1}, {"name": "Gulab Jamun", "qty": 2}],
                "payment": {"type": "Online UPI", "status": "PAID"},
                "order_time_str": "Yesterday"
            }
        )

        # 8. Offers
        PartnerOffer.objects.update_or_create(
            offer_id="OFFER-1",
            defaults={
                "name": "Weekend Special Flat Discount",
                "code": "PGWEEKEND50",
                "discount_type": "Flat",
                "discount_value": 50.0,
                "min_order": 299.0,
                "start_date": "2026-11-20",
                "end_date": "2026-11-22",
                "status": "Active"
            }
        )

        # 9. Support Tickets
        SupportTicket.objects.update_or_create(
            ticket_id="TCK-8921",
            defaults={
                "issue_type": "Order Payment & Payout Issue",
                "order_id": "#ORD-1234",
                "description": "Payout for order #ORD-1234 was deducted under refund adjustment incorrectly.",
                "attachment_url": "https://cdn.pgpartner.com/docs/statement.pdf",
                "status": "OPEN",
                "estimated_response_hours": 4
            }
        )

        # 10. Notifications
        PartnerNotification.objects.update_or_create(
            notification_id="NOTIF-1",
            defaults={
                "notif_type": "order",
                "title": "New Order Received #ORD-1234",
                "message": "Customer Rahul Sharma placed an order for ₹540. Prepare immediately.",
                "time_str": "2 mins ago",
                "status": "Unread"
            }
        )

        # 11. Settlements
        SettlementRecord.objects.update_or_create(
            settlement_id="SETL-2026-9842",
            defaults={
                "amount": 18450.0,
                "date_str": "15 Nov 2026",
                "bank_info": "HDFC Bank •••• 5678",
                "utr": "HDFCN26319842104",
                "status": "Processed"
            }
        )

        # 12. Reviews
        CustomerReview.objects.update_or_create(
            review_id="REV-1",
            defaults={
                "customer": "Ananya Sharma",
                "rating": 5,
                "date_str": "Today, 01:20 PM",
                "dish": "Butter Chicken & Garlic Naan",
                "review_text": "Authentic rich taste, warm delivery and generous portions!",
                "reply_text": ""
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded initial partner API data into PostgreSQL!"))
