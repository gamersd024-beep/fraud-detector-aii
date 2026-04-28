import gradio as gr
import requests
from pypdf import PdfReader
import tempfile
import re
import os

# ---------- Extract Text ----------
def extract_text(source):
    try:
        # If URL
        if isinstance(source, str) and source.startswith("http"):
            r = requests.get(source, timeout=10)
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            temp.write(r.content)
            path = temp.name
        else:
            path = source

        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        return ""

# ---------- Extract Fields ----------
def extract_fields(text):
    name = re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+", text)
    dob = re.findall(r"\d{2}-\d{2}-\d{4}", text)
    income = re.findall(r"\d{4,}", text)

    return {
        "name": name[0] if name else "Not found",
        "dob": dob[0] if dob else "Not found",
        "income": income[0] if income else "Not found"
    }

# ---------- Compare Logic ----------
def compare(pdf1, pdf2, link1, link2):
    try:
        # Decide input sources
        source1 = link1.strip() if link1 else (pdf1.name if pdf1 else "")
        source2 = link2.strip() if link2 else (pdf2.name if pdf2 else "")

        if not source1 or not source2:
            return "❌ Please upload or provide BOTH PDFs"

        t1 = extract_text(source1)
        t2 = extract_text(source2)

        if not t1 or not t2:
            return "❌ Could not read one or both PDFs"

        d1 = extract_fields(t1)
        d2 = extract_fields(t2)

        score = 100
        issues = []

        # Name check
        if d1["name"] != d2["name"]:
            score -= 40
            issues.append("🔴 Name mismatch")

        # DOB check
        if d1["dob"] != d2["dob"]:
            score -= 30
            issues.append("⚠️ DOB mismatch")

        # Income check
        if d1["income"] != d2["income"]:
            score -= 20
            issues.append(f"⚠️ Income mismatch ({d1['income']} vs {d2['income']})")

        # Decision
        if score >= 80:
            decision = "✅ APPROVED"
        elif score >= 50:
            decision = "⚠️ NEEDS REVIEW"
        else:
            decision = "❌ REJECTED"

        return f"""
## 🔍 Risk Score: {score}/100  
{decision}

### Findings:
{chr(10).join(issues) if issues else "🟢 No major issues"}

### Extracted Data:
Doc1 → {d1}  
Doc2 → {d2}
"""

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ---------- UI ----------
with gr.Blocks() as app:
    gr.Markdown("# 🚀 AI Document Fraud Detection")

    gr.Markdown("Upload PDFs OR paste public links")

    pdf1 = gr.File(label="Upload PDF 1")
    pdf2 = gr.File(label="Upload PDF 2")

    link1 = gr.Textbox(label="PDF 1 Link (optional)")
    link2 = gr.Textbox(label="PDF 2 Link (optional)")

    btn = gr.Button("Check Fraud")
    output = gr.Markdown()

    btn.click(
        compare,
        inputs=[pdf1, pdf2, link1, link2],
        outputs=output
    )

# ---------- Launch (Render Safe) ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.launch(server_name="0.0.0.0", server_port=port)
