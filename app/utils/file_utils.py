import pandas as pd
import json
import io

def load_answer_key(uploaded_file):
    """
    Supported formats:
    - Excel (.xlsx, .xls) with columns: question | answer
    - CSV with columns: question | answer
    - JSON: { "1": "A", "2": "C" }
    """

    if uploaded_file is None:
        return {}

    filename = uploaded_file.name.lower()

    try:
        # ---------- EXCEL ----------
        if filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)

        # ---------- CSV ----------
        elif filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        # ---------- JSON ----------
        elif filename.endswith(".json"):
            data = json.load(uploaded_file)
            return {
                int(k): str(v).strip().upper()
                for k, v in data.items()
            }

        else:
            raise ValueError("Unsupported file format")

        # ---------- COMMON EXCEL / CSV HANDLING ----------
        required_cols = {"question", "answer"}
        if not required_cols.issubset(set(df.columns.str.lower())):
            raise ValueError("File must contain columns: question, answer")

        # Normalize column names
        df.columns = df.columns.str.lower()

        answer_key = {
            int(row["question"]): str(row["answer"]).strip().upper()
            for _, row in df.iterrows()
        }

        return answer_key

    except Exception as e:
        raise RuntimeError(f"Invalid answer key file: {e}")
