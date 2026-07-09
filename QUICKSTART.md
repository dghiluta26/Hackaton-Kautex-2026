# ⚡ Quick Start Guide - Kautex Resource Planning Tool

## 🚀 5-Minute Setup

### 1️⃣ Install & Run (2 minutes)

```bash
# Navigate to project
cd C:\Users\eduar\resource_planning_app

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run Login.py
```

Browser opens automatically at `http://localhost:8501`

### 2️⃣ Login (1 minute)

**Demo Credentials:**
- **Username:** `admin`
- **Password:** `admin123`

Click "Login" button → Dashboard loads

### 3️⃣ Create Your First Data (2 minutes)

**Step 1: Add Employee**
- Go to "Employees" page
- Click "Add Employee" tab
- Enter name, location, hourly rate
- Click "Add Employee"

**Step 2: Add Topic**
- Go to "Topics" page
- Click "Add Topic" tab
- Enter topic name, category, business justification
- Click "Add Topic"

**Step 3: Allocate**
- Go to "Allocations" page
- Select employee
- Add allocation to topic
- System validates 100% rule automatically
- Click "Save Allocation"

---

## 📊 Dashboard Overview

| Section | Purpose |
|---------|---------|
| **Top Metrics** | Total Cost, Headcount, Avg Cost/Employee |
| **Budget Distribution** | Stacked bar chart by project |
| **Budget Justification** | High-cost projects with alerts |
| **Employee Status** | Allocation % per employee |

---

## 🎯 Common Tasks

### Task: Import 10 Employees

1. Go to **Reports** → **Import Data**
2. Select **Employees**
3. Upload CSV with columns: Name, Location, Available Hours/Year, Hourly Rate
4. Click "Import Employees"
5. ✅ Done! Check Employees page

### Task: Export Cost Report

1. Go to **Reports** → **Export Data**
2. Click "Generate Cost Report (Excel)"
3. Download file: `cost_report.xlsx`
4. Open in Excel, see all costs by project

### Task: View High-Cost Projects

1. Go to **Dashboard**
2. Scroll to "Budget Justification & Alerts"
3. Click expander to see details
4. View cost breakdown and business justification

### Task: Check 100% Capacity

1. Go to **Allocations**
2. Look at "Allocation Matrix" tab
3. "Status" column shows:
   - ✅ = Fully allocated (100%)
   - ⚠️  = Unallocated (0-99%)
   - ❌ = Over/Under allocated

---

## 🔑 Key Features at a Glance

### 🔐 Authentication
- Secure login with role-based access
- Admin: Full CRUD operations
- Viewer: Read-only dashboard access

### 💰 Cost Tracking
- Internal personnel costs automatically calculated
- External tooling, testing, recovery costs
- Deep cost breakdown by topic

### 📊 Allocation Matrix
- Employee ↔ Topic mapping
- Real-time 100% validation
- Capacity indicators

### 📤 Data Management
- Export: CSV, Excel with formatting
- Import: Bulk upload employees, topics, allocations
- Reports: Cost analysis and executive summaries

---

## 🎨 User Interface

### Sidebar Navigation
```
🔐 User Info          → Shows current login
📍 Navigation         → Quick access to pages
🚪 Logout            → Sign out
```

### Main Pages
```
📊 Dashboard         → KPIs & cost overview
👥 Employees        → CRUD operations
📌 Topics           → Project management
🎯 Allocations      → Capacity planning
📤 Reports          → Export/Import
```

---

## ❓ FAQ

**Q: What happens if I try to save 90% allocation?**
A: System shows error: "Must allocate exactly 100%" and blocks save

**Q: Can I edit an employee's allocation?**
A: Yes! Go to Allocations → Single Employee → Edit existing allocation

**Q: How do I add external costs?**
A: Go to Topics → Manage Costs → Select topic → Add Cost Item

**Q: Can viewers export data?**
A: No, only Admins can export/import. Viewers see read-only Dashboard.

**Q: Where is my data stored?**
A: In `data/planning.db` (SQLite file)

**Q: How do I backup my data?**
A: Go to Reports → Export Data → Download all CSV files

---

## 🔄 Typical Workflow

```
1. Admin logs in
   ↓
2. Creates Employees (or bulk imports)
   ↓
3. Creates Topics/Projects
   ↓
4. Allocates employees to topics (100% rule)
   ↓
5. Adds external costs to topics
   ↓
6. Monitors Dashboard for cost metrics
   ↓
7. Exports reports for executive review
   ↓
8. Viewer logs in and sees Dashboard only
   ↓
9. Viewer downloads reports for analysis
```

---

## 🚨 Validation Rules

| Rule | Impact | Example |
|------|--------|---------|
| **100% Capacity** | Prevents over/under allocation | Can't save 95% + 10% = 105% |
| **Required Fields** | Blocks incomplete data | Name field required for employee |
| **Valid Percentages** | 0-100% range only | Can't enter -5% or 150% |
| **Unique Names** | Prevents duplicates | Can't create two "Project X" |

---

## 💡 Tips & Tricks

1. **Use Comments** - Add "Lead Developer" comment to document why allocation exists
2. **Bulk Import** - Use CSV import to quickly add 100+ employees
3. **Export Before Major Changes** - Backup data via Reports → Export
4. **Use Categories** - Organize projects by category (Customer, Internal, etc.)
5. **Monitor Dashboard Daily** - Check cost trends and capacity utilization

---

## 📞 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + L` | Open sidebar (Streamlit) |
| `Ctrl + S` | Save in forms (if enabled) |
| `Tab` | Navigate between fields |

---

## 🎓 Learning Path

**Day 1:** 
- Install & login
- Create 3 employees
- Create 2 topics
- Create allocations

**Day 2:**
- Explore Dashboard
- Add external costs
- Export cost report

**Day 3:**
- Invite viewer user
- Bulk import data
- Advanced allocations

---

## ✅ First-Run Checklist

- [ ] Application starts without errors
- [ ] Can login with admin credentials
- [ ] Dashboard displays "Healthy" status
- [ ] Can add an employee
- [ ] Can add a topic
- [ ] Can create an allocation
- [ ] 100% validation works (try saving 95%)
- [ ] Can export data
- [ ] Can logout and re-login

---

**Ready to go!** 🚀

Start with **Step 1** above and explore each page. All data is automatically saved.

For detailed docs, see `DEPLOYMENT_GUIDE.md`
