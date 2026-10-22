# NOBLESSE MOTOR CARS

**Curated Luxury & Automotive Precision Management Platform**

![Django](https://img.shields.io/badge/Django-5.2-0C4B33?style=for-the-badge&logo=django&logoColor=white)

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)

![Styling](https://img.shields.io/badge/CSS3-Zero--Framework%20Native-1572B6?style=for-the-badge&logo=css3&logoColor=white)

![Lenis](https://img.shields.io/badge/Lenis-v1.3%20Smooth%20Scroll-d4af37?style=for-the-badge)

![Database](https://img.shields.io/badge/SQLite-Relational-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

---

## 🏛️ Executive Summary

**Noblesse Motor Cars** is a bespoke, enterprise-grade automotive dealership platform and digital showroom. Built on Django 5, the application bridges high-end luxury brand aesthetics with computational rigor—delivering single-price transparency, real-time inventory discovery, white-glove VIP test drive booking, and client collection management.

### 🎨 The 60-30-10 Luxury Design System

The platform strictly adheres to the golden ratio of interior and architectural visual design:

- **60% Obsidian Black & Charcoal (`#08080a`, `#121215`, `#16161c`)**: Immersive, dark-mode canvas evoking exclusive sanctuary lighting.
- **30% Crisp White & Platinum Silver (`#ffffff`, `#e2e2e7`, `#9c9ca4`)**: High-contrast typography and subtle structural separation.
- **10% Imperial 24K Gold (`#d4af37`, `#fae392`, `#9e7a2b`)**: Focused visual accents for primary CTAs, bespoke emblems, and status indicators.

---

## ✨ Feature Suite

### 1. Curated Digital Showroom & Vault (`/inventory/`)

- **Multi-Factor Filter Engine:** Query vehicles dynamically by Silhouette (_Coupe, Sedan, SUV, Grand Tourer_), Powertrain (_Electric, Performance Hybrid, Petrol_), or custom search keyword.
- **Smart Sorting:** Real-time ordering by Price (_Ascending / Descending_), Newest Arrival, Mileage, and Model Year.
- **Custom Floating Dropdown:** Hardware-accelerated custom dropdown component with auto-blur dismissal and elevated stacking contexts (`z-index: 300`).
- **Philippine Peso Currency:** Native single-price formatting across all collections (`₱5,500,000.00`).

### 2. Interactive Vehicle Dossier (`/vehicle/<id>/`)

- **Cinematic Gallery:** Main high-definition viewport paired with interactive multi-angle thumbnail previewers.
- **Comprehensive Engineering Specifications:** Fuel delivery, transmission ratios, bespoke color code, and odometer ratings.
- **Aerospace Diagnostic Certification:** Transparent vehicle inspection badges and single-price guarantees.
- **Related Acquisitions:** Context-aware vehicle recommendations based on shared silhouettes and powertrains.

### 3. VIP Concierge & Test Drive Dispatch (`/appointments/`)

- **Private Sanctuary Viewings:** Schedule test drive consultations for specific vehicles.
- **Reference Generation:** Unique alpha-numeric appointment reference codes for client tracking.

### 4. Client Portal & Collector Dashboard (`/accounts/`)

- **Curated Vault Saves:** Registered collectors can bookmark and track prospective vehicle acquisitions.
- **Appointment Tracking:** Real-time visibility into scheduled private viewings, dates, and concierge notes.

### 5. Dynamic Dealership CMS & Staff Admin (`/admin/`)

- **Runtime Configurable Settings:** Manage dealership hours, sanctuary addresses, direct dispatch contact telephone numbers, and financing teaser rates without redeploying code.

---

## ⚡ Technical Architecture & Engineering Precision

- **Zero-Framework Native CSS:** Crafted without bloated CSS utility libraries. Employs modern CSS Custom Properties, flexbox/grid layout primitives, and glassmorphic surface blurs (`backdrop-filter: blur(24px)`).
- **Hardware-Accelerated Floating Capsule Header:** Header is promoted to its own GPU composite layer (`transform: translateZ(0); will-change: transform;`) with state-guarded scroll throttling.
- **Optimized Lenis Smooth Scroll:** Integrated with Lenis v1.3 with automated animation lifecycle control, preventing requestAnimationFrame recursion leaks.
- **Custom SVG Vector Identity:** Hand-crafted responsive SVG crest featuring aerodynamic wings, obsidian gradient shield, and gold drop-shadow filters.
- **Secure Database Practice:** SQLite database binaries are strictly ignored by Git to protect user credentials and transactional appointments.

---

## 🚀 Quickstart & Local Setup

### Prerequisites

- **Python 3.12+**
- **Git**

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/<your-username>/comms-daniel-cms.git
   cd comms-daniel-cms
   ```

1. **Initialize and Activate Virtual Environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

1. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

1. **Run Database Migrations:**

   ```bash
   python manage.py migrate
   ```

1. **Create an Administrative Superuser (Optional):**

   ```bash
   python manage.py createsuperuser
   ```

1. **Start the Development Server:**

   ```bash
   python manage.py runserver
   ```

   Navigate to `http://127.0.0.1:8000/` in your browser.

---

## 📂 Repository Anatomy

```
comms-daniel-cms/
├── config/                 # Django core project configuration & ASGI/WSGI
│   ├── settings.py         # Global settings & static/media directory config
│   ├── urls.py             # Root URL routing
│   └── wsgi.py
├── showroom/               # Landing, showroom inventory, and vehicle detail views
│   ├── templates/showroom/ # home.html, inventory_list.html, vehicle_detail.html
│   └── views.py            # Aggregate aggregation, search logic, dynamic settings
├── inventory/              # Vehicle catalog ORM models and migrations
│   └── models.py           # Vehicle, VehicleImage, SavedVehicle, DealershipSetting
├── appointments/           # Client scheduling and private viewing requests
│   └── models.py           # Appointment, AppointmentSlot
├── accounts/               # VIP client onboarding and dashboard
│   └── templates/accounts/ # login.html, register.html, dashboard.html
├── static/                 # Static vector brand identity and assets
│   └── img/
│       ├── noblesse-logo.svg
│       └── favicon.svg
├── media/                  # Uploaded vehicle photography assets
├── manage.py               # Django management utility
└── requirements.txt        # Pinned project dependencies
```

---

## 👤 Systems Architect & Lead Developer

- **Daniel John Villarmino** — _Systems Architect & Lead Developer_
- **Dealership Sanctuary:** 29 Congressional Ave, Project 8, Quezon City, 1106 Metro Manila
- **Concierge Telephone:** 0985 123 8888

---
