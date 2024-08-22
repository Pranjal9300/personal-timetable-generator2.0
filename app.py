# Import necessary libraries
import streamlit as st
import pandas as pd
import re

# Load the general timetable from an Excel file
def load_excel(file):
    return pd.read_excel(file, sheet_name=None)

# Get the section timetable from the general timetable
def get_section_timetable(timetable_sheet, section):
    section_start = {
        'A': 2,
        'B': 16,
        'C': 30
    }
    start_row = section_start.get(section)
    end_row = start_row + 12 if start_row is not None else None
    if start_row is not None and end_row is not None:
        section_timetable = timetable_sheet.iloc[start_row:end_row]
        return section_timetable
    else:
        return None

# Clean cell values by removing text within brackets and splitting by '/'
def clean_cell_value(cell_value):
    cell_value = re.sub(r'\[.*?\]', '', cell_value)
    cell_value = re.sub(r'\(.*?\)', '', cell_value)
    cell_value = cell_value.replace('/', ' ').strip()
    return cell_value

# Filter and blank out timetable cells based on selected subjects
def filter_and_blank_timetable_by_subjects(timetable, selected_subjects):
    for index, row in timetable.iterrows():
        for col in timetable.columns[1:]:
            cell_value = str(row[col]).strip()
            cleaned_value = clean_cell_value(cell_value)
            cell_subjects = cleaned_value.split()
            if not any(sub in cell_subjects for sub in selected_subjects):
                timetable.at[index, col] = ""
    return timetable

# Create a personal timetable based on user input
def create_personal_timetable(timetable_sheet, section, selected_subjects):
    section_timetable = get_section_timetable(timetable_sheet, section)
    if section_timetable is not None:
        personal_timetable = filter_and_blank_timetable_by_subjects(section_timetable, selected_subjects)
        return personal_timetable
    else:
        return None

# Streamlit app
st.title("Personal Timetable Generator")

# Upload the general timetable Excel file
uploaded_file = st.file_uploader("Upload your timetable Excel file", type=["xlsx"])

if uploaded_file:
    sheets = load_excel(uploaded_file)
    timetable_sheet = sheets.get("MBA 2023-25_3RD SEMESTER")

    if timetable_sheet is not None:
        # Get the user's section and selected subjects
        section = st.selectbox("Select your Section", ["A", "B", "C"])
        selected_subjects = st.multiselect("Select your subjects", [
            "Innovation, Entrepreneurship and Start-ups (IES)",
            "Know yourself (KY)",
            "Professional Ethics (PE)",
            # Add more subjects here
        ])

        # Create the personal timetable
        personal_timetable = create_personal_timetable(timetable_sheet, section, selected_subjects)

        if personal_timetable is not None:
            st.subheader("Your Personal Timetable")
            st.dataframe(personal_timetable)
        else:
            st.error(f"Timetable for Section {section} not found.")
    else:
        st.error("The required timetable sheet is not found in the uploaded file.")
