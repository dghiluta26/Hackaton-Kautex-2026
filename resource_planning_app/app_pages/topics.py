"""Topics page: manage topics/projects."""

import streamlit as st
import pandas as pd

from models.topic import Topic
from services.topic_service import create_topic, get_all_topics

st.title("Topics")
st.caption("View and manage topics/projects, their objectives and deliverables.")

# --- 1. Display Current Topics ---
st.subheader("Topic List")
all_topics = get_all_topics()

if len(all_topics) > 0:
    st.dataframe([topic.model_dump() for topic in all_topics], hide_index=True)
else:
    st.info("No topics found. Please upload a CSV below.")

st.divider()

# --- 2. The CSV Uploader ---
st.subheader("Mass Import Topics (CSV)")
st.caption("Required columns: name, category, area, status")

uploaded_file = st.file_uploader("Upload CSV", type="csv", key="topic_uploader")

if uploaded_file is not None:
    # Smart delimiter detection (Comma vs Semicolon) and BOM handling
    sample = uploaded_file.read(1024).decode("utf-8-sig", errors="ignore")
    uploaded_file.seek(0)
    separator = ";" if ";" in sample.split("\n")[0] else ","

    df = pd.read_csv(uploaded_file, sep=separator, encoding="utf-8-sig")
    df.columns = [str(col).strip().lower() for col in df.columns]

    st.write(f"Preview (Detected separator: '{separator}'):")
    st.dataframe(df.head(), hide_index=True)

    if st.button("Import to Database", type="primary"):
        success_count = 0
        skipped_count = 0

        for index, row in df.iterrows():
            # Skip blank rows
            if pd.isna(row.get("name")) or str(row.get("name")).strip() == "":
                skipped_count += 1
                continue

            new_topic = Topic(
                name=str(row["name"]).strip(),
                category=str(row.get("category", "Unmapped")),
                area=str(row.get("area", "")),
                status=str(row.get("status", "Active"))
            )
            create_topic(new_topic)
            success_count += 1

        st.success(f"Successfully imported {success_count} topics! (Skipped {skipped_count} invalid rows)")
        st.rerun()