import streamlit as st
import pandas as pd
import re
import json
import os

PROFILE_FILE = 'profiles.json'

def load_profiles():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_profiles(profiles):
    with open(PROFILE_FILE, 'w') as f:
        json.dump(profiles, f, indent=4)

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

def main():
    st.title("Personal Timetable Generator")

    profiles = load_profiles()
    
    st.sidebar.header("User Profile Management")
    
    # Profile Creation and Management
    st.sidebar.subheader("Create or Select Profile")
    profile_name = st.sidebar.text_input("Profile Name")
    enrollment_no = st.sidebar.text_input("Enrollment Number")
    
    if st.sidebar.button("Save Profile"):
        if profile_name and enrollment_no:
            subjects = [
                "IES", "KY", "PE", "Bibl", "PB-A", "IB", "PM", "E.Bus", "CB",
                "IMC", "S&DM", "Man", "SBM", "FSA", "BussV", "SPM", "IF", "MoB",
                "PA", "TM&SA", "DMV", "ASO", "AIML", "DM", "MPC", "MSI", "MRTA",
                "MCMC", "PMS", "TA", "L&D", "C&RM", "P&IM", "SCM", "TDM", "W&DFM"
            ]
            selected_subjects = st.sidebar.multiselect("Select Subjects", subjects)

            profiles[profile_name] = {
                "enrollment_no": enrollment_no,
                "subjects": selected_subjects
            }
            save_profiles(profiles)
            st.sidebar.success(f"Profile '{profile_name}' saved successfully!")

    # Profile Selection
    st.sidebar.subheader("Select Existing Profile")
    profile_list = list(profiles.keys())
    selected_profile = st.sidebar.selectbox("Profiles", profile_list)
    
    if selected_profile:
        st.sidebar.text(f"Profile: {selected_profile}")
        enrollment_no = profiles[selected_profile]['enrollment_no']
        st.sidebar.text(f"Enrollment Number: {enrollment_no}")
        selected_subjects = profiles[selected_profile]['subjects']
        st.sidebar.text(f"Selected Subjects: {', '.join(selected_subjects)}")
        
        if st.sidebar.button("Delete Profile"):
            del profiles[selected_profile]
            save_profiles(profiles)
            st.sidebar.success(f"Profile '{selected_profile}' deleted successfully!")
    
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
                # Combine course title and abbreviation for selection
                subjects = subjects_sheet[['Cours Code', 'Course Title', 'Abbreviation']].drop_duplicates()
                
                # Replace abbreviations as required
                subjects['Abbreviation'] = subjects['Abbreviation'].replace({'PB': 'PB-A', 'MAn': 'Man'})
                
                subjects['Display'] = subjects['Course Title'] + " (" + subjects['Abbreviation'] + ")"
                subject_options = subjects['Display'].tolist()

                selected_subjects = st.multiselect("Subjects", subject_options)

                if selected_subjects:
                    # Extract just the abbreviations to filter the timetable
                    selected_abbreviations = [sub.split('(')[-1].replace(')', '').strip() for sub in selected_subjects]

                    # Get the timetable for the selected section
                    section_timetable = get_section_timetable(timetable_sheet, selected_section)

                    if section_timetable is not None:
                        # Filter the timetable cell-wise and blank out unselected subjects
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
