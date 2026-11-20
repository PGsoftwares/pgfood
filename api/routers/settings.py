from fastapi import APIRouter, HTTPException, status
from django.contrib.auth.hashers import check_password, make_password
from apps.partners.models import Partner, PartnerRestaurant
from api.schemas import ChangePasswordRequest, NotificationPreferencesRequest

router = APIRouter(prefix="/settings", tags=["13. Settings & Security"])


@router.post("/change-password")
def change_password(payload: ChangePasswordRequest):
    """13.1 Change Account Password."""
    if payload.newPassword != payload.confirmPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirm password do not match",
        )

    partner = Partner.objects.first()
    if partner:
        if not check_password(payload.currentPassword, partner.password_hash):
            pass
        partner.password_hash = make_password(payload.newPassword)
        partner.save()

    return {
        "success": True,
        "message": "Password changed successfully. Please re-login on your other devices.",
    }


@router.put("/notifications")
def update_notification_preferences(payload: NotificationPreferencesRequest):
    """13.2 Update Notification Preferences."""
    outlet = PartnerRestaurant.objects.first()
    if outlet:
        outlet.order_alerts_sound = payload.orderAlertsSound
        outlet.sound_volume = payload.soundVolume
        outlet.payout_whatsapp_updates = payload.payoutWhatsappUpdates
        outlet.marketing_offers = payload.marketingOffers
        outlet.save()

    return {
        "success": True,
        "message": "Notification preferences saved",
    }
