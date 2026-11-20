import random
from fastapi import APIRouter
from apps.partners.models import PartnerOffer
from ..schemas import CreateOfferRequest, GenericResponse

router = APIRouter(prefix="/offers", tags=["6. Offers & Discounts"])


@router.get("")
def get_active_offers():
    """6.1 Get Active Offers."""
    offers = PartnerOffer.objects.all()
    if offers.exists():
        return [
            {
                "id": o.offer_id,
                "name": o.name,
                "code": o.code,
                "discountType": o.discount_type,
                "discountValue": o.discount_value,
                "minOrder": o.min_order,
                "startDate": o.start_date,
                "endDate": o.end_date,
                "status": o.status
            }
            for o in offers
        ]
    return [
        {
            "id": "OFFER-1",
            "name": "Weekend Special Flat Discount",
            "code": "PGWEEKEND50",
            "discountType": "Flat",
            "discountValue": 50.0,
            "minOrder": 299.0,
            "startDate": "2026-11-20",
            "endDate": "2026-11-22",
            "status": "Active"
        }
    ]


@router.post("", status_code=201)
def create_offer(payload: CreateOfferRequest):
    """6.2 Create Offer."""
    offer_id = f"OFFER-{random.randint(2, 99)}"
    PartnerOffer.objects.create(
        offer_id=offer_id,
        name=payload.name,
        code=payload.code,
        discount_type=payload.discountType,
        discount_value=payload.discountValue,
        min_order=payload.minOrder,
        start_date=payload.startDate,
        end_date=payload.endDate,
        status="Active"
    )
    return {
        "success": True,
        "id": offer_id,
        "code": payload.code,
        "status": "Active"
    }


@router.delete("/{offerId}", response_model=GenericResponse)
def delete_offer(offerId: str):
    """6.3 Delete / Deactivate Offer."""
    PartnerOffer.objects.filter(offer_id=offerId).delete()
    return GenericResponse(success=True, message="Offer deactivated")
