# PG Food Delivery Management System — Admin Panel & Partner FastAPI

A production-grade, enterprise Food Delivery Management System combining:
1. **Django Tabler Pro Admin Panel**: A dashboard built with **Python Django**, **PostgreSQL**, and the **Purchased Tabler Pro Admin Template** (Bootstrap 5, Tabler Icons, ApexCharts, Dark/Light theme toggle).
2. **FastAPI Partner App API**: A high-performance API backend implementing all 13 partner operational sections with JWT authentication, PostgreSQL integration, and Swagger UI at `/docs`.

---

## 1. System Architecture & Tech Stack

- **Backend Web Frameworks**:
  - **Django 6+**: Admin authentication, session security, ORM models, Tabler Pro views, migrations.
  - **FastAPI**: Asynchronous REST API backend serving the PG Partner Mobile & Web applications.
  - **Unified ASGI Server**: Dual-dispatch in `config/asgi.py` routing `/v1/*`, `/docs`, `/redoc`, and `/openapi.json` to FastAPI, and all other routes to Django.
- **Database**: PostgreSQL 18 (Database: `pgfood`, port: `5432`)
- **Frontend Template**: Purchased Tabler Pro (v1.4.0) with Bootstrap 5
- **Icons**: Tabler SVG Icons
- **Theme Engine**: Single-click rounded-corner button with shadow toggling between **Light Mode** and **Dark Mode** across login, dashboard, and management views (persisted in `localStorage` with zero-flash rendering).
- **Authentication**:
  - Admin Panel: Session-based Django authentication with email identifier and password hashing.
  - Partner App: Bearer JWT token authentication (`pyjwt`, `HS256`, 7-day expiry).

---

## 2. Directory Structure

```text
pgfood/
│
├── config/                         # Django & ASGI Configuration
│   ├── settings.py                 # PostgreSQL, Installed Apps, Security
│   ├── urls.py                     # Root routing table
│   ├── wsgi.py                     # WSGI gateway
│   └── asgi.py                     # Unified ASGI dispatcher (FastAPI + Django)
│
├── api/                            # FastAPI Partner Application Backend
│   ├── main.py                     # FastAPI app, CORS, OpenAPI metadata, router assembly
│   ├── config.py                   # JWT secret, algorithm, token expiry
│   ├── auth.py                     # JWT token generator, hasher, HTTPBearer dependency
│   ├── schemas.py                  # Pydantic v2 validation models
│   └── routers/                    # 13 Operational Sections
│       ├── auth.py                 # 1. Login, OTP, Password Reset, Logout
│       ├── registration.py         # 2. Partner Onboarding (Steps 1–7)
│       ├── dashboard.py            # 3. Dashboard Stats & Outlet Availability
│       ├── orders.py               # 4. Orders Pipeline (New, Prep, Ready, Handover)
│       ├── menu.py                 # 5. Menu Categories, Items, Add-ons
│       ├── offers.py               # 6. Active Offers & Discounts
│       ├── timings.py              # 7. Working Hours & Break Schedules
│       ├── earnings.py             # 8. Earnings & PDF Settlement Statements
│       ├── reviews.py              # 9. Customer Reviews & Merchant Replies
│       ├── notifications.py        # 10. Notifications (Read / Read-All)
│       ├── profile.py              # 11. Restaurant & Owner Profile
│       ├── support.py              # 12. Support Tickets & Document Attachments
│       └── settings.py             # 13. Change Password & Notification Preferences
│
├── apps/
│   ├── accounts/                   # Admin Authentication & Superuser
│   │   ├── models.py               # Custom User model (Email as identifier)
│   │   ├── forms.py                # Admin login, profile, password change forms
│   │   ├── views.py                # Accounts views
│   │   └── urls.py                 # /accounts/login/, /logout/, /profile/
│   │
│   └── partners/                   # PostgreSQL Models Shared by Admin & FastAPI
│       ├── models.py               # Partner, PartnerApplication, PartnerRestaurant,
│       │                           # MenuCategory, FoodItem, AddonGroup, PartnerOrder,
│       │                           # PartnerOffer, SupportTicket, PartnerNotification,
│       │                           # SettlementRecord, CustomerReview
│       ├── management/commands/    # Seed script: seed_partner_data.py
│       └── migrations/             # Database migrations
│
├── dashboard/                      # Tabler Pro Admin Dashboard App
│   ├── views.py                    # Dashboard, Partner Applications, Restaurants, Orders, Menu
│   ├── urls.py                     # /dashboard/, /partner-applications/, /restaurants/, /orders/, /menu/
│   ├── services.py                 # KPI calculation, sales charts & activity feed
│   └── tests.py                    # 17 comprehensive Django integration tests
│
├── templates/
│   ├── layouts/
│   │   ├── base.html               # Main dashboard layout (Sidebar + Header + Page Content)
│   │   └── auth.html               # Login page layout
│   ├── includes/
│   │   ├── sidebar.html            # Sidebar with active links and Swagger API Docs
│   │   └── header.html             # Top navbar with 1-click theme toggle & API Docs pill
│   └── dashboard/
│       ├── index.html              # Main Admin Dashboard (KPIs, ApexCharts, Recent Orders)
│       ├── partner_applications.html # Review & verify onboarding applications
│       ├── restaurants.html        # Manage restaurant outlets & online states
│       ├── orders.html             # Live kitchen & delivery orders pipeline
│       └── menu.html               # Food categories & dish availability management
│
├── run_api.py                      # Standalone launcher for FastAPI (port 8001)
├── test_api.py                     # Automated test suite for all 13 FastAPI sections (41 tests)
├── manage.py
└── requirements.txt
```

---

## 3. Partner API Specification (13 Sections)

Base URL: `http://localhost:8000/v1` (or `http://localhost:8001/v1`)
Interactive Swagger Docs: `http://localhost:8000/docs` (or `http://localhost:8001/docs`)

| Section | Endpoint | Method | Description |
|---|---|---|---|
| **1. Auth & Password Reset** | `/v1/auth/login` | POST | Partner login with mobile/email & password |
| | `/v1/auth/forgot-password` | POST | Request 6-digit OTP for password reset |
| | `/v1/auth/verify-otp` | POST | Verify OTP & receive verification token |
| | `/v1/auth/reset-password` | POST | Set new password with verification token |
| | `/v1/auth/logout` | POST | Invalidate device push token & logout |
| **2. Onboarding & Registration** | `/v1/registration/owner-details` | POST | Step 1: Owner name, phone, email, password |
| | `/v1/registration/restaurant-details` | POST | Step 2: Name, cuisines, cover & logo images |
| | `/v1/registration/address` | POST | Step 3: Street, area, city, pincode, GPS |
| | `/v1/registration/documents` | POST | Step 4: PAN, GST, FSSAI certificates |
| | `/v1/registration/bank-details` | POST | Step 5: Account holder, IFSC, bank name |
| | `/v1/registration/submit` | POST | Step 6: Review & submit application |
| | `/v1/registration/status` | GET | Step 7: Check verification & approval status |
| **3. Dashboard & Availability** | `/v1/dashboard/stats` | GET | Order counts, revenue, rating & pipeline |
| | `/v1/restaurant/status` | GET / PUT | Toggle outlet ONLINE / OFFLINE with reason |
| **4. Orders Pipeline** | `/v1/orders?status=new` | GET | List incoming orders awaiting acceptance |
| | `/v1/orders/{id}/accept` | POST | Accept order and set preparation time |
| | `/v1/orders/{id}/reject` | POST | Reject order with operational reason |
| | `/v1/orders/{id}` | GET | Full order details with items, bill, payment |
| | `/v1/orders/{id}/prep-time` | PATCH | Extend preparation time by N minutes |
| | `/v1/orders/{id}/ready` | POST | Mark order ready for pickup & generate OTP |
| | `/v1/orders/{id}/handover` | POST | Verify pickup OTP and handover to rider |
| | `/v1/orders/history` | GET | Paginated historical orders with filters |
| **5. Food Menu & Customizations** | `/v1/menu/categories` | GET / POST | List & create menu categories |
| | `/v1/menu/categories/{id}` | PUT / DELETE | Update category details or delete |
| | `/v1/menu/items` | GET / POST | List food items with filters & add new dish |
| | `/v1/menu/items/{id}` | PUT / DELETE | Edit food dish or remove from catalog |
| | `/v1/menu/items/{id}/availability` | PATCH | Instant In-Stock / Out-of-Stock toggle |
| | `/v1/menu/addons` | GET / POST | Customization groups (sizes, toppings) |
| | `/v1/menu/addons/{id}` | DELETE | Remove add-on group |
| **6. Offers & Discounts** | `/v1/offers` | GET / POST | List active coupons & create new offer |
| | `/v1/offers/{id}` | DELETE | Deactivate coupon code |
| **7. Restaurant Timing** | `/v1/restaurant/timings` | GET / PUT | Working days, opening/closing, break hours |
| **8. Financials & Settlements** | `/v1/earnings?period=today` | GET | Gross sales, platform commission, net payout |
| | `/v1/earnings/settlements` | GET | Settlement payout history & UTR records |
| | `/v1/earnings/settlements/{id}/download` | GET | Download official PDF settlement statement |
| **9. Customer Reviews** | `/v1/reviews?page=1` | GET | Average rating, star breakdown & reviews |
| | `/v1/reviews/{id}/reply` | POST | Submit merchant response to review |
| **10. Notifications** | `/v1/notifications` | GET | Notification feed (orders, alerts, payouts) |
| | `/v1/notifications/{id}/read` | PATCH | Mark single notification as read |
| | `/v1/notifications/read-all` | POST | Mark all notifications as read |
| **11. Profile Management** | `/v1/restaurant/profile` | GET / PUT | View & update restaurant & owner details |
| **12. Help & Support Tickets** | `/v1/support/tickets` | POST | Submit multipart ticket with file attachment |
| **13. Settings & Security** | `/v1/settings/change-password` | POST | Change partner account password |
| | `/v1/settings/notifications` | PUT | Sound alerts, volume & WhatsApp preferences |

---

## 4. Admin Panel Features

- **Dashboard Overview (`/dashboard/`)**:
  - 4 Key Statistics Cards (Total Orders, Total Revenue, Total Restaurants, Delivery Fleet).
  - Dual ApexCharts: Sales Overview (with Daily / Weekly / Monthly dynamic toggle) and Order Status Distribution.
  - Recent Orders table with customer avatars, payment status, and order details.
  - Platform Activity timeline feed.
- **Partner Applications Verification (`/dashboard/partner-applications/`)**:
  - Live review queue for onboarded restaurants.
  - Review Modal displaying FSSAI, PAN, GST, and bank verification status.
  - One-click **Approve & Activate** or **Reject** with compliance remarks.
- **Restaurants & Outlets (`/dashboard/restaurants/`)**:
  - Verified outlet management with ratings, reviews, owner contact, and store state.
  - Instant action buttons: **Pause Orders / Go Online** and **Suspend / Resume**.
- **Live Orders Pipeline (`/dashboard/orders/`)**:
  - Live view across all fulfillment states: New, Preparing, Ready at Counter, In Transit, Delivered.
  - Quick stage progression buttons (Accept -> Mark Ready -> Handover -> Complete).
- **Food Catalog & Menu (`/dashboard/menu/`)**:
  - Categories overview with dish counts.
  - Food dishes table with Veg / Non-Veg badges, prices, and one-click In-Stock / Out-of-Stock toggles.
- **Top Navigation & Theme**:
  - Interactive **Swagger API Docs** pill button in the top navigation and sidebar.
  - **1-Click Theme Switcher**: Rounded button with shadow toggling Light & Dark modes without dropdown friction.
  - Profile dropdown with My Profile and Change Password.

---

## 5. Installation & Setup Instructions

### Prerequisites
- Python 3.12+ (or 3.14)
- PostgreSQL running on port 5432 (default dbname: `pgfood`, user: `postgres`, password: `1234`)

### 1. Activate Environment
```bash
.\.venv\Scripts\Activate.ps1
```

### 2. Configure Environment (`.env`)
```ini
SECRET_KEY=pgfood-delivery-admin-secret-key-phase1-super-secure-2026
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,testserver

DB_NAME=pgfood
DB_USER=postgres
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=5432
```

### 3. Run Migrations & Seed Sample Data
```bash
python manage.py migrate
python manage.py seed_partner_data
```

---

## 6. Running the Applications

### Option A: Unified ASGI Server (Recommended — Serves Both on Port 8000)
Runs both the Django Tabler Admin Panel and the FastAPI Partner API on the same port:
```bash
uvicorn config.asgi:application --host 127.0.0.1 --port 8000 --reload
```
- Admin Panel: `http://127.0.0.1:8000/`
- Partner API Swagger Docs: `http://127.0.0.1:8000/docs`
- Partner API ReDoc: `http://127.0.0.1:8000/redoc`
- API Base URL: `http://127.0.0.1:8000/v1`

### Option B: Dual Independent Processes
- **Django Admin Panel** (Port 8000):
  ```bash
  python manage.py runserver 8000
  ```
- **FastAPI Partner API** (Port 8001):
  ```bash
  python run_api.py
  ```
  FastAPI Swagger Docs: `http://127.0.0.1:8001/docs`

---

## 7. Running the Test Suites

### 1. FastAPI Partner API Test Suite (41 Tests across all 13 sections)
```bash
python test_api.py
```
Output:
```text
Results: 41 PASSED, 0 FAILED
```

### 2. Django Admin Panel Test Suite (17 Tests)
```bash
python manage.py test
```
Output:
```text
Ran 17 tests in 16.4s - OK
```

---

## 8. Default Credentials

- **Admin Panel Superuser**:
  - Email: `admin@pgfood.com`
  - Password: `AdminPassword123!`
- **Partner App Demo Account**:
  - Identifier: `9876543210` or `vikram@spicebox.com`
  - Password: `Password@123`
  - Partner ID: `PTR-9842`
  - Restaurant ID: `REST-842` (`Royal Spice Kitchen`)
