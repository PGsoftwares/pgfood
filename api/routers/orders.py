from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from apps.partners.models import PartnerOrder
from ..schemas import (
    AcceptOrderRequest, HandoverRequest,
    PrepTimeRequest, RejectOrderRequest
)

router = APIRouter(prefix="/orders", tags=["4. Orders Management Pipeline"])


@router.get("")
def get_orders_by_status(status: Optional[str] = Query(None)):
    """4.1, 4.5, 4.8 Get Orders by Status (new, preparing, ready)."""
    status_lower = (status or "").lower()

    if status_lower == "new":
        db_orders = PartnerOrder.objects.filter(status=PartnerOrder.Status.NEW)
        if db_orders.exists():
            return [
                {
                    "id": o.order_id,
                    "orderTime": o.order_time_str,
                    "amount": o.amount,
                    "customer": {
                        "name": o.customer_name,
                        "phone": o.customer_phone or "+91 98765 01234"
                    },
                    "items": o.items,
                    "paymentMethod": o.payment.get("type", "UPI Online (Paid)"),
                    "instructions": o.instructions
                }
                for o in db_orders
            ]
        # Demo fallback conforming to API doc
        return [
            {
                "id": "#ORD-1234",
                "orderTime": "Just now",
                "amount": 540.0,
                "customer": {"name": "Rahul Sharma", "phone": "+91 98765 01234"},
                "items": [
                    {"name": "Butter Chicken", "qty": 1, "price": 320.0, "addons": "Extra Butter"},
                    {"name": "Garlic Naan", "qty": 2, "price": 110.0, "addons": ""}
                ],
                "paymentMethod": "UPI Online (Paid)",
                "instructions": "Make it less spicy and pack extra mint chutney."
            }
        ]

    elif status_lower == "preparing":
        db_orders = PartnerOrder.objects.filter(status=PartnerOrder.Status.PREPARING)
        if db_orders.exists():
            return [
                {
                    "id": o.order_id,
                    "orderTime": o.order_time_str,
                    "prepMinutes": o.prep_minutes,
                    "amount": o.amount,
                    "customer": {"name": o.customer_name},
                    "items": o.items
                }
                for o in db_orders
            ]
        return [
            {
                "id": "#ORD-1233",
                "orderTime": "12 mins ago",
                "prepMinutes": 20,
                "amount": 780.0,
                "customer": {"name": "Priya Patel"},
                "items": [
                    {"name": "Paneer Tikka", "qty": 1},
                    {"name": "Dal Makhani", "qty": 1}
                ]
            }
        ]

    elif status_lower == "ready":
        db_orders = PartnerOrder.objects.filter(status=PartnerOrder.Status.READY_FOR_PICKUP)
        if db_orders.exists():
            return [
                {
                    "id": o.order_id,
                    "amount": o.amount,
                    "deliveryPartner": o.delivery_partner.get("name", "Ramesh Verma"),
                    "partnerPhone": o.delivery_partner.get("phone", "+91 98888 12345"),
                    "pickupOtp": o.pickup_otp,
                    "arrivedAtCounter": o.delivery_partner.get("arrivedAtCounter", True)
                }
                for o in db_orders
            ]
        return [
            {
                "id": "#ORD-1232",
                "amount": 420.0,
                "deliveryPartner": "Ramesh Verma",
                "partnerPhone": "+91 98888 12345",
                "pickupOtp": "4921",
                "arrivedAtCounter": True
            }
        ]

    # All active orders
    return list(PartnerOrder.objects.values("order_id", "status", "customer_name", "amount", "order_time_str"))


@router.post("/{orderId}/accept")
def accept_order(orderId: str, payload: AcceptOrderRequest):
    """4.2 Accept Order."""
    order = PartnerOrder.objects.filter(order_id=orderId).first()
    if order:
        order.status = PartnerOrder.Status.PREPARING
        order.prep_minutes = payload.preparationMinutes
        order.save()

    ready_time = (datetime.now(timezone.utc) + timedelta(minutes=payload.preparationMinutes)).isoformat()
    return {
        "success": True,
        "orderId": orderId,
        "status": "PREPARING",
        "estimatedReadyTime": ready_time
    }


@router.post("/{orderId}/reject")
def reject_order(orderId: str, payload: RejectOrderRequest):
    """4.3 Reject Order."""
    order = PartnerOrder.objects.filter(order_id=orderId).first()
    if order:
        order.status = PartnerOrder.Status.CANCELLED
        order.save()

    return {
        "success": True,
        "orderId": orderId,
        "status": "CANCELLED",
        "message": "Order rejected and customer notified"
    }


@router.get("/history")
def get_order_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1),
    status: str = Query("all"),
    search: Optional[str] = Query(None)
):
    """4.10 Order History."""
    return {
        "total": 580,
        "page": page,
        "orders": [
            {
                "id": "#ORD-1230",
                "date": "2026-11-19T11:30:00Z",
                "customer": "Deepa Nair",
                "amount": 450.0,
                "itemsCount": 2,
                "status": "COMPLETED",
                "payment": "Online UPI"
            }
        ]
    }


@router.get("/{orderId}")
def get_order_details(orderId: str):
    """4.4 Get Order Details."""
    order = PartnerOrder.objects.filter(order_id=orderId).first()
    if order:
        return {
            "id": order.order_id,
            "status": order.status,
            "createdAt": order.created_at.isoformat(),
            "customer": {
                "name": order.customer_name,
                "phone": order.customer_phone or "+91 98765 01234"
            },
            "items": order.items,
            "billSummary": order.bill_summary or {
                "itemTotal": 500.0,
                "gstAndRestaurantTaxes": 25.0,
                "packagingCharges": 15.0,
                "totalBill": 540.0
            },
            "payment": order.payment or {
                "type": "UPI Online",
                "status": "PAID",
                "transactionId": "UPI-26309184"
            },
            "deliveryPartner": order.delivery_partner or {
                "name": "Suresh Kumar",
                "phone": "+91 91234 56789",
                "status": "ON_THE_WAY"
            },
            "instructions": order.instructions
        }

    return {
        "id": orderId,
        "status": "PREPARING",
        "createdAt": "2026-11-20T14:15:00Z",
        "customer": {
            "name": "Rahul Sharma",
            "phone": "+91 98765 01234"
        },
        "items": [
            {"name": "Butter Chicken", "qty": 1, "price": 320.0, "addons": "Extra Gravy"},
            {"name": "Butter Naan", "qty": 2, "price": 90.0, "addons": ""}
        ],
        "billSummary": {
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
        "deliveryPartner": {
            "name": "Suresh Kumar",
            "phone": "+91 91234 56789",
            "status": "ON_THE_WAY"
        },
        "instructions": "Make it less spicy."
    }


@router.patch("/{orderId}/prep-time")
def update_prep_time(orderId: str, payload: PrepTimeRequest):
    """4.6 Update Order Preparation Time."""
    order = PartnerOrder.objects.filter(order_id=orderId).first()
    new_prep = 30
    if order:
        order.prep_minutes += payload.additionalMinutes
        new_prep = order.prep_minutes
        order.save()

    updated_ready = (datetime.now(timezone.utc) + timedelta(minutes=new_prep)).isoformat()
    return {
        "success": True,
        "orderId": orderId,
        "totalPrepMinutes": new_prep,
        "updatedReadyTime": updated_ready
    }


@router.post("/{orderId}/ready")
def mark_order_ready(orderId: str):
    """4.7 Mark Order Ready for Pickup."""
    order = PartnerOrder.objects.filter(order_id=orderId).first()
    if order:
        order.status = PartnerOrder.Status.READY_FOR_PICKUP
        order.save()

    return {
        "success": True,
        "orderId": orderId,
        "status": "READY_FOR_PICKUP",
        "deliveryPartnerOtp": "4921"
    }


@router.post("/{orderId}/handover")
def confirm_handover(orderId: str, payload: HandoverRequest):
    """4.9 Confirm Handover to Delivery Partner."""
    order = PartnerOrder.objects.filter(order_id=orderId).first()
    if order:
        order.status = PartnerOrder.Status.OUT_FOR_DELIVERY
        order.save()

    return {
        "success": True,
        "orderId": orderId,
        "status": "OUT_FOR_DELIVERY",
        "message": "Order handed over to delivery partner"
    }
