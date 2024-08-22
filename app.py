import streamlit as st
import pandas as pd
import re
from github import Github

# GitHub repository details
GITHUB_TOKEN = "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"
GITHUB_USERNAME = "Pranjal9300"
REPO_NAME = "personal-timetable-generator2.0"
PROFILE_FILENAME = "profiles.csv"

# Initialize GitHub object
g = Github(GITHUB_TOKEN)
repo = g.get_repo(f"{GITHUB_USERNAME}/{REPO_NAME}")

# Load or create profiles
def load_profiles():
    try:
        profiles_file = repo.get_contents(PROFILE_FILENAME)
        profiles = pd.read_csv(profiles_file.download_url)
    except:
        profiles = pd.DataFrame(columns=['Name', 'Enrollment No', 'Section', 'Subjects'])
    return profiles

def save_profiles(profiles):
    profiles_csv = profiles.to_csv(index=False)
    repo.update_file(PROFILE_FILENAME, "Updating profiles", profiles_csv, repo.get_contents(PROFILE_FILENAME).sha)

def create_profile(name, enrollment_no, section, subjects):
    profiles = load_profiles()
    if enrollment_no in profiles['Enrollment No'].values:
        st.error("A profile with this enrollment number already exists.")
    else:
        new_profile = pd.DataFrame({
            'Name': [name],
            'Enrollment No': [enrollment_no],
            'Section': [section],
            'Subjects': [', '.join(subjects)]
        })
        profiles = pd.concat([profiles, new_profile], ignore_index=True)
        save_profiles(profiles)
        st.success("Profile created successfully!")

def edit_profile(enrollment_no, section, subjects):
    profiles = load_profiles()
    if enrollment_no in profiles['Enrollment No'].values:
        profiles.loc[profiles['Enrollment No'] == enrollment_no, ['Section', 'Subjects']] = [section, ', '.join(subjects)]
        save_profiles(profiles)
        st.success("Profile updated successfully!")
    else:
        st.error("Profile not found.")

def delete_profile(enrollment_no):
    profiles = load_profiles()
    if enrollment_no in profiles['Enrollment No'].values:
        profiles = profiles[profiles['Enrollment No'] != enrollment_no]
        save_profiles(profiles)
        st.success("Profile deleted successfully!")
    else:
        st.error("Profile not found.")

# Rest of your Streamlit code
def main():
    st.title("Personal Timetable Generator")

    # Profile creation and management
    st.subheader("Manage Profiles")
    name = st.text_input("Name")
    enrollment_no = st.text_input("Enrollment Number")
    section = st.selectbox("Select your Section", ['A', 'B', 'C'])

    st.subheader("Select Your Subjects")
    compulsory_subjects = ["Innovation, Entrepreneurship and Start-ups (IES)", "Know yourself (KY)", "Professional Ethics (PE)"]
    general_electives_1 = st.selectbox("General Electives 1", ["Bibliophiles (Bibl)", "Psychology in Business (PB-A)"])
    general_electives_2 = st.selectbox("General Electives 2", ["International Business (IB)", "Project Management (PM)", "E-Business (E.Bus)"])

    major_sector_options = {
        "Sales and Marketing": ["Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)"],
        "Finance": ["Financial Statement Analysis (FSA)", "Business Valuation (BussV)", "Security and Portfolio Management (SPM)"],
        "Business Analytics and Operations": ["Programing for Analytics (PA)", "Data Mining and Visualization (DMV)", "AI and Machine Learning (AIML)"],
        "Media": ["Digital Media (DM)", "Media Production and Consumption (MPC)", "Media Research Tools and Analytics (MRTA)"],
        "HR": ["Performance Management System (PMS)", "Talent Acquisition (TA)", "Learnings & Development (L&D)"],
        "Logistics & Supply Chain": ["Purchasing & Inventory Management (P&IM)", "Supply Chain Management (SCM)", "Transportation & Distribution Management (TDM)"]
    }
    major_sector = st.selectbox("Choose Your Major Sector", list(major_sector_options.keys()))
    major_subjects = major_sector_options[major_sector]

    additional_subjects = st.selectbox("Choose any one additional subject", [
        "Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)",
        "Marketing Analytics (Man)", "Strategic Brand Management (SBM)", "Financial Statement Analysis (FSA)",
        "Business Valuation (BussV)", "Security and Portfolio Management (SPM)", "International Finance (IF)",
        "Management of Banks (MoB)", "Programming for Analytics (PA)", "Text Mining and Sentiment Analytics (TM&SA)",
        "Data Mining and Visualization (DMV)", "Analytics for Service Operations (ASO)", "AI and Machine Learning (AIML)",
        "Digital Media (DM)", "Media Production and Consumption (MPC)", "Media and Sports Industry (MSI)",
        "Media Research Tools and Analytics (MRTA)", "Media Cost Management & Control (MCMC)",
        "Performance Management System (PMS)", "Talent Acquisition (TA)", "Learnings & Development (L&D)",
        "Compensation & Reward Management (C&RM)", "Purchasing & Inventory Management (P&IM)",
        "Supply Chain Management (SCM)", "Transportation & Distribution Management (TDM)",
        "Warehousing & Distribution Facilities Management (W&DFM)"
    ])

    selected_subjects = compulsory_subjects + [general_electives_1, general_electives_2] + major_subjects + [additional_subjects]

    if st.button("Create Profile"):
        create_profile(name, enrollment_no, section, selected_subjects)

    if st.button("Edit Profile"):
        edit_profile(enrollment_no, section, selected_subjects)

    if st.button("Delete Profile"):
        delete_profile(enrollment_no)

    # Timetable generation using the enrolled subjects and section
    uploaded_file = st.file_uploader("Upload your timetable Excel file", type=["xlsx"])
    if uploaded_file and enrollment_no:
        profiles = load_profiles()
        user_profile = profiles[profiles['Enrollment No'] == enrollment_no].iloc[0]

        section = user_profile['Section']
        selected_subjects = user_profile['Subjects'].split(", ")

        sheets = pd.read_excel(uploaded_file, sheet_name=None)
        timetable_sheet = sheets.get("MBA 2023-25_3RD SEMESTER")

        if timetable_sheet is not None:
            section_timetable = get_section_timetable(timetable_sheet, section)
            personal_timetable = filter_and_blank_timetable_by_subjects(section_timetable, selected_subjects)
            st.subheader("Your Personal Timetable")
            st.dataframe(personal_timetable)
        else:
            st.error("The required sheet is not found in the uploaded file.")

if __name__ == "__main__":
    main()
