from fastapi import APIRouter, HTTPException, status
from apps.partners.models import Partner, PartnerRestaurant
from api.schemas import ProfileUpdateRequest

router = APIRouter(prefix="/restaurant", tags=["11. Restaurant & Owner Profile"])


@router.get("/profile")
def get_restaurant_profile():
    """11.1 Get Restaurant & Owner Profile."""
    outlet = PartnerRestaurant.objects.first()
    partner = Partner.objects.first()

    if outlet:
        return {
            "restaurantName": outlet.name,
            "outletId": f"#{outlet.restaurant_id.replace('REST-', 'PG-')}",
            "ownerName": partner.name if partner else "Vikram Malhotra",
            "mobile": partner.mobile if partner else "9876543210",
            "email": partner.email if partner else "vikram.malhotra@spicebox.com",
            "address": outlet.address,
            "logoUrl": outlet.logo_url or "https://cdn.pgpartner.com/restaurants/logo_842.png",
            "rating": outlet.rating,
            "fssaiNumber": outlet.fssai_number or "11223344556677",
        }

    return {
        "restaurantName": "Royal Spice Kitchen",
        "outletId": "#PG-842",
        "ownerName": "Vikram Malhotra",
        "mobile": "9876543210",
        "email": "vikram.malhotra@spicebox.com",
        "address": "Shop 14, Ground Floor, Phoenix Mall, Koramangala, Bangalore - 560095",
        "logoUrl": "https://cdn.pgpartner.com/restaurants/logo_842.png",
        "rating": 4.5,
        "fssaiNumber": "11223344556677",
    }


@router.put("/profile")
def update_restaurant_profile(payload: ProfileUpdateRequest):
    """11.2 Update Restaurant & Owner Profile."""
    outlet = PartnerRestaurant.objects.first()
    partner = Partner.objects.first()

    if outlet and payload.restaurantName:
        outlet.name = payload.restaurantName
    if outlet and payload.address:
        outlet.address = payload.address
    if outlet:
        outlet.save()

    if partner:
        if payload.ownerName:
            partner.name = payload.ownerName
        if payload.mobile:
            partner.mobile = payload.mobile
        if payload.email:
            partner.email = payload.email
        partner.save()

    return {
        "success": True,
        "message": "Restaurant and owner profile updated successfully",
    }
