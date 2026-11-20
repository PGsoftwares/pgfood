import os
import random
from typing import Optional
from fastapi import APIRouter, File, Form, UploadFile, status
from django.conf import settings
from apps.partners.models import SupportTicket

router = APIRouter(prefix="/support", tags=["12. Help & Support Tickets"])


@router.post("/tickets", status_code=status.HTTP_201_CREATED)
def submit_support_ticket(
    issueType: str = Form(...),
    orderId: Optional[str] = Form(""),
    description: str = Form(...),
    attachment: Optional[UploadFile] = File(None),
):
    """12.1 Submit Support Ticket."""
    ticket_id = f"TCK-{random.randint(1000, 9999)}"
    attachment_url = ""

    if attachment and attachment.filename:
        upload_dir = os.path.join(settings.MEDIA_ROOT, "support")
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{ticket_id}_{attachment.filename}")
        contents = attachment.file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        attachment_url = f"/media/support/{ticket_id}_{attachment.filename}"

    SupportTicket.objects.create(
        ticket_id=ticket_id,
        restaurant_id="REST-842",
        issue_type=issueType,
        order_id=orderId or "",
        description=description,
        attachment_url=attachment_url,
        status="OPEN",
        estimated_response_hours=4,
    )

    return {
        "success": True,
        "ticketId": ticket_id,
        "status": "OPEN",
        "estimatedResponseHours": 4,
        "message": "Ticket created. Support team will get back to your registered email.",
    }
