# 📊 Kautex Resource & Cost Planning Tool

> A professional web-based resource planning and cost management application built for executive leadership teams

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-Kautex-blue.svg)](LICENSE)

---

## 🎯 Overview

The **Kautex Resource & Cost Planning Tool** is a comprehensive solution for managing global employee headcount, allocating resources to engineering projects, and tracking deep financial cost breakdowns with executive-level reporting.

### ✨ Key Highlights

- 🔐 **Secure Authentication** - Role-based login (Admin & Viewer roles)
- 💯 **100% Capacity Enforcement** - Prevents allocation errors automatically
- 💰 **Deep Cost Analysis** - Multi-level cost breakdowns (personnel, tooling, testing, recovery)
- 📊 **Executive Dashboard** - Real-time KPIs with Plotly visualizations
- 📤 **Data Management** - Export/Import capabilities (CSV, Excel)
- 🎨 **Professional Design** - Modern UI with Kautex branding
- 🚀 **Scalable Architecture** - Modular design with SQLModel ORM

---

## 📦 What's Inside

```
resource_planning_app/
├── login.py                        # 🔐 Secure login entry point
├── app.py                          # 📊 Main dashboard
├── requirements.txt                # 📋 Python dependencies
├── QUICKSTART.md                   # ⚡ 5-minute setup guide
├── DEPLOYMENT_GUIDE.md             # 🚀 Detailed deployment instructions
├── README.md                       # 📖 This file
├── assets/
│   └── kautex_logo.png            # 🎨 Professional branding
├── data/                           # 💾 Database storage
│   ├── planning.db                # SQLite database
│   └── users.json                 # User credentials
├── database/
│   ├── connection.py              # 🔌 Database engine
│   └── init_db.py                 # ⚙️ Initialization
├── models/
│   ├── employee.py                # 👥 Employee ORM
│   ├── topic.py                   # 📌 Topic/Project ORM
│   ├── allocation.py              # 🎯 Allocation ORM
│   └── cost_item.py               # 💳 Cost ORM
├── services/
│   ├── employee_service.py        # CRUD
│   ├── topic_service.py           # CRUD
│   ├── allocation_service.py      # CRUD
│   ├── cost_service.py            # CRUD
│   ├── export_service.py          # 📥 Export (CSV, Excel)
│   └── import_service.py          # 📤 Bulk import
├── pages/
│   ├── 1_Dashboard.py             # 📊 Executive overview
│   ├── 2_Employees.py             # 👥 Employee management
│   ├── 3_Topics.py                # 📌 Project management
│   ├── 4_Allocations.py           # 🎯 Allocation matrix
│   └── 5_Reports.py               # 📤 Reports & exports
└── utils/
    ├── calculations.py            # ⚙️ Business logic
    └── auth.py                    # 🔐 Authentication
```

---

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
cd C:\Users\eduar\resource_planning_app
pip install -r requirements.txt
```

### 2. Run Application
```bash
streamlit run login.py
```

### 3. Login
- **Username:** `admin`
- **Password:** `admin123`

### 4. Start Using
- Create employees
- Add projects (topics)
- Allocate resources (100% rule enforced)
- Monitor dashboard

**→ See `QUICKSTART.md` for detailed guide**

---

## 🎯 Core Features

### 1️⃣ **100% Capacity Rule**
The heart of the system - ensures every employee is allocated 100% across all projects:
```python
# Example
- Employee "John Smith":
  - Project A: 40% ✓
  - Project B: 60% ✓
  - Total: 100% ✅ (can save)
  
- If trying Project A (40%) + Project B (50%):
  - Total: 90% ❌ (blocked - "Remaining: 10%")
```

### 2️⃣ **Cost Calculation Engine**
Multi-level cost tracking:
```
Topic Total Cost = 
  Internal Personnel Cost (allocated hours × rate)
  + External Tooling
  + Testing Costs
  - Recovery (rebilling, etc.)
  
Global Total = Sum of all topics
```

### 3️⃣ **Executive Dashboard**
Real-time metrics:
- Total cost across all projects
- Total headcount
- Cost distribution by project (Plotly chart)
- High-cost project alerts
- Employee allocation status

### 4️⃣ **Role-Based Access**

| Role | Dashboard | CRUD | Export | Import |
|------|-----------|------|--------|--------|
| **Admin** | ✅ | ✅ | ✅ | ✅ |
| **Viewer** | ✅ (RO) | ❌ | ❌ | ❌ |

### 5️⃣ **Data Management**
- **Export:** CSV (employees, topics, allocations) + Excel (formatted reports)
- **Import:** Bulk upload via CSV with validation
- **Reports:** Cost analysis, allocation matrix, high-cost flags

---

## 💾 Database Schema

### Employee
```python
{
  id: int (PK),
  name: str,
  location: str,
  available_hours_per_year: int = 1600,
  hourly_rate: float,
  created_at: datetime,
  updated_at: datetime
}
```

### Topic
```python
{
  id: int (PK),
  name: str,
  category: str,  # "Internal Efforts", "Customer Request", etc.
  business_justification: str,
  created_at: datetime,
  updated_at: datetime
}
```

### Allocation
```python
{
  id: int (PK),
  employee_id: int (FK),
  topic_id: int (FK),
  allocation_percentage: float,  # 0.0 to 1.0
  comment: str,
  created_at: datetime,
  updated_at: datetime
}
```

### CostItem
```python
{
  id: int (PK),
  topic_id: int (FK),
  cost_type: str,  # "Tooling", "Testing", "Recovery"
  amount: float,   # Negative for recovery
  description: str,
  created_at: datetime,
  updated_at: datetime
}
```

---

## 🏗️ Architecture

### Service Layer Pattern
```
Pages (Streamlit)
    ↓
Services (Business Logic)
    ↓
Models (ORM)
    ↓
Database (SQLite)
```

### Key Modules

**`utils/calculations.py`** - Core business logic
- `AllocationValidator` - 100% capacity enforcement
- `HoursCalculator` - Allocation → hours conversion
- `CostCalculator` - Multi-level cost computation
- `ReportGenerator` - Executive alerts & summaries

**`utils/auth.py`** - Authentication
- User login/logout
- Role-based access control
- Session management

**`services/*`** - CRUD Operations
- Employee, Topic, Allocation, Cost management
- Export to CSV/Excel
- Import from CSV with validation

---

## 🔐 Security Features

✅ **Authentication**
- Secure login with username/password
- Role-based access control
- Session-based authentication

✅ **Data Integrity**
- 100% capacity rule prevents inconsistencies
- Validation on all imports
- Foreign key constraints

✅ **User Credentials**
- Stored in `data/users.json` (change defaults!)
- Passwords should be updated post-deployment
- Role assignments per user

---

## 📊 Usage Workflows

### Admin Workflow
```
1. Create Employees (via UI or bulk import)
   ↓
2. Create Topics/Projects
   ↓
3. Add external costs to topics
   ↓
4. Allocate employees (100% validated)
   ↓
5. Monitor Dashboard
   ↓
6. Export reports for review
   ↓
7. Make adjustments as needed
```

### Viewer Workflow
```
1. Login (read-only role)
   ↓
2. View Dashboard & metrics
   ↓
3. Access Reports page
   ↓
4. Download/analyze exported data
   ↓
5. Read executive summaries
```

---

## 🔄 Common Tasks

### Add 100 Employees in 1 Minute
```csv
# Save as employees.csv
Name,Location,Available Hours/Year,Hourly Rate
John Smith,GV CAE Bonn,1600,50.00
Jane Doe,GV Test Troy,1600,55.00
...
```
→ Go to Reports → Import → Upload → Done!

### Monitor Total Costs
```
1. Go to Dashboard
2. See top metrics (Total Cost, Headcount, Avg Cost)
3. Review cost distribution chart
4. Check high-cost project alerts
```

### Create Allocation (with Validation)
```
1. Go to Allocations
2. Select Employee
3. For each Topic, enter allocation %
4. System checks: sum must = 100%
5. If OK → Save / If not → Shows error
```

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Frontend | Streamlit | 1.32.0 |
| ORM | SQLModel | 0.0.14 |
| Database | SQLite | Built-in |
| Data | Pandas | 2.1.3 |
| Visualization | Plotly | 5.18.0 |
| Export | OpenPyXL | 3.11.0 |
| Language | Python | 3.8+ |

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **QUICKSTART.md** | 5-minute setup & common tasks |
| **DEPLOYMENT_GUIDE.md** | Installation, configuration, troubleshooting |
| **README.md** | This comprehensive guide |
| **Code comments** | Inline documentation in all modules |

---

## ⚡ Performance

- ✅ Handles 1000+ employees
- ✅ Supports 100+ projects
- ✅ Real-time validation
- ✅ Fast CSV import (bulk operations)
- ✅ Efficient cost calculations

---

## 🔧 Customization

### Change Capacity Rule
Edit `utils/calculations.py` → `AllocationValidator.validate_employee_allocation()`

### Add New Cost Type
1. Update allowed values in `CostItem`
2. Update cost calculation in `CostCalculator`
3. Update UI in `pages/3_Topics.py`

### Customize Colors
Edit CSS in `.markdown()` sections of pages

### Modify User Roles
Edit `data/users.json` and `utils/auth.py`

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | `pip install -r requirements.txt` |
| Port 8501 in use | `streamlit run login.py --server.port 8502` |
| Database locked | Close all windows, restart |
| Login fails | Check `data/users.json` for credentials |

---

## 📈 Future Enhancements

- [ ] Multi-user concurrent editing
- [ ] Advanced reporting (PDF exports)
- [ ] Historical tracking (audit trail)
- [ ] Integration with HR systems
- [ ] Mobile-friendly interface
- [ ] REST API for external integrations

---

## 📞 Support

For issues or questions:
1. Check `DEPLOYMENT_GUIDE.md` troubleshooting section
2. Review inline code comments
3. Verify database integrity: `data/planning.db`

---

## 📄 License

© 2026 Kautex GmbH. All rights reserved.

---

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [SQLModel Guide](https://sqlmodel.tiangolo.com/)
- [Plotly Charts](https://plotly.com/python/)

---

**Ready to deploy?** → Start with `QUICKSTART.md` →  Follow `DEPLOYMENT_GUIDE.md` → Begin using!

**v2.0** | Last Updated: July 8, 2026
