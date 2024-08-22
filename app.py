import streamlit as st

# Dummy storage for profiles
profiles = {}

# Function to create or update a profile
def create_or_update_profile(name, enrollment_no, section, subjects):
    profiles[enrollment_no] = {
        'name': name,
        'section': section,
        'subjects': subjects
    }
    st.success(f"Profile for {name} (Enrollment No: {enrollment_no}) has been saved.")

# Function to delete a profile
def delete_profile(enrollment_no):
    if enrollment_no in profiles:
        del profiles[enrollment_no]
        st.success(f"Profile with Enrollment No: {enrollment_no} has been deleted.")
    else:
        st.error("Profile not found.")

# Function to display a profile
def display_profile(enrollment_no):
    profile = profiles.get(enrollment_no)
    if profile:
        st.write(f"**Name:** {profile['name']}")
        st.write(f"**Section:** {profile['section']}")
        st.write("**Subjects:**")
        for subject in profile['subjects']:
            st.write(f"- {subject}")
    else:
        st.error("Profile not found.")

# UI for the app
st.title("Student Profile Management")

# Menu for actions
menu = st.sidebar.selectbox("Select Action", ["Create/Update Profile", "Delete Profile", "View Profile"])

if menu == "Create/Update Profile":
    st.header("Create or Update Profile")
    name = st.text_input("Enter your name")
    enrollment_no = st.text_input("Enter your enrollment number")
    section = st.selectbox("Select your section", ["A", "B", "C"])
    
    st.subheader("Select Subjects")
    
    compulsory_subjects = ["Innovation, Entrepreneurship and Start-ups (IES)", "Know yourself (KY)", "Professional Ethics (PE)"]
    general_elective_1 = st.selectbox("General Electives 1 (Choose one)", ["Bibliophiles (Bibl)", "Psychology in Business (PB-A)"])
    general_elective_2 = st.selectbox("General Electives 2 (Choose one)", ["International Business (IB)", "Project Management (PM)", "E-Business (E.Bus)"])
    
    major_sector = st.selectbox("Choose your Major Sector", [
        "Sales and Marketing",
        "Finance",
        "Business Analytics and Operations",
        "Media",
        "HR",
        "Logistics & Supply Chain"
    ])
    
    sector_subjects = {
        "Sales and Marketing": ["Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)"],
        "Finance": ["Financial Statement Analysis (FSA)", "Business Valuation (BussV)", "Security and Portfolio Management (SPM)"],
        "Business Analytics and Operations": ["Programing for Analytics (PA)", "Data Mining and Visualization (DMV)", "AI and Machine Learning (AIML)"],
        "Media": ["Digital Media (DM)", "Media Production and Consumption (MPC)", "Media Research Tools and Analytics (MRTA)"],
        "HR": ["Performance Management System (PMS)", "Talent Acquisition (TA)", "Learnings & Development (L&D)"],
        "Logistics & Supply Chain": ["Purchasing & Inventory Management (P&IM)", "Supply Chain Management (SCM)", "Transportation & Distribution Management (TDM)"]
    }
    
    chosen_sector_subjects = sector_subjects[major_sector]
    selected_subjects = st.multiselect("Major Sector Subjects (Choose all)", chosen_sector_subjects, chosen_sector_subjects)
    
    additional_subject = st.selectbox("Choose any one additional subject", [
        "Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)",
        "Marketing Analytics (Man)", "Strategic Brand Management (SBM)", "Financial Statement Analysis (FSA)",
        "Business Valuation (BussV)", "Security and Portfolio Management (SPM)", "International Finance (IF)",
        "Management of Banks (MoB)", "Programing for Analytics (PA)", "Text Mining and Sentiment Analytics (TM&SA)",
        "Data Mining and Visualization (DMV)", "Analytics for Service Operations (ASO)", "AI and Machine Learning (AIML)",
        "Digital Media (DM)", "Media Production and Consumption (MPC)", "Media and Sports Industry (MSI)",
        "Media Research Tools and Analytics (MRTA)", "Media Cost Management & Control (MCMC)",
        "Performance Management System (PMS)", "Talent Acquisition (TA)", "Learnings & Development (L&D)",
        "Compensation & Reward Management (C&RM)", "Purchasing & Inventory Management (P&IM)",
        "Supply Chain Management (SCM)", "Transportation & Distribution Management (TDM)",
        "Warehousing & Distribution Facilities Management (W&DFM)"
    ])
    
    # Combine all selected subjects
    subjects = compulsory_subjects + [general_elective_1, general_elective_2] + selected_subjects + [additional_subject]
    
    if st.button("Save Profile"):
        create_or_update_profile(name, enrollment_no, section, subjects)

elif menu == "Delete Profile":
    st.header("Delete Profile")
    enrollment_no = st.text_input("Enter the enrollment number of the profile to delete")
    if st.button("Delete Profile"):
        delete_profile(enrollment_no)

elif menu == "View Profile":
    st.header("View Profile")
    enrollment_no = st.text_input("Enter the enrollment number to view")
    if st.button("View Profile"):
        display_profile(enrollment_no)
