# 📊 Kautex Resource & Cost Planning Platform

> A Streamlit web application for planning engineering headcount, allocating employees to
> projects, and tracking multi-level project costs — built for the Kautex Hackathon 2026.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B.svg)](https://streamlit.io/)
[![Database](https://img.shields.io/badge/database-Supabase%20%2F%20PostgreSQL-3ECF8E.svg)](https://supabase.com/)
[![ORM](https://img.shields.io/badge/ORM-SQLModel-informational.svg)](https://sqlmodel.tiangolo.com/)
[![License](https://img.shields.io/badge/license-Internal%20%2F%20Kautex-lightgrey.svg)](#license)

---

## Table of Contents

- [Overview](#overview)
- [Repository Layout](#repository-layout)
- [Core Application: `resource_planning_app/`](#core-application-resource_planning_app)
  - [Features](#features)
  - [Data Model](#data-model)
  - [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Configuration](#database-configuration)
  - [Seeding an Admin Account](#seeding-an-admin-account)
  - [Running the App](#running-the-app)
- [Sample Data](#sample-data)
- [Companion BI Dashboard Prototype](#companion-bi-dashboard-prototype)
- [Legacy / Early Scaffold Files](#legacy--early-scaffold-files)
- [Tech Stack](#tech-stack)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

This repository contains the deliverables built for the **Kautex Hackathon 2026**: a
resource-planning and cost-management tool that lets an engineering organization

- maintain a **headcount roster** (employees, teams, departments, locations),
- create **topics** (projects / initiatives) with objectives, deliverables, and status,
- **allocate** employees to topics as a percentage of their available capacity,
- track **cost items** (external tooling, testing, recovery) alongside computed internal
  personnel cost, and
- **export/import** data and generate executive-facing cost reports.

The project is organized as one primary deliverable plus supporting prototypes and
planning documents produced during the hackathon:

| Folder / File | Role |
|---|---|
| [`resource_planning_app/`](#core-application-resource_planning_app) | ✅ **The main application.** Multi-user Streamlit app with authentication, role-based access, and a shared Supabase/PostgreSQL database. |
| `kautex_bi_dashboard*.py` | 🧪 Standalone single-file executive BI dashboard **prototype/template** with mock data (see [below](#companion-bi-dashboard-prototype)). |
| `app.py`, `Login.py`, root `requirements.txt` | 🕰️ An earlier scaffold of the app that predates `resource_planning_app/` (see [Legacy files](#legacy--early-scaffold-files)). |
| `seed_employee.csv`, `seed_topics.csv`, `Hackathon Database (Good).csv` | 📄 Sample/seed data used to populate and demo the app. |
| `QUICKSTART.md`, `DEPLOYMENT_GUIDE.md`, `FEATURES_COMPLETE.md`, `DELIVERY_SUMMARY.md`, `INDEX.md` | 📚 Additional planning/handoff notes written earlier in the project. Where they conflict with this README or with the code in `resource_planning_app/`, **this README and the code are the source of truth.** |

---

## Repository Layout

```
Hackaton-Kautex-2026/
├── README.md                        ← you are here
├── requirements.txt                 ← dependencies for the legacy root scaffold
├── app.py / Login.py                ← legacy scaffold entry points (superseded)
├── kautex_bi_dashboard*.py          ← standalone BI dashboard prototype + variants
├── seed_employee.csv                ← sample employee data (8 rows)
├── seed_topics.csv                  ← sample topic/project data
├── Hackathon Database (Good).csv    ← extended sample dataset
│
└── resource_planning_app/           ← ★ THE MAIN APPLICATION ★
    ├── app.py                       # Entry point: auth + role-based navigation
    ├── app_theme.py                 # Shared Kautex styling, charts, helpers
    ├── requirements.txt
    ├── .streamlit/
    │   ├── config.toml
    │   └── secrets.toml.example     # Template for the Supabase connection string
    ├── app_pages/
    │   ├── login.py                 # Login form
    │   ├── register.py              # Self-service employee sign-up
    │   ├── dashboard.py             # Live utilization & cost overview
    │   ├── employees.py             # Employee CRUD (admin only)
    │   ├── topics.py                # Topic CRUD + per-topic cost items
    │   ├── allocation_matrix.py     # Employee ↔ Topic allocation grid
    │   └── reports.py               # CSV/Excel export, bulk CSV import, cost report
    ├── database/
    │   ├── connection.py            # SQLModel engine, Supabase/Postgres connection
    │   ├── init_db.py               # Table creation
    │   ├── seed.py                  # Seeds one admin login for testing
    │   └── migrate_to_supabase.py   # One-off SQLite → Supabase migration script
    ├── models/                      # SQLModel table definitions
    │   ├── employee.py, team.py, department.py, location.py
    │   ├── topic.py, allocation.py, cost_item.py
    │   └── user.py
    ├── services/                    # Data-access / business-logic layer
    │   ├── employee_service.py, topic_service.py, allocation_service.py
    │   ├── cost_service.py          # Cost aggregation & high-cost topic detection
    │   ├── auth_service.py          # bcrypt hashing, register/login
    │   ├── export_service.py        # CSV / Excel exports
    │   └── import_service.py        # Bulk CSV import with validation
    ├── utils/
    │   └── calculations.py          # Pure cost & utilization math (unit-testable)
    └── data/
        └── planning.db              # Local SQLite artifact (used only by the
                                      # legacy migration script; the live app
                                      # reads/writes Supabase/Postgres)
```

---

## Core Application: `resource_planning_app/`

### Features

**🔐 Authentication & Roles**
- Username/password login with `bcrypt` password hashing.
- Self-service sign-up creates an **Employee**-role account; **Admin** accounts are
  seeded via `database/seed.py`.
- Role-based navigation: Admins see an extra **Employees** management page; both roles
  see Dashboard, Topics, Allocation Matrix, and Reports.

**👥 Employee Management** (admin only)
- Create, edit, and delete employee records: name, team, department, location,
  available hours/year, hourly rate, status, manager, notes.

**📌 Topic (Project) Management**
- Create, edit, and delete topics with category, area, objective, deliverables,
  business justification, status, and notes.
- Mass-import topics from CSV.
- Attach cost items to a topic (see below).

**🎯 Allocation Matrix**
- Assign any employee to any topic as a percentage of their capacity.
- Live utilization tracking per employee across all their topic assignments.
- Per-employee, per-topic cost computed automatically from hours, rate, and
  allocation percentage.

**💰 Multi-Level Cost Tracking**
Each topic's total cost is the sum of:
```
Total Cost = Internal Personnel Cost      (Σ allocated hours × hourly rate)
           + External Tooling
           + Testing
           − Recovery / rebilling
```
- Cost items are categorized as **External Tooling**, **Testing**, or **Recovery**
  and entered per topic.
- "High-cost" topics (external costs above a configurable share of total cost) are
  automatically flagged for executive review.

**📈 Dashboard**
- Live headcount, total cost, and average cost-per-employee metrics.
- Utilization charts and cost-distribution visualizations (Altair).

**📤 Reports — Export / Import**
- **Export:** Employees, Topics, and Allocations to CSV; a formatted Excel cost
  report; and an Excel allocation matrix.
- **Import:** Bulk CSV upload for employees, topics, and allocations, with
  per-row validation and an import summary.
- **Executive cost report**: global totals, per-topic cost breakdown, and
  high-cost topic flags in one view.

### Data Model

| Entity | Key Fields |
|---|---|
| `Employee` | name, team_id, department_id, location_id, available_hours_per_year, hourly_rate, status, manager, notes |
| `Team` | name, department_id, location_id, description |
| `Department` | name, description |
| `Location` | name, country, description |
| `Topic` | name, category, area, description, objective, deliverables, business_justification, status, notes |
| `Allocation` | employee_id (FK), topic_id (FK), allocation_percentage, comment |
| `CostItem` | topic_id (FK), cost_type (External Tooling / Testing / Recovery), amount, description |
| `User` | username, password_hash, role (admin / employee), employee_id (FK, optional) |

All tables are defined as [SQLModel](https://sqlmodel.tiangolo.com/) classes in
`resource_planning_app/models/` and created automatically on first run.

### Architecture

```
app_pages/  (Streamlit UI, one file per page)
     │
     ▼
services/   (business logic, CRUD, cost aggregation, import/export)
     │
     ▼
models/     (SQLModel ORM table definitions)
     │
     ▼
database/   (SQLModel engine → Supabase / PostgreSQL)
```

- **`utils/calculations.py`** holds pure, dependency-free functions (cost formulas,
  utilization checks) so the core business math can be unit-tested independently of
  Streamlit and the database.
- **`services/cost_service.py`** aggregates allocations and cost items in a single
  round trip per table (rather than one query per topic) to avoid N+1 queries against
  the hosted Supabase database.
- The **Reports** page uses `st.fragment` so that interacting with one tab (e.g. the
  import-type selector) doesn't force a full-page rerun of every other tab's queries.

---

## Getting Started

### Prerequisites

- Python 3.10+
- A [Supabase](https://supabase.com/) project (or any PostgreSQL database) — the app
  is designed to connect to a **shared** database rather than a local file, so every
  user sees the same data.

### Installation

```bash
cd resource_planning_app

# (recommended) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

### Database Configuration

The app reads its connection string from Streamlit secrets (or an environment
variable) and **fails loudly if it isn't set**, rather than silently falling back to
an empty local database.

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` and set your connection string (use the **Session
Pooler** URI from Supabase → Project Settings → Database → Connection string):

```toml
DATABASE_URL = "postgresql://postgres.xxxx:[PASSWORD]@aws-0-region.pooler.supabase.com:6543/postgres"
```

`secrets.toml` is gitignored — never commit real credentials.

> Alternatively, set `DATABASE_URL` as an environment variable instead of using
> `secrets.toml`.

### Seeding an Admin Account

```bash
python -m database.init_db     # creates all tables if they don't exist
python -m database.seed        # creates a default admin login (safe to re-run)
```

This prints a default admin username/password to the console. **Change the password
before using the app outside local testing.**

### Running the App

```bash
streamlit run app.py
```

The app opens on the login page. Log in with the seeded admin account, or use
**Sign up** to self-register a new employee account. Admins get an additional
**Employees** page; every role can access Dashboard, Topics, Allocation Matrix, and
Reports.

---

## Sample Data

Two ready-to-import CSV files are provided at the repository root for quickly
populating a fresh database via the Reports → Import tab:

- **`seed_employee.csv`** — sample headcount (name, team, department, location,
  available hours/year, hourly rate, status).
- **`seed_topics.csv`** — sample topics/projects (name, category, area, status).
- **`Hackathon Database (Good).csv`** — a larger combined sample dataset used during
  the hackathon demo.

---

## Companion BI Dashboard Prototype

`kautex_bi_dashboard.py` (and its `*_new.py` / `*_template.py` / `*.bak` variants) is
a **standalone, single-file** executive BI dashboard built with Streamlit, Pandas, and
Plotly. It is a design exploration/template — independent of `resource_planning_app/`
— intended to prototype an executive-facing visual layer (region filters, a
dark/light theme toggle, and a clickable world/region selector) on top of **mock
data**. It is not wired to the shared database and can be run on its own:

```bash
pip install streamlit pandas plotly
streamlit run kautex_bi_dashboard.py
```

The `.bak` / `_new` / `_template` files are earlier iterations of this same prototype,
kept for reference.

---

## Legacy / Early Scaffold Files

The root-level `app.py`, `Login.py`, and `requirements.txt` are an **earlier draft**
of the resource-planning app, written before it was reorganized into
`resource_planning_app/`. They reference a `pages/` directory and a `utils/auth.py`
module that no longer exist at the repository root, so **they are not runnable as-is**
and are kept only for historical reference. Use `resource_planning_app/` for anything
functional.

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI framework | [Streamlit](https://streamlit.io/) (multipage app, `st.navigation`) |
| ORM | [SQLModel](https://sqlmodel.tiangolo.com/) |
| Database | PostgreSQL via [Supabase](https://supabase.com/) |
| Data handling | Pandas |
| Charts | Altair (in-app), Plotly (BI dashboard prototype) |
| Auth | bcrypt password hashing |
| Export | OpenPyXL / XlsxWriter |

Exact pinned versions live in `resource_planning_app/requirements.txt`.

---

## Roadmap

- [ ] Split Admin vs. Employee dashboards once distinct UX designs are finalized
- [ ] "Forgot password" flow (currently a disabled placeholder on the login page)
- [ ] Persistent (cookie-based) login sessions
- [ ] PDF export for the executive cost report
- [ ] Historical/audit trail for allocation and cost changes

---

## Troubleshooting

| Issue | Likely Cause / Fix |
|---|---|
| `RuntimeError: DATABASE_URL is not set` | Create `.streamlit/secrets.toml` from the `.example` file, or set the `DATABASE_URL` environment variable. |
| `ModuleNotFoundError` | Re-run `pip install -r requirements.txt` inside `resource_planning_app/`, ideally in an active virtual environment. |
| Port `8501` already in use | `streamlit run app.py --server.port 8502` |
| Login fails after registering | Confirm the account was created (`database/seed.py` output, or check the `user` table) and that you're pointing at the same `DATABASE_URL` used during sign-up. |
| Import/export unusually slow | Confirm you're on a low-latency connection to the Supabase pooler; the Reports page batches queries specifically to minimize round trips. |

---

## License

© 2026 Kautex GmbH. Built for internal use as part of the Kautex Hackathon 2026.
All rights reserved.
