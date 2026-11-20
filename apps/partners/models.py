import uuid
from django.db import models
from django.utils import timezone


class Partner(models.Model):
    """Restaurant partner account for authentication and access."""
    partner_id = models.CharField(max_length=50, primary_key=True, default="PTR-9842")
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    restaurant_id = models.CharField(max_length=50, blank=True, default="REST-842")
    status = models.CharField(max_length=50, default="APPROVED")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "partner_accounts"
        verbose_name = "Partner Account"
        verbose_name_plural = "Partner Accounts"

    def __str__(self):
        return f"{self.name} ({self.partner_id}) - {self.mobile}"


class PartnerApplication(models.Model):
    """Onboarding application submitted by prospective restaurant partner."""
    class Status(models.TextChoices):
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    application_id = models.CharField(max_length=60, primary_key=True)
    registration_id = models.CharField(max_length=60, unique=True)
    owner_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20)
    email = models.EmailField()
    password_hash = models.CharField(max_length=255, blank=True)

    restaurant_name = models.CharField(max_length=255, blank=True)
    restaurant_type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    cuisines = models.JSONField(default=list, blank=True)
    logo_url = models.CharField(max_length=500, blank=True)
    cover_image_url = models.CharField(max_length=500, blank=True)

    address = models.TextField(blank=True)
    area = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=20, blank=True)
    landmark = models.CharField(max_length=150, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    fssai_number = models.CharField(max_length=50, blank=True)
    fssai_cert_url = models.CharField(max_length=500, blank=True)
    pan_number = models.CharField(max_length=50, blank=True)
    pan_doc_url = models.CharField(max_length=500, blank=True)
    gst_number = models.CharField(max_length=50, blank=True)
    license_doc_url = models.CharField(max_length=500, blank=True)

    account_holder_name = models.CharField(max_length=255, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=50, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    bank_status = models.CharField(max_length=50, default="PENNY_DROP_SUCCESS")

    status = models.CharField(max_length=50, choices=Status.choices, default=Status.UNDER_REVIEW)
    admin_remarks = models.TextField(blank=True)
    restaurant_id = models.CharField(max_length=50, blank=True)
    submission_date = models.DateTimeField(default=timezone.now)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "partner_applications"
        verbose_name = "Partner Application"
        verbose_name_plural = "Partner Applications"
        ordering = ["-submission_date"]

    def __str__(self):
        return f"{self.application_id} - {self.restaurant_name} ({self.status})"


class PartnerRestaurant(models.Model):
    """Registered restaurant outlet."""
    restaurant_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    outlet_id = models.CharField(max_length=50, default="#PG-842")
    owner_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    logo_url = models.CharField(max_length=500, blank=True)
    cover_image_url = models.CharField(max_length=500, blank=True)
    rating = models.FloatField(default=4.5)
    total_reviews = models.IntegerField(default=348)
    fssai_number = models.CharField(max_length=50, blank=True)

    is_online = models.BooleanField(default=True)
    status = models.CharField(max_length=50, default="ACTIVE")  # ACTIVE, PAUSED
    pause_reason = models.CharField(max_length=255, blank=True)
    resume_at = models.DateTimeField(null=True, blank=True)

    working_days = models.JSONField(default=dict)
    opening_time = models.CharField(max_length=10, default="10:00")
    closing_time = models.CharField(max_length=10, default="23:30")
    has_break_time = models.BooleanField(default=True)
    break_start_time = models.CharField(max_length=10, default="15:30")
    break_end_time = models.CharField(max_length=10, default="17:00")

    order_alerts_sound = models.BooleanField(default=True)
    sound_volume = models.CharField(max_length=20, default="High")
    payout_whatsapp_updates = models.BooleanField(default=True)
    marketing_offers = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "partner_restaurants"
        verbose_name = "Restaurant Outlet"
        verbose_name_plural = "Restaurant Outlets"

    def __str__(self):
        return f"{self.name} ({self.restaurant_id})"


class MenuCategory(models.Model):
    category_id = models.CharField(max_length=50, primary_key=True)
    restaurant_id = models.CharField(max_length=50, default="REST-842")
    name = models.CharField(max_length=150)
    image_url = models.CharField(max_length=500, blank=True)
    item_count = models.IntegerField(default=0)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "menu_categories"
        verbose_name = "Menu Category"
        verbose_name_plural = "Menu Categories"

    def __str__(self):
        return f"{self.name} ({self.category_id})"


class FoodItem(models.Model):
    item_id = models.CharField(max_length=50, primary_key=True)
    restaurant_id = models.CharField(max_length=50, default="REST-842")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=150)
    food_type = models.CharField(max_length=50, default="veg")  # veg, non-veg
    price = models.FloatField(default=0.0)
    prep_time_minutes = models.IntegerField(default=15)
    available = models.BooleanField(default=True)
    image_url = models.CharField(max_length=500, blank=True)
    rating = models.FloatField(default=4.8)

    class Meta:
        db_table = "menu_food_items"
        verbose_name = "Food Item"
        verbose_name_plural = "Food Items"

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class AddonGroup(models.Model):
    group_id = models.CharField(max_length=50, primary_key=True)
    restaurant_id = models.CharField(max_length=50, default="REST-842")
    group_name = models.CharField(max_length=255)
    required = models.BooleanField(default=False)
    min_selection = models.IntegerField(default=0)
    max_selection = models.IntegerField(default=1)
    options = models.JSONField(default=list)

    class Meta:
        db_table = "menu_addon_groups"


class PartnerOrder(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "New Order"
        PREPARING = "PREPARING", "Preparing"
        READY_FOR_PICKUP = "READY_FOR_PICKUP", "Ready for Pickup"
        OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY", "Out for Delivery"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    order_id = models.CharField(max_length=50, primary_key=True)
    restaurant_id = models.CharField(max_length=50, default="REST-842")
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.NEW)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=25, blank=True)
    amount = models.FloatField(default=0.0)
    prep_minutes = models.IntegerField(default=20)
    pickup_otp = models.CharField(max_length=10, default="4921")
    items = models.JSONField(default=list)
    bill_summary = models.JSONField(default=dict)
    payment = models.JSONField(default=dict)
    delivery_partner = models.JSONField(default=dict)
    instructions = models.TextField(blank=True)
    order_time_str = models.CharField(max_length=100, default="Just now")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "partner_orders"
        verbose_name = "Partner Order"
        verbose_name_plural = "Partner Orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_id} - {self.customer_name} (₹{self.amount})"


class PartnerOffer(models.Model):
    offer_id = models.CharField(max_length=50, primary_key=True)
    restaurant_id = models.CharField(max_length=50, default="REST-842")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    discount_type = models.CharField(max_length=50, default="Percentage")
    discount_value = models.FloatField(default=0.0)
    min_order = models.FloatField(default=0.0)
    start_date = models.CharField(max_length=50)
    end_date = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="Active")

    class Meta:
        db_table = "partner_offers"


class SupportTicket(models.Model):
    ticket_id = models.CharField(max_length=50, primary_key=True)
    restaurant_id = models.CharField(max_length=50, default="REST-842")
    issue_type = models.CharField(max_length=255)
    order_id = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    attachment_url = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=50, default="OPEN")
    estimated_response_hours = models.IntegerField(default=4)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "partner_support_tickets"


class PartnerNotification(models.Model):
    notification_id = models.CharField(max_length=50, primary_key=True)
    restaurant_id = models.CharField(max_length=50, default="REST-842")
    notif_type = models.CharField(max_length=50, default="order")
    title = models.CharField(max_length=255)
    message = models.TextField()
    time_str = models.CharField(max_length=50, default="Just now")
    status = models.CharField(max_length=50, default="Unread")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "partner_notifications"


class SettlementRecord(models.Model):
    settlement_id = models.CharField(max_length=50, primary_key=True)
    restaurant_id = models.CharField(max_length=50, default="REST-842")
    amount = models.FloatField()
    date_str = models.CharField(max_length=100)
    bank_info = models.CharField(max_length=255)
    utr = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="Processed")

    class Meta:
        db_table = "partner_settlements"


class CustomerReview(models.Model):
    review_id = models.CharField(max_length=50, primary_key=True)
    restaurant_id = models.CharField(max_length=50, default="REST-842")
    customer = models.CharField(max_length=255)
    rating = models.IntegerField(default=5)
    date_str = models.CharField(max_length=100, default="Today, 01:20 PM")
    dish = models.CharField(max_length=255)
    review_text = models.TextField()
    reply_text = models.TextField(blank=True)

    class Meta:
        db_table = "partner_customer_reviews"
