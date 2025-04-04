import streamlit as st
import re
from unidecode import unidecode

# --- Helper functions ---


def sanitize(text):
    # Convert accented characters to non-accented ones
    text = unidecode(text)
    text = text.lower().strip()

    # Replace spaces with single underscore
    text = re.sub(r'\s+', '_', text)

    # Replace special characters with single underscore
    text = re.sub(r'[^\w\d_+-]', '_', text)

    # Replace multiple consecutive underscores with a single underscore
    text = re.sub(r'_+', '_', text)

    # Remove leading/trailing underscores
    text = text.strip('_')

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


st.title("Winflow file namer")

# Section dropdown
sections = ['contexte', 'presentation', 'methodologie',
            'consultants', 'references', 'annexes']
section = st.selectbox("Selectinner la section", sections)

# Description input
description = st.text_input("donner un nom court et informatif")

# Dynamic tag input
st.markdown("### Ajouter un ou plusieurs tags")
num_tags = st.number_input(
    "Nombre de tags", min_value=0, max_value=10, step=1, value=0)
tags = {}

tag_keys = ['partenaire', 'team_structure',
            'secteur_activite', 'expertise', "client", "date"]

for i in range(num_tags):
    cols = st.columns([1, 2])
    with cols[0]:
        key = st.selectbox(f"Tag key {i+1}", tag_keys, key=f"tag_key_{i}")
    with cols[1]:
        # Add help text for the first tag value
        if i == 0:
            value = st.text_input(
                f"Tag value {i+1}",
                key=f"tag_value_{i}",
                help="Par exemple auream ou auream+adaltys si valeurs multiples")
        else:
            value = st.text_input(
                f"Tag value {i+1}",
                key=f"tag_value_{i}")
    tags[key] = value

# Generate filename
if section and description:
    filename = build_filename(section, description, tags)
    st.markdown("### Nom du fichier suggéré")
    st.code(filename)
else:
    st.info("Veuillez fournir une section et une description.")
