# Developer Handover Guide: Noblesse Motor Cars (Apex Autos CMS)

**Project Name:** Noblesse Motor Cars / Apex Autos CMS  
**Repository:** `comms-daniel-cms`  
**Stack:** Python 3.12+ · Django 5.2.17 · SQLite3 · Pillow  
**Handover Date:** October 2026  

---

## 1. Project Overview & Architecture

This application is a full-featured automotive dealership Content Management System (CMS) with an integrated public luxury showroom and customer appointment booking engine.

### Core Modules (`apps`):
- **`config/`**: Project-wide settings, root URL routing, WSGI/ASGI configurations, and media file delivery.
- **`showroom/`**: Customer-facing digital storefront.
  - Landing page (`/`) with real-time inventory search and filtering.
  - Vehicle detail page (`/vehicle/<pk>/`) with interactive multi-photo gallery and spec cards.
- **`inventory/`**: Data layer for vehicles and assets.
  - `Vehicle`: Year, make, model, body style, fuel type, transmission, mileage, price, status (`available`, `reserved`, `sold`), featured flag.
  - `VehicleImage`: Gallery images linked via ForeignKey with custom sort order (`upload_to="vehicles/%Y/%m/"`).
  - `SavedVehicle`: Customer bookmarks with unique constraints.
  - `DealershipSetting`: Key-value configuration store.
- **`appointments/`**: Service and test-drive scheduling module.
  - `AppointmentSlot`: Staff-managed booking windows with defined capacity and active status.
  - `Appointment`: Customer booking requests with unique reference codes (`APX-XXXXXXXX`), status (`pending`, `confirmed`, `cancelled`), and custom notes.
- **`accounts/`**: Customer authentication and portal.
  - Registration, login, logout, and authenticated dashboard (`/accounts/dashboard/`) displaying saved vehicles and active test-drive bookings.
- **`dashboard/`**: Scaffolded app for internal dealership staff metrics and operations.

---

## 2. Prerequisites & Quickstart

### Prerequisites
- Python 3.12 or newer
- `pip` package manager
- (Optional) `git`

### Setup Instructions

```bash
# 1. Unzip the project archive and enter directory
cd comms-daniel-cms

# 2. Create and activate a fresh virtual environment
python3 -m venv .venv
source .venv/bin/activate    # On Linux/macOS
# or: .venv\Scripts\activate # On Windows

# 3. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Verify system checks and migrations
python manage.py check
python manage.py migrate

# 5. Start the local development server
python manage.py runserver
```

Once running, access the application at **`http://127.0.0.1:8000/`**.

---

## 3. Seeded Accounts & Credentials

The pre-bundled SQLite database (`db.sqlite3`) comes pre-populated with active listings and test accounts:

| Role | Username / Identifier | Password | Access / Scope |
|---|---|---|---|
| **Superuser / Staff** | `apexadmin` | `admin123` | Full access to Django Admin (`/admin/`) & Showroom |
| **Staff Member** | `dollesinamerson@gmail.com` | `admin123` | Full access to Django Admin (`/admin/`) |
| **Customer** | `anaroxas` | `admin123` | Customer portal, save vehicles, book test drives |

### Management Commands
- **Reset password for any user:**
  ```bash
  python manage.py changepassword <username>
  ```
- **Create an additional superuser:**
  ```bash
  python manage.py createsuperuser
  ```

---

## 4. Key Endpoints & Routing Sitemap

| URL Pattern | View / Purpose | Auth Required |
|---|---|---|
| `/` | Public Showroom & Inventory Search | No |
| `/vehicle/<int:pk>/` | Vehicle Detail & Photo Gallery | No |
| `/accounts/login/` | Customer Sign In | No |
| `/accounts/register/` | Customer Registration | No |
| `/accounts/logout/` | Sign Out (POST) | Yes |
| `/accounts/dashboard/` | Customer Portal (Saved Cars & Bookings) | Yes |
| `/accounts/save/<int:vehicle_id>/` | Save / Bookmark Vehicle (POST) | Yes |
| `/appointments/request/<int:vehicle_id>/` | Request Test Drive / Consultation | Yes |
| `/admin/` | Staff & Management Admin Portal | Staff / Superuser |
| `/media/<path>` | Uploaded Vehicle Media Assets | No (`DEBUG=True`) |

---

## 5. Media & Database Handling

- **Database:** Uses local SQLite (`db.sqlite3`). If starting fresh or deploying to Postgres, run `python manage.py migrate`.
- **Media Files:** Stored in `media/vehicles/%Y/%m/`. Django is configured in `config/urls.py` to serve media automatically while `DEBUG = True`.
- **Image Uploads:** Handled via Pillow (`pillow==12.3.0`). Multiple photos per vehicle are supported through inline forms in the admin portal (`VehicleImageInline`).

---

## 6. Developer Guidelines & Extension Ideas

1. **Brand Identity:**
   - Public facing brand tokens are defined in `:root` inside templates: `--ink: #06131f`, `--cyan: #64e7f3`, `--cyan-dark: #268da0`, `--mist: #f1f7f8`.
2. **Adding Appointment Kinds:**
   - In `appointments/models.py` and `appointments/views.py`, you can extend appointment types (currently supports `test_drive`, `consultation`, `trade_in`).
3. **Staff Dashboard:**
   - The `dashboard` app is registered in `INSTALLED_APPS` and can be expanded with analytics (total stock value, leads generated, scheduled drives).
