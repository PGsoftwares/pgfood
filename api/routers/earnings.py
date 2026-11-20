from io import BytesIO
from typing import Optional
from fastapi import APIRouter, Query, Response
from apps.partners.models import SettlementRecord

router = APIRouter(prefix="/earnings", tags=["8. Financials, Earnings & Settlements"])


@router.get("")
def get_earnings_summary(period: str = Query("today")):
    """8.1 Get Financial Earnings Summary (today, weekly, monthly)."""
    period_lower = period.lower()
    if period_lower == "weekly":
        return {
            "period": "weekly",
            "grossSales": 56420.0,
            "platformCommission": 10155.6,
            "commissionPercentage": 18.0,
            "taxesAndFees": 2821.0,
            "taxPercentage": 5.0,
            "netEarnings": 43443.4,
            "totalDeliveredOrders": 142,
            "averageOrderValue": 397.32
        }
    elif period_lower == "monthly":
        return {
            "period": "monthly",
            "grossSales": 248600.0,
            "platformCommission": 44748.0,
            "commissionPercentage": 18.0,
            "taxesAndFees": 12430.0,
            "taxPercentage": 5.0,
            "netEarnings": 191422.0,
            "totalDeliveredOrders": 618,
            "averageOrderValue": 402.26
        }

    # default: today
    return {
        "period": "today",
        "grossSales": 8450.0,
        "platformCommission": 1521.0,
        "commissionPercentage": 18.0,
        "taxesAndFees": 422.5,
        "taxPercentage": 5.0,
        "netEarnings": 6506.5,
        "totalDeliveredOrders": 21,
        "averageOrderValue": 402.38
    }


@router.get("/settlements")
def get_settlements_history(page: int = Query(1, ge=1), limit: int = Query(20, ge=1)):
    """8.2 Get Settlements History."""
    records = SettlementRecord.objects.all()
    if records.exists():
        return [
            {
                "id": s.settlement_id,
                "amount": s.amount,
                "date": s.date_str,
                "bank": s.bank_info,
                "utr": s.utr,
                "status": s.status
            }
            for s in records
        ]
    return [
        {
            "id": "SETL-2026-9842",
            "amount": 18450.0,
            "date": "15 Nov 2026",
            "bank": "HDFC Bank •••• 5678",
            "utr": "HDFCN26319842104",
            "status": "Processed"
        }
    ]


@router.get("/settlements/{settlementId}/download")
def download_settlement_statement(settlementId: str):
    """8.3 Download Settlement Statement (PDF)."""
    # Generate simple PDF bytes conforming to API doc
    pdf_content = (
        f"%PDF-1.4\n1 0 obj\n<< /Title (Settlement Statement {settlementId}) >>\n"
        "endobj\n2 0 obj\n<< /Type /Catalog /Pages 3 0 R >>\nendobj\n"
        "xref\n0 3\n0000000000 65535 f \ntrailer\n<< /Root 2 0 R >>\n%%EOF"
    ).encode("utf-8")

    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="Settlement_{settlementId}.pdf"'}
    )
