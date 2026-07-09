# 📊 Kautex Resource & Cost Planning Platform

> **Kautex Craiova Hackathon 2026 Deliverable**
> A Streamlit-powered platform for digitizing engineering headcount, enforcing capacity allocation rules, and tracking multi-level project costs.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Database](https://img.shields.io/badge/DB-SQLite%20%7C%20PostgreSQL-336791.svg)](#)
[![License](https://img.shields.io/badge/License-Internal--Kautex-lightgrey.svg)](#-license)
[![Status](https://img.shields.io/badge/Status-Hackathon%20Prototype-yellow.svg)](#-team-review--action-items)

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features-implemented)
- [Tech Stack](#-tech-stack)
- [Quickstart](#️-quickstart-running-locally)
- [Project Architecture](#-project-architecture)
- [Deployment Guide](#️-deployment-guide-supabase-integration)
- [Default Credentials](#-default-local-credentials)
- [Roadmap](#-roadmap)
- [Team Review & Action Items](#-team-review--action-items)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Overview

This application transitions resource planning from manual spreadsheets to a centralized, secure web dashboard. It allows engineering managers to maintain a live headcount roster, dynamically allocate employee capacity to specific projects (enforcing a strict **100% capacity rule**), and automatically aggregate internal and external costs into executive-facing reports.

Built during the **Kautex Craiova Hackathon 2026**, this prototype demonstrates a full end-to-end workflow — from data entry to executive reporting — replacing error-prone manual spreadsheet tracking with a governed, auditable system.

---

## ✨ Key Features Implemented

| Feature | Description |
|---|---|
| 🔐 **Secure RBAC Authentication** | Role-based access control with `bcrypt` password hashing. Admins have full CRUD access; regular employees/viewers have restricted read-only or scoped access. |
| 🎯 **Interactive Allocation Matrix** | A live, editable data grid that tracks employee project assignments and instantly flags under/over-utilization. |
| 💰 **Automated Cost Engine** | Calculates internal personnel costs (hours × rate × allocation) and aggregates them with external tooling, testing, and recovery costs. |
| 📈 **Executive Dashboard** | Real-time KPIs, Plotly/Altair visualizations, and automatic alerts for high-cost projects (where external costs exceed 30% of the budget). |
| 🔄 **Bulk Data Operations** | One-click CSV imports for mass onboarding (Employees, Topics, Allocations) and comprehensive Excel/CSV reporting exports. |

---

## 💻 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit, Altair, Plotly |
| **Backend & Logic** | Python 3.10+, Pandas |
| **Database & ORM** | SQLite (local) / PostgreSQL via Supabase (cloud-ready), SQLModel |
| **Security** | `bcrypt`, Streamlit Session State |

---

## 🛠️ Quickstart (Running Locally)

### 1. Navigate to the core application folder
```bash
cd resource_planning_app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize the database
This creates the local SQLite database and seeds default data:
```bash
python -m database.init_db
python -m database.seed
```

### 4. Launch the app
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501` by default.

### 🔑 Default Local Credentials

| Role | Username | Password | Access Level |
|---|---|---|---|
| Admin | `admin` | `Admin123!` | Full access (CRUD) |
| Viewer | `viewer` | `Viewer123!` | Read-only |

> ⚠️ **Security Note:** These are default seed credentials for local development only. Change them immediately before any shared or production deployment.

---

## 🏗️ Project Architecture

The codebase follows a modular **Service-Layer pattern** to ensure scalability and clean separation of concerns.

```
resource_planning_app/
├── app.py                     # Main entry point & session router
├── app_theme.py                # Global UI styling and chart configurations
├── app_pages/                  # Modular UI views (Dashboard, Matrix, Reports)
├── database/                   # Connection engine and initialization scripts
├── models/                     # SQLModel database schemas (Employees, Topics, Costs)
├── services/                   # Business logic, CRUD operations, and I/O handlers
└── utils/                      # Pure mathematical calculators for capacity & cost
```

**Layer responsibilities:**

- **`app.py`** — Bootstraps the Streamlit session, handles routing between pages based on auth state and role.
- **`app_pages/`** — Presentation layer only; each page renders UI and delegates all logic to `services/`.
- **`services/`** — Encapsulates business rules (capacity validation, cost aggregation, CSV import/export) so UI and data-access concerns stay decoupled.
- **`models/`** — SQLModel entities defining the schema for Employees, Topics/Projects, Allocations, and Costs.
- **`database/`** — Engine setup, migrations, and seeding scripts; abstracts SQLite vs. PostgreSQL.
- **`utils/`** — Stateless helper functions for capacity math and cost formulas, kept independent for easy unit testing.

---

## ☁️ Deployment Guide (Supabase Integration)

The application is fully pre-configured to run on a cloud-hosted PostgreSQL database via [Supabase](https://supabase.com/).

### 1. Create the secrets file
Create a `.streamlit` folder inside `resource_planning_app/`, then inside it create a `secrets.toml` file.

### 2. Add your Supabase connection string
```toml
DATABASE_URL = "postgresql://postgres.[your-project-ref]:[your-password]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
```

> 🔒 **Important:** Ensure `.streamlit/secrets.toml` remains listed in `.gitignore` to prevent credential leaks.

### 3. Run the migration script
Sync your local schemas to the cloud:
```bash
python -m database.migrate_to_supabase
```

### 4. Deploy
Once the schema is synced, the app can be deployed to Streamlit Community Cloud (or any host supporting Streamlit) by pointing it at the same repository and configuring the `DATABASE_URL` secret in the deployment environment.

---

## 🗺️ Roadmap

Potential next steps beyond the hackathon prototype:

- [ ] Automated unit tests for `utils/calculations.py`
- [ ] Audit log for allocation and cost changes
- [ ] Email/Slack alerts for over-utilization or budget threshold breaches
- [ ] Multi-project timeline / Gantt view
- [ ] Role granularity beyond Admin/Viewer (e.g., Project Lead scoped access)

---

## ✅ Team Review & Action Items

This branch represents the fully functional core loop for the hackathon prototype. Before merging to `main`, team feedback is requested on the following:

1. **UX Flow** — Does the Allocation Matrix tab feel intuitive for mass-editing capacities?
2. **Cost Logic** — Please review `utils/calculations.py` to ensure the internal/external cost aggregation perfectly matches the Kautex financial guidelines.
3. **Role Segregation** — Verify that the Admin vs. Viewer restrictions in `app.py` meet our exact security requirements.

📝 Please drop your feedback in the PR comments!

---

## 🤝 Contributing

1. Create a feature branch from `main`.
2. Follow the existing Service-Layer pattern — keep business logic out of `app_pages/`.
3. Run and update seed data as needed for local testing.
4. Open a PR summarizing changes and referencing the relevant action item(s) above.

---

## 📄 License

Internal deliverable developed for the **Kautex Craiova Hackathon 2026**. Not licensed for external distribution unless otherwise approved by Kautex.

---

<p align="center">Built with ❤️ for the Kautex Craiova Hackathon 2026</p>