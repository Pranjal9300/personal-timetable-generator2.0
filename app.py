import streamlit as st

# Dummy storage for profiles
profiles = {}

# Function to create a new profile
def create_profile(name, enrollment_no, section, subjects):
    if enrollment_no in profiles:
        st.error(f"Profile with Enrollment No: {enrollment_no} already exists.")
    else:
        profiles[enrollment_no] = {
            'name': name,
            'section': section,
            'subjects': subjects
        }
        st.success(f"Profile for {name} (Enrollment No: {enrollment_no}) has been created.")

# Function to update an existing profile
def update_profile(enrollment_no, section, subjects):
    if enrollment_no in profiles:
        profiles[enrollment_no]['section'] = section
        profiles[enrollment_no]['subjects'] = subjects
        st.success(f"Profile with Enrollment No: {enrollment_no} has been updated.")
    else:
        st.error("Profile not found.")

# Function to delete a profile
def delete_profile(enrollment_no):
    if enrollment_no in profiles:
        del profiles[enrollment_no]
        st.success(f"Profile with Enrollment No: {enrollment_no} has been deleted.")
    else:
        st.error("Profile not found.")

# Function to display all profiles
def display_all_profiles():
    if profiles:
        st.write("### Profiles:")
        for enrollment_no, profile in profiles.items():
            st.write(f"- {profile['name']} (Enrollment No: {enrollment_no})")
    else:
        st.error("No profiles found.")

# Function to display a specific profile
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
menu = st.sidebar.selectbox("Select Action", ["Create Profile", "Update Profile", "Delete Profile", "View Profiles"])

if menu == "Create Profile":
    st.header("Create Profile")
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
    
    selected_sector_subjects = sector_subjects[major_sector]
    selected_subjects = st.multiselect("Major Sector Subjects (Choose all)", selected_sector_subjects, selected_sector_subjects)
    
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
    
    if st.button("Create Profile"):
        create_profile(name, enrollment_no, section, subjects)

elif menu == "Update Profile":
    st.header("Update Profile")
    enrollment_no = st.text_input("Enter your enrollment number")
    if enrollment_no in profiles:
        section = st.selectbox("Select your section", ["A", "B", "C"], index=["A", "B", "C"].index(profiles[enrollment_no]['section']))
        
        st.subheader("Select Subjects")
        
        compulsory_subjects = ["Innovation, Entrepreneurship and Start-ups (IES)", "Know yourself (KY)", "Professional Ethics (PE)"]
        general_elective_1 = st.selectbox("General Electives 1 (Choose one)", ["Bibliophiles (Bibl)", "Psychology in Business (PB-A)"], 
                                          index=["Bibliophiles (Bibl)", "Psychology in Business (PB-A)"].index(profiles[enrollment_no]['subjects'][3]))
        general_elective_2 = st.selectbox("General Electives 2 (Choose one)", ["International Business (IB)", "Project Management (PM)", "E-Business (E.Bus)"], 
                                          index=["International Business (IB)", "Project Management (PM)", "E-Business (E.Bus)"].index(profiles[enrollment_no]['subjects'][4]))
        
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
        
        selected_sector_subjects = sector_subjects[major_sector]
        selected_subjects = st.multiselect("Major Sector Subjects (Choose all)", selected_sector_subjects, selected_sector_subjects)
        
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
        
        if st.button("Update Profile"):
            update_profile(enrollment_no, section, subjects)
    else:
        st.error("Profile not found. Please check the Enrollment Number.")

elif menu == "Delete Profile":
    st.header("Delete Profile")
    enrollment_no = st.text_input("Enter your enrollment number")
    if st.button("Delete Profile"):
        delete_profile(enrollment_no)

elif menu == "View Profiles":
    st.header("View Profiles")
    display_all_profiles()
