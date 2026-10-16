# Developer Handover Guide

## 1. Prerequisites & Quickstart

### Prerequisites

- Python 3.12 or newer
- `pip` package manager

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

## 2. Seeded Accounts & Credentials

The pre-bundled SQLite database (`db.sqlite3`) comes pre-populated with active listings and test accounts:

| Role                  | Username / Identifier       | Password   | Access / Scope                                     |
| --------------------- | --------------------------- | ---------- | -------------------------------------------------- |
| **Superuser / Staff** | `apexadmin`                 | `admin123` | Full access to Django Admin (`/admin/`) & Showroom |
| **Staff Member**      | `dollesinamerson@gmail.com` | `admin123` | Full access to Django Admin (`/admin/`)            |
| **Customer**          | `anaroxas`                  | `admin123` | Customer portal, save vehicles, book test drives   |

### Management Commands

- **Reset password for any user:**
  ```bash
  python manage.py changepassword <username>
  ```
- **Create an additional superuser:**
  ```bash
  python manage.py createsuperuser
  ```
