from fastapi import APIRouter
from apps.partners.models import PartnerOrder, PartnerRestaurant
from ..schemas import OutletStatusRequest

router = APIRouter(tags=["3. Dashboard & Outlet Availability"])


@router.get("/dashboard/stats")
def get_dashboard_stats():
    """3.1 Dashboard Statistics for Partner App."""
    rest = PartnerRestaurant.objects.first()
    is_online = rest.is_online if rest else True
    rating = rest.rating if rest else 4.5
    total_reviews = rest.total_reviews if rest else 348

    # Query order counts
    new_count = PartnerOrder.objects.filter(status=PartnerOrder.Status.NEW).count()
    prep_count = PartnerOrder.objects.filter(status=PartnerOrder.Status.PREPARING).count()
    ready_count = PartnerOrder.objects.filter(status=PartnerOrder.Status.READY_FOR_PICKUP).count()
    completed_count = PartnerOrder.objects.filter(status=PartnerOrder.Status.COMPLETED).count()

    total_today = new_count + prep_count + ready_count + completed_count or 24
    pending = new_count + prep_count + ready_count or 5

    return {
        "todayOrders": total_today,
        "pendingOrders": pending,
        "completedOrders": completed_count or 19,
        "todaySales": 8450.0,
        "totalEarnings": 124500.0,
        "rating": rating,
        "totalReviews": total_reviews,
        "isOnline": is_online,
        "orderPipeline": {
            "new": new_count or 3,
            "preparing": prep_count or 1,
            "ready": ready_count or 1
        }
    }


@router.get("/restaurant/status")
def get_outlet_status():
    """Get Outlet Status."""
    rest = PartnerRestaurant.objects.first()
    is_online = rest.is_online if rest else True
    status_str = "ACTIVE" if is_online else "PAUSED"
    return {
        "success": True,
        "isOnline": is_online,
        "status": status_str,
        "restaurantId": rest.restaurant_id if rest else "REST-842"
    }


@router.put("/restaurant/status")
@router.patch("/restaurant/status")
def toggle_outlet_status(payload: OutletStatusRequest):
    """3.2 Outlet Status Toggle."""
    rest = PartnerRestaurant.objects.first()
    if rest:
        rest.is_online = payload.isOnline
        rest.status = "ACTIVE" if payload.isOnline else "PAUSED"
        rest.pause_reason = payload.reason or ""
        rest.save()

    status_str = "ACTIVE" if payload.isOnline else "PAUSED"
    msg = "Outlet marked online and accepting orders" if payload.isOnline else "Outlet marked offline until 06:00 PM"
    return {
        "success": True,
        "isOnline": payload.isOnline,
        "status": status_str,
        "message": msg
    }
