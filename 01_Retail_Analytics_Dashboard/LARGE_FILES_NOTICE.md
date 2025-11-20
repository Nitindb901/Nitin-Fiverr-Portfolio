# 📦 Large Files Notice

## ⚠️ GitHub File Size Limitations

GitHub has a **100MB file size limit** per file. This project contains two large CSV files that exceed this limit:

- `data/retail_transactions_clean.csv` (~138 MB)
- `dashboard/powerbi_ready.csv` (~133 MB)

These files are **excluded from Git** via `.gitignore` to prevent push errors.

---

## ✅ Solutions

### Option 1: Generate Files Locally (Recommended)

**All large files can be regenerated from scratch using the included scripts:**

```powershell
# Navigate to project folder
cd 01_Retail_Analytics_Dashboard

# Install dependencies
pip install -r requirements.txt

# Generate data (creates raw CSV)
python scripts/generate_data.py

# Clean and process (creates clean CSV)
python scripts/etl_clean.py

# Export dashboard files (creates powerbi_ready.csv)
python scripts/export_for_dashboard.py
```

**Time**: ~2-3 minutes total  
**Result**: All large files recreated exactly as in the original project

---

### Option 2: Download from Cloud Storage

Large files are available for download:

**Google Drive**: [Download Large Files](https://drive.google.com/drive/folders/YOUR_FOLDER_ID)  
**Dropbox**: [Download Large Files](https://www.dropbox.com/YOUR_LINK)

*Note: Update these links with your actual cloud storage URLs*

---

### Option 3: Use Git LFS (Advanced)

If you want to include large files in Git, use **Git Large File Storage (LFS)**:

```powershell
# Install Git LFS
# Download from: https://git-lfs.github.com/

# Initialize Git LFS in your repository
git lfs install

# Track large CSV files
git lfs track "*.csv"

# Add the .gitattributes file
git add .gitattributes

# Now add and commit large files
git add data/retail_transactions_clean.csv
git add dashboard/powerbi_ready.csv
git commit -m "Add large data files with Git LFS"
git push
```

**Pros**: Files are in GitHub  
**Cons**: Requires Git LFS setup, counts against LFS storage quota

---

## 📁 What's Included in GitHub

### Included Files (Under 100MB):
✅ All Python scripts (`scripts/*.py`)  
✅ Jupyter notebook (`notebooks/*.ipynb`)  
✅ All visualizations (`results/*.png`)  
✅ Smaller CSV files:
  - `dashboard/daily_aggregation.csv` (~200 KB)
  - `dashboard/category_aggregation.csv` (~2 KB)
  - `dashboard/store_performance.csv` (~1 KB)
  - `dashboard/monthly_trend.csv` (~2 KB)
  - `results/kpi_summary.csv` (~5 KB)
  - `results/category_summary.csv` (~3 KB)
  - `results/top_skus.csv` (~2 KB)
  - `results/top_brands.csv` (~2 KB)

✅ Complete documentation  
✅ Requirements file  
✅ Dashboard guides

### Excluded Files (Over 100MB):
❌ `data/retail_transactions_raw.csv` (~149 MB)  
❌ `data/retail_transactions_clean.csv` (~138 MB)  
❌ `dashboard/powerbi_ready.csv` (~133 MB)

---

## 🎯 For Portfolio Reviewers

**To run this project and see all files:**

1. Clone the repository
2. Run the three Python scripts (as shown in Option 1)
3. All large files will be generated in 2-3 minutes

**Why this approach?**
- ✅ Demonstrates code reproducibility
- ✅ Shows data pipeline execution
- ✅ Avoids GitHub file size limits
- ✅ Allows anyone to recreate the exact dataset

---

## 🔧 Troubleshooting

### "File too large" error during git push?

```powershell
# Verify large files are in .gitignore
cat .gitignore | Select-String "csv"

# Remove large files from staging if accidentally added
git rm --cached data/retail_transactions_clean.csv
git rm --cached dashboard/powerbi_ready.csv

# Commit the removal
git commit -m "Remove large files from tracking"

# Push again
git push
```

### Need to share large files with someone?

**Quick Share Options:**
1. **WeTransfer**: https://wetransfer.com/ (free, up to 2GB)
2. **Google Drive**: Upload and share link
3. **Dropbox**: Upload and create public link
4. **OneDrive**: Already in your OneDrive, just share the folder

---

## 📊 File Size Summary

| File | Size | Status | Solution |
|------|------|--------|----------|
| retail_transactions_raw.csv | 149 MB | ❌ Excluded | Run scripts |
| retail_transactions_clean.csv | 138 MB | ❌ Excluded | Run scripts |
| powerbi_ready.csv | 133 MB | ❌ Excluded | Run scripts |
| daily_aggregation.csv | 200 KB | ✅ Included | In repo |
| All visualizations (10 files) | ~15 MB | ✅ Included | In repo |
| All documentation | ~500 KB | ✅ Included | In repo |
| Python scripts | ~50 KB | ✅ Included | In repo |
| Jupyter notebook | ~1 MB | ✅ Included | In repo |

---

## 💡 Best Practices

### For Portfolio Projects:

1. **Always include scripts** to generate large files ✅
2. **Document the generation process** clearly ✅
3. **Provide cloud storage links** if needed ✅
4. **Use sample data** for demonstrations (optional)
5. **Keep visualizations** in the repo (usually small) ✅

### This Project Follows All Best Practices! 🎉

---

## 🚀 Quick Start for Recruiters/Reviewers

```powershell
# 1. Clone the repo
git clone https://github.com/nitindb901/Nitin-Fiverr-Portfolio.git
cd Nitin-Fiverr-Portfolio/01_Retail_Analytics_Dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate all files (2-3 minutes)
python scripts/generate_data.py
python scripts/etl_clean.py
python scripts/export_for_dashboard.py

# 4. Explore!
# - Open Jupyter notebook for analysis
# - Check results/ folder for visualizations
# - Use dashboard/ files in Power BI or Excel
```

---

## ✅ Checklist for Portfolio Publishing

- [x] All scripts included and documented
- [x] Requirements.txt with dependencies
- [x] README with clear instructions
- [x] .gitignore properly configured
- [x] Large files excluded from Git
- [x] Generation process documented
- [x] Visualizations included (small files)
- [x] Documentation complete
- [x] This LARGE_FILES_NOTICE.md created

---

**Your portfolio is professional and follows industry best practices!** 🎉

For questions, contact: nitindb901@gmail.com
