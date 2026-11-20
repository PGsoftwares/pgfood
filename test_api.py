"""Comprehensive automated test script for all 13 sections of PG Partner FastAPI."""

import sys
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_suite():
    passed = 0
    failed = 0

    def check(name, condition, details=""):
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"[PASS] {name}")
        else:
            failed += 1
            print(f"[FAIL] {name}: {details}")

    print("--- 1. Testing Root & Docs ---")
    r = client.get("/")
    check("GET /", r.status_code == 200 and r.json().get("status") == "online", r.text)

    r = client.get("/openapi.json")
    check("GET /openapi.json", r.status_code == 200, r.text)

    print("\n--- 2. Section 1: Auth & Password Reset ---")
    r = client.post("/v1/auth/login", json={"identifier": "9876543210", "password": "Password@123"})
    check("POST /v1/auth/login (valid)", r.status_code == 200 and r.json().get("success") is True, r.text)
    token = r.json().get("token", "")

    r = client.post("/v1/auth/forgot-password", json={"identifier": "9876543210"})
    check("POST /v1/auth/forgot-password", r.status_code == 200 and "otpSessionId" in r.json(), r.text)
    otp_session_id = r.json().get("otpSessionId", "")

    r = client.post("/v1/auth/verify-otp", json={"otpSessionId": otp_session_id, "otp": "4921"})
    check("POST /v1/auth/verify-otp", r.status_code == 200 and "verificationToken" in r.json(), r.text)
    verif_token = r.json().get("verificationToken", "")

    r = client.post(
        "/v1/auth/reset-password",
        json={
            "verificationToken": verif_token,
            "newPassword": "Password@123",
            "confirmPassword": "Password@123",
        },
    )
    check("POST /v1/auth/reset-password", r.status_code == 200 and r.json().get("success") is True, r.text)

    r = client.post("/v1/auth/logout", json={"deviceToken": "fcm_token_123"})
    check("POST /v1/auth/logout", r.status_code == 200, r.text)

    print("\n--- 3. Section 2: Partner Onboarding & Registration ---")
    r = client.post(
        "/v1/registration/owner-details",
        json={
            "ownerName": "Test Partner",
            "mobileNumber": "9811223344",
            "email": "testpartner@example.com",
            "password": "Password@123",
        },
    )
    check("POST /v1/registration/owner-details", r.status_code == 201, r.text)

    r = client.get("/v1/registration/status?mobile=9876543210")
    check("GET /v1/registration/status", r.status_code == 200, r.text)

    print("\n--- 4. Section 3: Dashboard & Outlet Availability ---")
    r = client.get("/v1/dashboard/stats")
    check("GET /v1/dashboard/stats", r.status_code == 200 and "todayOrders" in r.json(), r.text)

    r = client.get("/v1/restaurant/status")
    check("GET /v1/restaurant/status", r.status_code == 200 and "isOnline" in r.json(), r.text)

    r = client.patch("/v1/restaurant/status", json={"isOnline": True})
    check("PATCH /v1/restaurant/status", r.status_code == 200 and r.json().get("isOnline") is True, r.text)

    print("\n--- 5. Section 4: Orders Management Pipeline ---")
    r = client.get("/v1/orders?status=new")
    check("GET /v1/orders?status=new", r.status_code == 200 and isinstance(r.json(), list), r.text)

    r = client.post("/v1/orders/%23ORD-1234/accept", json={"preparationMinutes": 25})
    check("POST /v1/orders/{id}/accept", r.status_code == 200, r.text)

    r = client.get("/v1/orders/%23ORD-1234")
    check("GET /v1/orders/{id}", r.status_code == 200 and "billSummary" in r.json(), r.text)

    r = client.patch("/v1/orders/%23ORD-1233/prep-time", json={"additionalMinutes": 10})
    check("PATCH /v1/orders/{id}/prep-time", r.status_code == 200, r.text)

    r = client.post("/v1/orders/%23ORD-1233/ready", json={})
    check("POST /v1/orders/{id}/ready", r.status_code == 200 and "deliveryPartnerOtp" in r.json(), r.text)

    r = client.get("/v1/orders?status=ready")
    check("GET /v1/orders?status=ready", r.status_code == 200 and isinstance(r.json(), list), r.text)

    r = client.post("/v1/orders/%23ORD-1232/handover", json={"pickupOtp": "4921"})
    check("POST /v1/orders/{id}/handover", r.status_code == 200, r.text)

    r = client.get("/v1/orders/history?page=1&limit=20")
    check("GET /v1/orders/history", r.status_code == 200 and "orders" in r.json(), r.text)

    print("\n--- 6. Section 5: Food Menu & Customizations ---")
    r = client.get("/v1/menu/categories")
    check("GET /v1/menu/categories", r.status_code == 200 and len(r.json()) > 0, r.text)

    r = client.get("/v1/menu/items")
    check("GET /v1/menu/items", r.status_code == 200 and len(r.json()) > 0, r.text)

    r = client.patch("/v1/menu/items/FOOD-101/availability", json={"available": True})
    check("PATCH /v1/menu/items/{id}/availability", r.status_code == 200, r.text)

    r = client.get("/v1/menu/addons")
    check("GET /v1/menu/addons", r.status_code == 200 and isinstance(r.json(), list), r.text)

    print("\n--- 7. Section 6: Offers & Discounts ---")
    r = client.get("/v1/offers")
    check("GET /v1/offers", r.status_code == 200 and len(r.json()) > 0, r.text)

    r = client.post(
        "/v1/offers",
        json={
            "name": "Festive 25",
            "code": "FEST25",
            "discountType": "Percentage",
            "discountValue": 25.0,
            "minOrder": 300.0,
            "startDate": "2026-11-20",
            "endDate": "2026-11-30",
        },
    )
    check("POST /v1/offers", r.status_code == 201 and "code" in r.json(), r.text)

    print("\n--- 8. Section 7: Restaurant Timing & Working Hours ---")
    r = client.get("/v1/restaurant/timings")
    check("GET /v1/restaurant/timings", r.status_code == 200 and "workingDays" in r.json(), r.text)

    r = client.put(
        "/v1/restaurant/timings",
        json={
            "workingDays": {"Monday": True, "Tuesday": True, "Wednesday": True},
            "openingTime": "10:00",
            "closingTime": "23:00",
            "hasBreakTime": False,
        },
    )
    check("PUT /v1/restaurant/timings", r.status_code == 200, r.text)

    print("\n--- 9. Section 8: Financials, Earnings & Settlements ---")
    r = client.get("/v1/earnings?period=today")
    check("GET /v1/earnings?period=today", r.status_code == 200 and "netEarnings" in r.json(), r.text)

    r = client.get("/v1/earnings/settlements")
    check("GET /v1/earnings/settlements", r.status_code == 200 and len(r.json()) > 0, r.text)

    r = client.get("/v1/earnings/settlements/SETL-2026-9842/download")
    check(
        "GET /v1/earnings/settlements/{id}/download (PDF)",
        r.status_code == 200 and r.headers.get("content-type") == "application/pdf",
        r.headers.get("content-type", ""),
    )

    print("\n--- 10. Section 9: Customer Reviews & Ratings ---")
    r = client.get("/v1/reviews")
    check("GET /v1/reviews", r.status_code == 200 and "breakdown" in r.json(), r.text)

    r = client.post("/v1/reviews/REV-1/reply", json={"replyText": "Thank you for loving our food!"})
    check("POST /v1/reviews/{id}/reply", r.status_code == 200, r.text)

    print("\n--- 11. Section 10: Notifications ---")
    r = client.get("/v1/notifications")
    check("GET /v1/notifications", r.status_code == 200 and len(r.json()) > 0, r.text)

    r = client.patch("/v1/notifications/NOTIF-1/read")
    check("PATCH /v1/notifications/{id}/read", r.status_code == 200 and r.json().get("status") == "Read", r.text)

    r = client.post("/v1/notifications/read-all")
    check("POST /v1/notifications/read-all", r.status_code == 200, r.text)

    print("\n--- 12. Section 11: Restaurant & Owner Profile ---")
    r = client.get("/v1/restaurant/profile")
    check("GET /v1/restaurant/profile", r.status_code == 200 and "restaurantName" in r.json(), r.text)

    r = client.put("/v1/restaurant/profile", json={"restaurantName": "Royal Spice Kitchen"})
    check("PUT /v1/restaurant/profile", r.status_code == 200, r.text)

    print("\n--- 13. Section 12: Help & Support Tickets ---")
    r = client.post(
        "/v1/support/tickets",
        data={
            "issueType": "Order Payment Issue",
            "orderId": "#ORD-1234",
            "description": "Payout check discrepancy",
        },
    )
    check("POST /v1/support/tickets", r.status_code == 201 and "ticketId" in r.json(), r.text)

    print("\n--- 14. Section 13: Settings & Security ---")
    r = client.post(
        "/v1/settings/change-password",
        json={
            "currentPassword": "Password@123",
            "newPassword": "Password@123",
            "confirmPassword": "Password@123",
        },
    )
    check("POST /v1/settings/change-password", r.status_code == 200, r.text)

    r = client.put(
        "/v1/settings/notifications",
        json={
            "orderAlertsSound": True,
            "soundVolume": "High",
            "payoutWhatsappUpdates": True,
            "marketingOffers": False,
        },
    )
    check("PUT /v1/settings/notifications", r.status_code == 200, r.text)

    print(f"\n==========================================")
    print(f"Results: {passed} PASSED, {failed} FAILED")
    print(f"==========================================")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    test_suite()
