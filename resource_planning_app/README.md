# Resource Planning & Cost Management App

## Project Purpose

This is a Streamlit web application for planning and managing resources across
teams and topics/projects. It tracks employees, teams, departments, locations,
topic allocations, comments, and the resulting costs, so that resource planning
and cost reporting can happen in one place.

This repository currently contains the **initial project foundation** only:
project structure, database setup, base models, placeholder services, and
placeholder pages. Full functionality (CRUD, charts, reports) will be built
on top of this foundation.

## Tech Stack

- **Python** — application logic
- **Streamlit** — web interface (multipage app)
- **SQLite** — local database file
- **SQLModel** — ORM for defining and querying database tables
- **Pandas** — data handling and tabular manipulation
- **Plotly** — charts and visualizations

## Getting Started

### 1. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize the database

This creates `data/planning.db` and all required tables. The `data/` folder
is created automatically if it doesn't exist.

```bash
python -m database.init_db
```

### 4. Seed an admin account

Creates one admin login for testing (safe to re-run — skips if it already exists):

```bash
python -m database.seed
```

This prints the seeded username/password to the console. Change it before
using the app outside of local testing.

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

The app opens on the login page. Log in with the seeded admin account, or
use "Sign up" to self-register a new employee account. Admins see an extra
"Employees" page; both roles see Dashboard, Topics, Allocation Matrix, and
Reports (this split will be refined once the admin/employee dashboard
designs are finalized).

## Project Structure

```
resource_planning_app/
│
├── app.py                  # Main entry point / home page
├── requirements.txt        # Python dependencies
├── README.md
├── .gitignore
│
├── database/                # Database connection & initialization
│   ├── connection.py
│   ├── init_db.py
│   └── seed.py               # seeds one admin account for testing
│
├── models/                  # SQLModel table definitions
│   ├── employee.py
│   ├── team.py
│   ├── department.py
│   ├── location.py
│   ├── topic.py
│   ├── allocation.py
│   ├── cost_item.py
│   └── user.py                # login accounts (username, password hash, role)
│
├── services/                 # Data access layer (CRUD, placeholders for now)
│   ├── employee_service.py
│   ├── topic_service.py
│   ├── allocation_service.py
│   ├── cost_service.py
│   └── auth_service.py       # fully implemented: hashing, register, login
│
├── app_pages/                # Streamlit multipage app pages
│   ├── login.py
│   ├── register.py
│   ├── dashboard.py
│   ├── employees.py          # admin only
│   ├── topics.py
│   ├── allocation_matrix.py
│   └── reports.py
│
├── utils/                    # Pure helper functions (cost/utilization math)
│   └── calculations.py
│
└── data/                     # SQLite database file (planning.db)
```

## Notes on the `data/` folder

The `data/` folder (and `planning.db`) is **not** ignored by git, but the
database can always be recreated by running `python -m database.init_db`
again — it's safe to delete the file if you want to start fresh.
