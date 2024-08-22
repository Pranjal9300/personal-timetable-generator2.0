import streamlit as st
import json
import os

# File to store profiles
PROFILE_FILE = 'profiles.json'

def load_profiles():
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, 'r') as file:
            profiles = json.load(file)
    else:
        profiles = {}
    return profiles

def save_profiles(profiles):
    with open(PROFILE_FILE, 'w') as file:
        json.dump(profiles, file)

def create_profile(name, enrollment_no, section, subjects):
    profiles = load_profiles()
    profiles[enrollment_no] = {
        'name': name,
        'section': section,
        'subjects': subjects
    }
    save_profiles(profiles)
    st.success(f"Profile created for {name} (Enrollment No: {enrollment_no})")

def update_profile(enrollment_no, section, subjects):
    profiles = load_profiles()
    if enrollment_no in profiles:
        profiles[enrollment_no]['section'] = section
        profiles[enrollment_no]['subjects'] = subjects
        save_profiles(profiles)
        st.success(f"Profile for {profiles[enrollment_no]['name']} (Enrollment No: {enrollment_no}) updated.")
    else:
        st.error(f"Profile with Enrollment No: {enrollment_no} not found.")

def delete_profile(enrollment_no):
    profiles = load_profiles()
    if enrollment_no in profiles:
        del profiles[enrollment_no]
        save_profiles(profiles)
        st.success(f"Profile with Enrollment No: {enrollment_no} deleted.")
    else:
        st.error(f"Profile with Enrollment No: {enrollment_no} not found.")

def display_all_profiles():
    profiles = load_profiles()
    if profiles:
        for enrollment_no, profile in profiles.items():
            st.write(f"**Name**: {profile['name']} | **Enrollment No**: {enrollment_no} | **Section**: {profile['section']} | **Subjects**: {', '.join(profile['subjects'])}")
    else:
        st.write("No profiles found.")

# Streamlit app logic
st.title("Student Profile Management")

menu = st.sidebar.selectbox("Menu", ["Create Profile", "Update Profile", "Delete Profile", "View Profiles"])

if menu == "Create Profile":
    st.header("Create Profile")
    name = st.text_input("Enter your name")
    enrollment_no = st.text_input("Enter your enrollment number")
    section = st.selectbox("Select your section", ["A", "B", "C"])
    
    # Subject selection
    compulsory_subjects = ["Innovation, Entrepreneurship and Start-ups (IES)", "Know yourself (KY)", "Professional Ethics (PE)"]
    
    general_elective_1 = st.selectbox("Select General Elective 1", ["Bibliophiles (Bibl)", "Psychology in Business (PB-A)"])
    general_elective_2 = st.selectbox("Select General Elective 2", ["International Business (IB)", "Project Management (PM)", "E-Business (E.Bus)"])
    
    major_sector = st.selectbox("Select Major Sector", [
        "Sales and Marketing", "Finance", "Business Analytics and Operations", "Media", "HR", "Logistics & Supply Chain"
    ])
    
    if major_sector == "Sales and Marketing":
        selected_subjects = ["Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)"]
    elif major_sector == "Finance":
        selected_subjects = ["Financial Statement Analysis (FSA)", "Business Valuation (BussV)", "Security and Portfolio Management (SPM)"]
    elif major_sector == "Business Analytics and Operations":
        selected_subjects = ["Programming for Analytics (PA)", "Data Mining and Visualization (DMV)", "AI and Machine Learning (AIML)"]
    elif major_sector == "Media":
        selected_subjects = ["Digital Media (DM)", "Media Production and Consumption (MPC)", "Media Research Tools and Analytics (MRTA)"]
    elif major_sector == "HR":
        selected_subjects = ["Performance Management System (PMS)", "Talent Acquisition (TA)", "Learnings & Development (L&D)"]
    elif major_sector == "Logistics & Supply Chain":
        selected_subjects = ["Purchasing & Inventory Management (P&IM)", "Supply Chain Management (SCM)", "Transportation & Distribution Management (TDM)"]
    
    additional_subject = st.selectbox("Select Additional Subject", [
        "Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)", "Marketing Analytics (Man)",
        "Strategic Brand Management (SBM)", "Financial Statement Analysis (FSA)", "Business Valuation (BussV)", "Security and Portfolio Management (SPM)",
        "International Finance (IF)", "Management of Banks (MoB)", "Programming for Analytics (PA)", "Text Mining and Sentiment Analytics (TM&SA)",
        "Data Mining and Visualization (DMV)", "Analytics for Service Operations (ASO)", "AI and Machine Learning (AIML)", "Digital Media (DM)",
        "Media Production and Consumption (MPC)", "Media and Sports Industry (MSI)", "Media Research Tools and Analytics (MRTA)",
        "Media Cost Management & Control (MCMC)", "Performance Management System (PMS)", "Talent Acquisition (TA)", "Learnings & Development (L&D)",
        "Compensation & Reward Management (C&RM)", "Purchasing & Inventory Management (P&IM)", "Supply Chain Management (SCM)",
        "Transportation & Distribution Management (TDM)", "Warehousing & Distribution Facilities Management (W&DFM)"
    ])
    
    # Combine all selected subjects
    subjects = compulsory_subjects + [general_elective_1, general_elective_2] + selected_subjects + [additional_subject]
    
    if st.button("Create Profile"):
        create_profile(name, enrollment_no, section, subjects)

elif menu == "Update Profile":
    st.header("Update Profile")
    enrollment_no = st.text_input("Enter your enrollment number")
    profiles = load_profiles()
    if enrollment_no in profiles:
        st.write(f"Name: {profiles[enrollment_no]['name']}")
        section = st.selectbox("Select your section", ["A", "B", "C"])
        
        # Subject selection (same as in "Create Profile")
        compulsory_subjects = ["Innovation, Entrepreneurship and Start-ups (IES)", "Know yourself (KY)", "Professional Ethics (PE)"]
        
        general_elective_1 = st.selectbox("Select General Elective 1", ["Bibliophiles (Bibl)", "Psychology in Business (PB-A)"])
        general_elective_2 = st.selectbox("Select General Elective 2", ["International Business (IB)", "Project Management (PM)", "E-Business (E.Bus)"])
        
        major_sector = st.selectbox("Select Major Sector", [
            "Sales and Marketing", "Finance", "Business Analytics and Operations", "Media", "HR", "Logistics & Supply Chain"
        ])
        
        if major_sector == "Sales and Marketing":
            selected_subjects = ["Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)"]
        elif major_sector == "Finance":
            selected_subjects = ["Financial Statement Analysis (FSA)", "Business Valuation (BussV)", "Security and Portfolio Management (SPM)"]
        elif major_sector == "Business Analytics and Operations":
            selected_subjects = ["Programming for Analytics (PA)", "Data Mining and Visualization (DMV)", "AI and Machine Learning (AIML)"]
        elif major_sector == "Media":
            selected_subjects = ["Digital Media (DM)", "Media Production and Consumption (MPC)", "Media Research Tools and Analytics (MRTA)"]
        elif major_sector == "HR":
            selected_subjects = ["Performance Management System (PMS)", "Talent Acquisition (TA)", "Learnings & Development (L&D)"]
        elif major_sector == "Logistics & Supply Chain":
            selected_subjects = ["Purchasing & Inventory Management (P&IM)", "Supply Chain Management (SCM)", "Transportation & Distribution Management (TDM)"]
        
        additional_subject = st.selectbox("Select Additional Subject", [
            "Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)", "Marketing Analytics (Man)",
            "Strategic Brand Management (SBM)", "Financial Statement Analysis (FSA)", "Business Valuation (BussV)", "Security and Portfolio Management (SPM)",
            "International Finance (IF)", "Management of Banks (MoB)", "Programming for Analytics (PA)", "Text Mining and Sentiment Analytics (TM&SA)",
            "Data Mining and Visualization (DMV)", "Analytics for Service Operations (ASO)", "AI and Machine Learning (AIML)", "Digital Media (DM)",
            "Media Production and Consumption (MPC)", "Media and Sports Industry (MSI)", "Media Research Tools and Analytics (MRTA)",
            "Media Cost Management & Control (MCMC)", "Performance Management System (PMS)", "Talent Acquisition (TA)", "Learnings & Development (L&D)",
            "Compensation & Reward Management (C&RM)", "Purchasing & Inventory Management (P&IM)", "Supply Chain Management (SCM)",
            "Transportation & Distribution Management (TDM)", "Warehousing & Distribution Facilities Management (W&DFM)"
        ])
        
        subjects = compulsory_subjects + [general_elective_1, general_elective_2] + selected_subjects + [additional_subject]
        
        if st.button("Update Profile"):
            update_profile(enrollment_no, section, subjects)
    else:
        st.error(f"No profile found with Enrollment No: {enrollment_no}")

elif menu == "Delete Profile":
    st.header("Delete Profile")
    enrollment_no = st.text_input("Enter your enrollment number")
    if st.button("Delete Profile"):
        delete_profile(enrollment_no)

elif menu == "View Profiles":
    st.header("View Profiles")
    display_all_profiles()
