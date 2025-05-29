# 🚀 Quick Start Guide - EIA Pro Platform

## 📋 **Prerequisites**
```bash
# Install required packages
pip install flask flask-cors
```

## 🌿 **Starting the Comprehensive Platform**

### **Option 1: Run Comprehensive Backend (Recommended)**
```bash
python backend_comprehensive.py
```
This runs the FULL platform with all 9 assessment modules integrated.

### **Option 2: Use the Launcher**
```bash
python run_comprehensive.py
```
This checks all requirements before starting.

### **Option 3: Run Basic Backend**
```bash
python backend_v1.py
```
This runs the basic version (air & noise only).

## 🌐 **Access the Platform**
1. Open your browser
2. Go to: `http://localhost:5000`
3. You'll see the comprehensive interface with all 9 modules

## 📊 **Using the Platform**

### **Step 1: Enter Project Information**
- Project Name (e.g., "Dubai Marina Tower")
- Project Type (Residential, Commercial, etc.)
- Location (e.g., "Dubai, UAE")
- Project Size in m²
- Other parameters as needed

### **Step 2: Run Assessment**
Click **"Run Comprehensive Assessment"** to analyze:
- ✅ Air Quality
- ✅ Noise Impact
- ✅ Water Resources
- ✅ Waste Management
- ✅ Biodiversity
- ✅ Soil & Geology
- ✅ Socio-Economic
- ✅ Risk Assessment
- ✅ Environmental Management Plan

### **Step 3: Review Results**
- Overall compliance score (0-100%)
- Individual module results
- Critical issues identified
- Mitigation recommendations

### **Step 4: Generate Report**
Click **"Generate Professional Report"** for:
- Comprehensive EIA document
- Regulatory compliance ready
- Professional formatting

## 🛠️ **Troubleshooting**

### **If modules fail to import:**
```bash
# Check if all files exist
ls src/assessment/

# Should see:
# - waste_management.py
# - water_resources.py
# - biological_environment.py
# - comprehensive_risk_assessment.py
# - socio_economic_environment.py
# - soil_geology.py
# - environmental_management_plan.py
```

### **If port 5000 is busy:**
```bash
# Kill existing process
lsof -ti:5000 | xargs kill -9

# Or use different port
python backend_comprehensive.py --port 5001
```

## 📧 **Support**
- Created by: Edy Bassil
- Email: bassileddy@gmail.com

---

**Platform Status:** ✅ READY FOR PROFESSIONAL USE