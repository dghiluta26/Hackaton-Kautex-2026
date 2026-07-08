"""Topics page: manage topics/projects."""

import streamlit as st

st.set_page_config(page_title="Topics", layout="wide")

st.title("Topics")
st.caption("View and manage topics/projects, their objectives and deliverables.")

# --- Topic list placeholder ---
st.subheader("Topic List")
st.info("A table listing all topics will be displayed here.")
# TODO: fetch topics with topic_service.get_all_topics() and show with st.dataframe

st.divider()

# --- Add/Edit topic form placeholder ---
st.subheader("Add / Edit Topic")
st.info("A form to create or update a topic will be displayed here.")
# TODO: build a form using st.form with fields matching the Topic model
# TODO: call topic_service.create_topic() / update_topic() on submit

st.divider()

# --- Business justification placeholder ---
st.subheader("Business Justification")
st.info("Details on the business justification for the selected topic will be displayed here.")
# TODO: show topic.business_justification and related notes for the selected topic
