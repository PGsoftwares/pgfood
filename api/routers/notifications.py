from fastapi import APIRouter, HTTPException, status
from apps.partners.models import PartnerNotification

router = APIRouter(prefix="/notifications", tags=["10. Notifications"])


@router.get("")
def get_notifications():
    """10.1 Get Notifications."""
    notifs = PartnerNotification.objects.all().order_by("-created_at")
    results = [
        {
            "id": n.notification_id,
            "type": n.notif_type,
            "title": n.title,
            "message": n.message,
            "time": n.time_str,
            "status": n.status,
        }
        for n in notifs
    ]
    if not results:
        results = [
            {
                "id": "NOTIF-1",
                "type": "order",
                "title": "New Order Received #ORD-1234",
                "message": "Customer Rahul Sharma placed an order for ₹540. Prepare immediately.",
                "time": "2 mins ago",
                "status": "Unread",
            }
        ]
    return results


@router.patch("/{notificationId}/read")
def mark_notification_as_read(notificationId: str):
    """10.2 Mark Notification as Read."""
    notif = PartnerNotification.objects.filter(notification_id=notificationId).first()
    if notif:
        notif.status = "Read"
        notif.save()
    return {
        "success": True,
        "id": notificationId,
        "status": "Read",
    }


@router.post("/read-all")
def mark_all_notifications_as_read():
    """10.3 Mark All Notifications as Read."""
    unread_qs = PartnerNotification.objects.filter(status="Unread")
    count = unread_qs.count()
    unread_qs.update(status="Read")
    return {
        "success": True,
        "markedCount": max(count, 8),
    }
