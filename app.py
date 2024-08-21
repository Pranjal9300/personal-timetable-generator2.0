import streamlit as st
import pandas as pd
import json
import os
import re

PROFILE_FILE = 'user_profiles.json'

PREDEFINED_SUBJECTS = [
    "Innovation, Entrepreneurship and Start-ups (IES)",
    "Know yourself (KY)",
    "Professional Ethics (PE)",
    "Bibliophiles (Bibl)",
    "Psychology in Business (PB-A)",
    "International Business (IB)",
    "Project Management (PM)",
    "E-Business (E.Bus)",
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
]

def load_excel(file):
    return pd.read_excel(file, sheet_name=None)

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

def clean_cell_value(cell_value):
    cell_value = re.sub(r'\[.*?\]', '', cell_value)
    cell_value = re.sub(r'\(.*?\)', '', cell_value)
    cell_value = cell_value.replace('/', ' ').strip()
    return cell_value

def filter_and_blank_timetable_by_subjects(timetable, selected_subjects):
    for index, row in timetable.iterrows():
        for col in timetable.columns[1:]:
            cell_value = str(row[col]).strip()
            cleaned_value = clean_cell_value(cell_value)

            cell_subjects = cleaned_value.split()

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

def create_profile(user_id, name, enrollment_no, selected_subjects):
    profiles = load_profiles()
    profiles[user_id] = {
        "name": name,
        "enrollment_no": enrollment_no,
        "subjects": selected_subjects
    }
    save_profiles(profiles)

def update_profile(user_id, selected_subjects):
    profiles = load_profiles()
    if user_id in profiles:
        profiles[user_id]["subjects"] = selected_subjects
        save_profiles(profiles)

def main():
    st.title("Personal Timetable Generator")

    profiles = load_profiles()
    
    profile_option = st.sidebar.selectbox("Select an option", ["Create New Profile", "Select Existing Profile"], key="profile_option")

    if profile_option == "Create New Profile":
        st.subheader("Create New Profile")
        name = st.text_input("Enter your Name", key="name")
        enrollment_no = st.text_input("Enter your Enrollment Number", key="enrollment_no")
        
        if name and enrollment_no:
            st.sidebar.subheader("Select Subjects for Profile", key="subject_selection")
            selected_subjects = st.sidebar.multiselect(
                "Subjects", 
                PREDEFINED_SUBJECTS, 
                key="create_subjects"
            )
            
            if st.sidebar.button("Create Profile", key="create_profile_button"):
                user_id = f"{name}_{enrollment_no}"
                create_profile(user_id, name, enrollment_no, selected_subjects)
                st.sidebar.success("Profile created successfully! You can now upload your timetable.")
                st.session_state.user_id = user_id
        else:
            st.warning("Please enter both your name and enrollment number.")

    elif profile_option == "Select Existing Profile":
        st.subheader("Select Existing Profile")
        if profiles:
            user_ids = list(profiles.keys())
            user_id = st.selectbox("Select Your Profile", user_ids, key="existing_profile")
            
            if user_id:
                st.session_state.user_id = user_id
                st.sidebar.subheader("Profile Details")
                st.sidebar.write(f"Name: {profiles[user_id]['name']}")
                st.sidebar.write(f"Enrollment Number: {profiles[user_id]['enrollment_no']}")
                st.sidebar.subheader("Select Subjects to Update", key="update_subject_selection")
                selected_subjects = st.sidebar.multiselect(
                    "Subjects", 
                    PREDEFINED_SUBJECTS, 
                    default=profiles[user_id]['subjects'], 
                    key="update_subjects"
                )
                
                if st.sidebar.button("Update Profile", key="update_profile_button"):
                    update_profile(user_id, selected_subjects)
                    st.sidebar.success("Profile updated successfully!")
        else:
            st.warning("No profiles found. Create a new profile first.")

    if 'user_id' in st.session_state:
        uploaded_file = st.file_uploader("Upload your timetable Excel file", type=["xlsx"], key="file_uploader")

        if uploaded_file:
            sheets = load_excel(uploaded_file)
            timetable_sheet = sheets.get("MBA 2023-25_3RD SEMESTER")
            subjects_sheet = sheets.get("FACULTY DETAILS")

            if timetable_sheet is not None and subjects_sheet is not None:
                sections = ['A', 'B', 'C']
                selected_section = st.selectbox("Select your Section", sections, key="section_selection")

                if selected_section:
                    st.subheader("Select Your Subjects")
                    
                    subject_options = PREDEFINED_SUBJECTS
                    
                    profile = profiles[st.session_state.user_id]
                    selected_subjects = st.multiselect("Subjects", subject_options, default=profile['subjects'], key="filter_subjects")
                    
                    update_profile(st.session_state.user_id, selected_subjects)

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
