import streamlit as st
import pandas as pd
import json
import os
import re

PROFILE_FILE = 'user_profiles.json'

PREDEFINED_SUBJECTS = {
    "Innovation, Entrepreneurship and Start-ups (IES)",
    "Know yourself (KY)",
    "Professional Ethics (PE)",
    "General Electives 1 - Bibliophiles (Bibl)",
    "General Electives 1 - Psychology in Business (PB-A)",
    "General Electives 2 - International Business (IB)",
    "General Electives 2 - Project Management (PM)",
    "General Electives 2 - E-Business (E.Bus)",
    "Consumer Behaviour (CB)",
    "Integrated Marketing Communication (IMC)",
    "Sales & Distribution Management (S&DM)",
    "Marketing Analytics (Man)",
    "Strategic Brand Management (SBM)",
    "Financial Statement Analysis (FSA)",
    "Business Valuation (BussV)",
    "Security and Portfolio Management (SPM)",
    "International Finance (IF)",
    "Management of Banks (MoB)",
    "Programming for Analytics (PA)",
    "Text Mining and Sentiment Analytics (TM&SA)",
    "Data Mining and Visualization (DMV)",
    "Analytics for Service Operations (ASO)",
    "AI and Machine Learning (AIML)",
    "Digital Media (DM)",
    "Media Production and Consumption (MPC)",
    "Media and Sports Industry (MSI)",
    "Media Research Tools and Analytics (MRTA)",
    "Media Cost Management & Control (MCMC)",
    "Performance Management System (PMS)",
    "Talent Acquisition (TA)",
    "Learnings & Development (L&D)",
    "Compensation & Reward Management (C&RM)",
    "Purchasing & Inventory Management (P&IM)",
    "Supply Chain Management (SCM)",
    "Transportation & Distribution Management (TDM)",
    "Warehousing & Distribution Facilities Management (W&DFM)"
}

def load_excel(file):
    # Load the entire Excel file
    return pd.read_excel(file, sheet_name=None)

def get_section_timetable(timetable_sheet, section):
    # Define where each section starts based on the section name
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

def clean_cell_value(cell_value):
    # Remove text within brackets and split by '/'
    cell_value = re.sub(r'\[.*?\]', '', cell_value)  # Remove text within square brackets
    cell_value = re.sub(r'\(.*?\)', '', cell_value)  # Remove text within round brackets
    cell_value = cell_value.replace('/', ' ').strip()  # Replace '/' with space and strip
    return cell_value

def filter_and_blank_timetable_by_subjects(timetable, selected_subjects):
    for index, row in timetable.iterrows():
        for col in timetable.columns[1:]:  # Skip the first column (time slot)
            cell_value = str(row[col]).strip()
            cleaned_value = clean_cell_value(cell_value)

            # Split the cleaned cell value into abbreviations
            cell_subjects = cleaned_value.split()

            # If none of the selected subjects match the cell subjects, blank it out
            if not any(sub in cell_subjects for sub in selected_subjects):
                timetable.at[index, col] = ""

    return timetable

def load_profiles():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_profiles(profiles):
    with open(PROFILE_FILE, 'w') as f:
        json.dump(profiles, f)

def get_or_create_profile(user_id):
    profiles = load_profiles()
    if user_id not in profiles:
        profiles[user_id] = {"subjects": []}
        save_profiles(profiles)
    return profiles[user_id]

def update_profile(user_id, selected_subjects):
    profiles = load_profiles()
    profiles[user_id]["subjects"] = selected_subjects
    save_profiles(profiles)

def main():
    st.title("Personal Timetable Generator")

    # User identification (this could be a more robust system in a real app)
    user_id = st.text_input("Enter your User ID")

    if user_id:
        profile = get_or_create_profile(user_id)
        st.sidebar.subheader("Profile Management")
        
        if st.sidebar.button("Save Profile"):
            # Save selected subjects to profile
            selected_subjects = st.sidebar.multiselect("Select Subjects to Save", list(PREDEFINED_SUBJECTS), default=profile["subjects"])
            update_profile(user_id, selected_subjects)
            st.sidebar.success("Profile updated successfully!")

        uploaded_file = st.file_uploader("Upload your timetable Excel file", type=["xlsx"])

        if uploaded_file:
            sheets = load_excel(uploaded_file)
            timetable_sheet = sheets.get("MBA 2023-25_3RD SEMESTER")
            subjects_sheet = sheets.get("FACULTY DETAILS")

            if timetable_sheet is not None and subjects_sheet is not None:
                sections = ['A', 'B', 'C']
                selected_section = st.selectbox("Select your Section", sections)

                if selected_section:
                    st.subheader("Select Your Subjects")
                    
                    # Display predefined subjects for selection
                    subject_options = list(PREDEFINED_SUBJECTS)
                    
                    # Show the saved profile subjects and allow modifying them
                    selected_subjects = st.multiselect("Subjects", subject_options, default=profile["subjects"])
                    
                    # Update profile with selected subjects
                    update_profile(user_id, selected_subjects)

                    if selected_subjects:
                        selected_abbreviations = [sub.split('(')[-1].replace(')', '').strip() for sub in selected_subjects]

                        section_timetable = get_section_timetable(timetable_sheet, selected_section)

                        if section_timetable is not None:
                            personal_timetable = filter_and_blank_timetable_by_subjects(section_timetable, selected_abbreviations)
                            st.subheader("Your Personal Timetable")
                            st.dataframe(personal_timetable)
                        else:
                            st.error(f"Timetable for Section {selected_section} not found.")
                    else:
                        st.warning("Please select at least one subject.")
            else:
                st.error("The required sheets are not found in the uploaded file.")

if __name__ == "__main__":
    main()
