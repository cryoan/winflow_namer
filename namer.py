import streamlit as st
import re
from unidecode import unidecode

# --- Helper functions ---


def sanitize(text):
    # Convert accented characters to non-accented ones
    text = unidecode(text)
    text = text.lower().strip()
    text = re.sub(r'\s+', '_', text)
    text = re.sub(r'[^\w\d_+-]', '', text)  # keep alphanumerics, _, +, -
    return text


def build_filename(section, description, tags):
    section = sanitize(section)
    description = sanitize(description)
    tag_parts = [f"@{sanitize(k)}:{sanitize(v)}" for k,
                 v in tags.items() if k and v]
    tag_string = ''.join(tag_parts)

    # If there are no tags, use single underscore separator
    if tag_string:
        return f"{section}__{description}__{tag_string}.docx"
    else:
        return f"{section}__{description}.docx"

# --- UI ---


st.title("Winflow file naming buidler")

# Section dropdown
sections = ['contexte', 'presentation', 'methodologie',
            'consultants', 'references', 'annexes']
section = st.selectbox("Select section", sections)

# Description input
description = st.text_input("Enter short description")

# Dynamic tag input
st.markdown("### Add Tags")
num_tags = st.number_input(
    "Number of tags", min_value=0, max_value=10, step=1, value=1)
tags = {}

tag_keys = ['partenaire', 'team_structure',
            'secteur_activite', 'expertise']

for i in range(num_tags):
    cols = st.columns([1, 2])
    with cols[0]:
        key = st.selectbox(f"Tag key {i+1}", tag_keys, key=f"tag_key_{i}")
    with cols[1]:
        value = st.text_input(f"Tag value {i+1}", key=f"tag_value_{i}")
    tags[key] = value

# Generate filename
if section and description:
    filename = build_filename(section, description, tags)
    st.markdown("### Suggested File Name")
    st.code(filename)
else:
    st.info("Please provide both a section and a description.")
