import streamlit as st
import pandas as pd
import json
import os

PROFILE_FILE = 'profiles.json'

# Load profiles from file
def load_profiles():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save profiles to file
def save_profiles(profiles):
    with open(PROFILE_FILE, 'w') as f:
        json.dump(profiles, f, indent=4)

# Load Excel sheets
def load_excel(file):
    return pd.read_excel(file, sheet_name=None)

# Extract section timetable
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

# Clean cell values for comparison
def clean_cell_value(cell_value):
    cell_value = re.sub(r'\[.*?\]', '', cell_value)  # Remove text within square brackets
    cell_value = re.sub(r'\(.*?\)', '', cell_value)  # Remove text within round brackets
    cell_value = cell_value.replace('/', ' ').strip()  # Replace '/' with space and strip
    return cell_value

# Filter timetable by selected subjects
def filter_and_blank_timetable_by_subjects(timetable, selected_subjects):
    for index, row in timetable.iterrows():
        for col in timetable.columns[1:]:  # Skip the first column (time slot)
            cell_value = str(row[col]).strip()
            cleaned_value = clean_cell_value(cell_value)
            cell_subjects = cleaned_value.split()

            if not any(sub in cell_subjects for sub in selected_subjects):
                timetable.at[index, col] = ""

    return timetable

def main():
    st.title("Personal Timetable Generator")

    profiles = load_profiles()
    
    st.sidebar.header("User Profile Management")
    
    # Profile Creation and Management
    st.sidebar.subheader("Create or Edit Profile")
    profile_name = st.sidebar.text_input("Profile Name")
    enrollment_no = st.sidebar.text_input("Enrollment Number")
    
    # Define subjects with both names and abbreviations
    subjects = [
        {"name": "Innovation, Entrepreneurship and Start-ups", "abbreviation": "IES"},
        {"name": "Know yourself", "abbreviation": "KY"},
        {"name": "Professional Ethics", "abbreviation": "PE"},
        {"name": "Bibliophiles", "abbreviation": "Bibl"},
        {"name": "Psychology in Business", "abbreviation": "PB-A"},
        {"name": "International Business", "abbreviation": "IB"},
        {"name": "Project Management", "abbreviation": "PM"},
        {"name": "E-Business", "abbreviation": "E.Bus"},
        {"name": "Consumer Behaviour", "abbreviation": "CB"},
        {"name": "Integrated Marketing Communication", "abbreviation": "IMC"},
        {"name": "Sales & Distribution Management", "abbreviation": "S&DM"},
        {"name": "Marketing Analytics", "abbreviation": "Man"},
        {"name": "Strategic Brand Management", "abbreviation": "SBM"},
        {"name": "Financial Statement Analysis", "abbreviation": "FSA"},
        {"name": "Business Valuation", "abbreviation": "BussV"},
        {"name": "Security and Portfolio Management", "abbreviation": "SPM"},
        {"name": "International Finance", "abbreviation": "IF"},
        {"name": "Management of Banks", "abbreviation": "MoB"},
        {"name": "Programming for Analytics", "abbreviation": "PA"},
        {"name": "Text Mining and Sentiment Analytics", "abbreviation": "TM&SA"},
        {"name": "Data Mining and Visualization", "abbreviation": "DMV"},
        {"name": "Analytics for Service Operations", "abbreviation": "ASO"},
        {"name": "AI and Machine Learning", "abbreviation": "AIML"},
        {"name": "Digital Media", "abbreviation": "DM"},
        {"name": "Media Production and Consumption", "abbreviation": "MPC"},
        {"name": "Media and Sports Industry", "abbreviation": "MSI"},
        {"name": "Media Research Tools and Analytics", "abbreviation": "MRTA"},
        {"name": "Media Cost Management & Control", "abbreviation": "MCMC"},
        {"name": "Performance Management System", "abbreviation": "PMS"},
        {"name": "Talent Acquisition", "abbreviation": "TA"},
        {"name": "Learnings & Development", "abbreviation": "L&D"},
        {"name": "Compensation & Reward Management", "abbreviation": "C&RM"},
        {"name": "Purchasing & Inventory Management", "abbreviation": "P&IM"},
        {"name": "Supply Chain Management", "abbreviation": "SCM"},
        {"name": "Transportation & Distribution Management", "abbreviation": "TDM"},
        {"name": "Warehousing & Distribution Facilities Management", "abbreviation": "W&DFM"}
    ]
    
    subject_df = pd.DataFrame(subjects)
    subject_df['Display'] = subject_df['name'] + " (" + subject_df['abbreviation'] + ")"
    subject_options = subject_df['Display'].tolist()

    # Profile Creation or Editing
    if st.sidebar.button("Save Profile"):
        if profile_name and enrollment_no:
            selected_subjects_display = st.sidebar.multiselect(
                "Select Subjects (up to 9)", 
                subject_options, 
                max_selections=9
            )

            selected_subjects_abbr = [sub.split('(')[-1].replace(')', '').strip() for sub in selected_subjects_display]
            profiles[profile_name] = {
                "enrollment_no": enrollment_no,
                "subjects": selected_subjects_display
            }
            save_profiles(profiles)
            st.sidebar.success(f"Profile '{profile_name}' saved successfully!")

    # Profile Selection and Edit
    st.sidebar.subheader("Select Existing Profile")
    profile_list = list(profiles.keys())
    selected_profile = st.sidebar.selectbox("Profiles", profile_list)

    if selected_profile:
        st.sidebar.text(f"Profile: {selected_profile}")
        enrollment_no = profiles[selected_profile]['enrollment_no']
        selected_subjects_display = profiles[selected_profile]['subjects']
        st.sidebar.text(f"Enrollment
