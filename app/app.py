import streamlit as st
import json
import numpy as np
import pandas as pd
from PIL import Image

from core.omr_detector import preprocess_image
from core.grader import grade_from_template
from utils.file_utils import load_answer_key

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="OMR Evaluator",
    layout="centered"
)

st.title("📄 AI OMR Evaluation System")
st.caption("Supports Excel / CSV / JSON answer keys | Template-based detection")

# ---------------- Sidebar ----------------
st.sidebar.header("Settings")
threshold = st.sidebar.slider(
    "Bubble Fill Threshold",
    min_value=0.20,
    max_value=0.60,
    value=0.35,
    step=0.05
)

# ---------------- Answer Key Upload ----------------
st.header("1️⃣ Upload Answer Key")

answer_file = st.file_uploader(
    "Upload Answer Key (Excel / CSV / JSON)",
    type=["xlsx", "xls", "csv", "json"]
)

answer_key = None
if answer_file:
    try:
        answer_key = load_answer_key(answer_file)
        st.success(f"✅ Loaded {len(answer_key)} answers successfully")
        st.write("Preview (first 10 answers):")
        st.json(dict(list(answer_key.items())[:10]))
    except Exception as e:
        st.error(f"❌ Failed to load answer key: {e}")

# ---------------- OMR Upload ----------------
st.header("2️⃣ Upload OMR Sheet")

omr_file = st.file_uploader(
    "Upload OMR Sheet Image (JPG / PNG)",
    type=["jpg", "jpeg", "png"]
)

# ---------------- Processing ----------------
if omr_file and answer_key:

    st.header("3️⃣ Evaluation Result")

    # Load image
    image = Image.open(omr_file).convert("RGB")
    img_np = np.array(image)

    st.subheader("Uploaded OMR Sheet")
    st.image(image, use_container_width=True)

    # Preprocess image
    _, thresh = preprocess_image(img_np)

    # Load template
    try:
        with open("app/templates/ugc_omr_template.json", "r") as f:
            template = json.load(f)
    except Exception:
        st.error("❌ OMR template file not found or invalid.")
        st.stop()

    # Grade
    results, score = grade_from_template(
        thresh=thresh,
        template=template,
        answer_key=answer_key,
        threshold=threshold
    )

    # Convert to DataFrame
    df = pd.DataFrame(results)

    st.success(f"🎯 Total Correct: {score} / {len(answer_key)}")

    st.subheader("Detailed Result")
    st.dataframe(df, use_container_width=True)

    # ---------------- Download Options ----------------
    st.subheader("📥 Download Results")

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="omr_result.csv",
        mime="text/csv"
    )

    json_data = json.dumps(results, indent=4).encode("utf-8")
    st.download_button(
        label="Download JSON",
        data=json_data,
        file_name="omr_result.json",
        mime="application/json"
    )

elif omr_file and not answer_key:
    st.warning("⚠️ Please upload an answer key first.")

else:
    st.info("⬆️ Upload an answer key and an OMR sheet to start evaluation.")

# ---------------- Footer ----------------
st.markdown("---")
st.caption(
    "🔍 Template-based OMR detection | Designed for school & exam-board use"
)
