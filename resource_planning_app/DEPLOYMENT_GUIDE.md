# 🚀 Kautex Resource & Cost Planning Tool - Deployment Guide

## 📦 Project Overview

A professional web-based resource planning and cost management tool built with Streamlit, SQLModel, and Plotly for executive leadership teams.

### ✨ Key Features

- ✅ **Secure Login System** - Role-based authentication (Admin & Viewer)
- ✅ **100% Capacity Enforcement** - Strict allocation validation
- ✅ **Deep Cost Analysis** - Multi-level cost breakdowns
- ✅ **Executive Dashboard** - Real-time metrics and alerts
- ✅ **Data Export** - CSV & Excel with formatting
- ✅ **Bulk Import** - Upload employees, topics, allocations
- ✅ **Professional Design** - Modern UI with Kautex branding

---

## 📋 System Requirements

- Python 3.8+
- pip (Python package manager)
- ~500MB disk space for dependencies
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## 🛠️ Installation Steps

### Step 1: Extract Project Files

```bash
cd C:\Users\eduar\resource_planning_app
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit==1.32.0` - Web framework
- `sqlmodel==0.0.14` - ORM for database
- `sqlalchemy==2.0.23` - Database toolkit
- `pandas==2.1.3` - Data analysis
- `plotly==5.18.0` - Interactive charts
- `openpyxl==3.11.0` - Excel export
- `xlsxwriter==3.1.2` - Excel formatting
- `PyPDF2==3.0.1` - PDF generation (future use)
- `pillow==10.1.0` - Image processing

### Step 4: Run the Application

```bash
streamlit run login.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 🔐 Default Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Full CRUD access

### Viewer Account
- **Username:** `viewer`
- **Password:** `viewer123`
- **Role:** Read-only access to reports

---

## 📁 Project Structure

```
resource_planning_app/
├── login.py                    # Login page (entry point)
├── app.py                      # Main dashboard
├── requirements.txt            # Python dependencies
├── assets/
│   └── kautex_logo.png        # Kautex branding
├── data/
│   ├── planning.db            # SQLite database (auto-created)
│   └── users.json             # User credentials
├── database/
│   ├── connection.py          # Database connection
│   └── init_db.py             # Database initialization
├── models/
│   ├── employee.py            # Employee ORM model
│   ├── topic.py               # Topic/Project ORM model
│   ├── allocation.py          # Allocation ORM model
│   └── cost_item.py           # Cost item ORM model
├── services/
│   ├── employee_service.py    # Employee CRUD
│   ├── topic_service.py       # Topic CRUD
│   ├── allocation_service.py  # Allocation CRUD
│   ├── cost_service.py        # Cost item CRUD
│   ├── export_service.py      # Data export (CSV, Excel)
│   └── import_service.py      # Bulk data import
├── pages/
│   ├── 1_Dashboard.py         # Executive dashboard
│   ├── 2_Employees.py         # Employee management
│   ├── 3_Topics.py            # Project management
│   ├── 4_Allocations.py       # Allocation matrix
│   └── 5_Reports.py           # Export/Import reports
└── utils/
    ├── calculations.py        # Business logic & validation
    └── auth.py                # Authentication system
```

---

## 💼 User Workflows

### Admin Workflow

1. **Login** with admin credentials
2. **Create Employees** → Go to Employees page, enter details
3. **Create Topics** → Go to Topics page, add projects
4. **Add Cost Items** → Attach external costs to topics
5. **Allocate Resources** → Go to Allocations page
   - Select employee and topics
   - Enter allocation % (must total 100%)
   - System validates allocation
6. **Monitor Dashboard** → Track costs and headcount
7. **Export Data** → Go to Reports page
   - Download cost reports (Excel)
   - Export allocation matrix
   - Bulk export for analysis
8. **Import Data** → Upload CSV files for bulk operations

### Viewer Workflow

1. **Login** with viewer credentials
2. **View Dashboard** → See KPIs and cost distribution
3. **Review Reports** → Access read-only views
4. **Download Data** → Export reports for external analysis
5. No edit/delete permissions

---

## 🎯 Business Logic

### 100% Capacity Rule

- Every employee must have exactly 100% allocation across all topics
- System prevents saving if allocation ≠ 100%
- Real-time validation with capacity indicators

### Cost Calculation

```
Internal Personnel Cost = Allocated Hours × Hourly Rate
Allocated Hours = Available Hours/Year × Allocation %

Topic Total Cost = 
  + Internal Personnel Cost
  + External Tooling Cost
  + Testing Cost
  - Recovery (negative)

Global Total = Sum of all Topic Costs
```

### High-Cost Flags

Topics with >30% external costs are flagged with:
- Business justification display
- External cost ratio
- Cost breakdown

---

## 📊 Data Management

### Export Formats

**CSV Export:**
- Employees.csv
- Topics.csv
- Allocations.csv

**Excel Export:**
- Cost_Report.xlsx (Multi-sheet with formatting)
- Allocation_Matrix.xlsx (Heatmap-style matrix)

### Import Templates

**Employees CSV:**
```
Name,Location,Available Hours/Year,Hourly Rate
John Smith,GV CAE Bonn,1600,50.00
Jane Doe,GV Test Troy,1600,55.00
```

**Topics CSV:**
```
Name,Category,Business Justification
Project X,Customer Request,This project delivers value for client ABC
Internal Framework,Internal Efforts,Core development work
```

**Allocations CSV:**
```
Employee Name,Topic Name,Allocation %,Comment
John Smith,Project X,60%,Lead Developer
John Smith,Internal Framework,40%,Framework maintenance
```

---

## 🔍 Troubleshooting

### Issue: "Python was not found"
**Solution:** Ensure Python is installed and added to PATH
```bash
python --version
```

### Issue: Module not found errors
**Solution:** Reinstall dependencies
```bash
pip install -r requirements.txt
```

### Issue: Database locked
**Solution:** Close all Streamlit windows and restart
```bash
# Kill all Python processes
taskkill /F /IM python.exe
```

### Issue: Port 8501 already in use
**Solution:** Specify different port
```bash
streamlit run login.py --server.port 8502
```

---

## 🔐 Security Notes

1. **Change Default Passwords:** Edit `data/users.json` after first run
2. **Database Backup:** Backup `data/planning.db` regularly
3. **User Management:** Add/remove users in `data/users.json`
4. **Environment Variables:** Consider using `.env` for sensitive data

---

## 📈 Performance Tips

1. **Optimize Data:** Archive old projects to improve dashboard speed
2. **Regular Exports:** Export data regularly for backup
3. **User Roles:** Use viewer role for read-only stakeholders
4. **Database Maintenance:** Periodically clean up old allocations

---

## 🚀 Deployment Options

### Local Deployment (Current Setup)
```bash
streamlit run login.py
```

### Docker Deployment
Create `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "login.py"]
```

Build and run:
```bash
docker build -t kautex-planning .
docker run -p 8501:8501 kautex-planning
```

### Cloud Deployment (Streamlit Cloud)
1. Push to GitHub
2. Deploy via [streamlit.io/cloud](https://streamlit.io/cloud)

---

## 📞 Support & Documentation

### Key Files to Review

- `README.md` - Project structure overview
- `utils/calculations.py` - Business logic documentation
- `utils/auth.py` - Authentication system
- Page-specific comments in `pages/` folder

### Common Customizations

1. **Add New Cost Type:**
   - Edit `CostItem.cost_type` enum in `models/cost_item.py`
   - Update cost calculations in `utils/calculations.py`

2. **Change Capacity Rule:**
   - Modify `AllocationValidator.validate_employee_allocation()` in `utils/calculations.py`

3. **Customize Colors:**
   - Update CSS in page `.markdown()` sections
   - Modify logo/branding in `assets/`

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Database created (`data/planning.db` exists)
- [ ] Logo asset exists (`assets/kautex_logo.png`)
- [ ] Can login with default credentials
- [ ] Dashboard displays metrics
- [ ] Can create employees
- [ ] Can create topics
- [ ] Can allocate resources
- [ ] 100% validation works

---

## 🎯 Next Steps

1. **Customize Users:** Update `data/users.json` with real credentials
2. **Add Real Data:** Use Import feature or Employees/Topics pages
3. **Configure Allocations:** Build the allocation matrix
4. **Review Dashboard:** Monitor costs and headcount
5. **Set Up Backups:** Regular exports to external storage

---

**Version:** 2.0  
**Last Updated:** July 8, 2026  
**Support:** Kautex Resource Planning Tool Team
