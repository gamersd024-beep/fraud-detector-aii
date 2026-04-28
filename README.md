---
title: Fraud Detector AI
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "4.44.1"
python_version: "3.10"
app_file: app.py
pinned: false
---

# 🚀 AI Document Fraud Detection

Compare two PDFs (or links) and detect mismatches in:

- Name
- Date of Birth (DOB)
- Income

---

## 🔧 How it works

1. Upload 2 PDFs OR paste public links  
2. System extracts text  
3. AI logic compares fields  
4. Generates risk score + decision  

---

## 📊 Output

- 🔍 Risk Score (0–100)
- ✅ Approved / ⚠️ Needs Review / ❌ Rejected
- 📌 Mismatch findings
- 📄 Extracted data

---

## ⚙️ Tech Stack

- Python
- Gradio
- PyPDF
- Regex-based extraction

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
python app.py
