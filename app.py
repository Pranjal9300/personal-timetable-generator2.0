import streamlit as st
import pandas as pd

# Predefined subjects
compulsory_subjects = ["Innovation, Entrepreneurship and Start-ups (IES)", "Know yourself (KY)", "Professional Ethics (PE)"]
general_electives_1 = ["Bibliophiles (Bibl)", "Psychology in Business (PB-A)"]
general_electives_2 = ["International Business (IB)", "Project Management (PM)", "E-Business (E.Bus)"]
major_sectors = {
    "Sales and Marketing": ["Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)"],
    "Finance": ["Financial Statement Analysis (FSA)", "Business Valuation (BussV)", "Security and Portfolio Management (SPM)"],
    "Business Analytics and Operations": ["Programing for Analytics (PA)", "Data Mining and Visualization (DMV)", "AI and Machine Learning (AIML)"],
    "Media": ["Digital Media (DM)", "Media Production and Consumption (MPC)", "Media Research Tools and Analytics (MRTA)"],
    "HR": ["Performance Management System (PMS)", "Talent Acquisition (TA)", "Learnings & Development (L&D)"],
    "Logistics & Supply Chain": ["Purchasing & Inventory Management (P&IM)", "Supply Chain Management (SCM)", "Transportation & Distribution Management (TDM)"]
}
additional_subjects = [
    "Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)",
    "Maketing Analytics (Man)", "Strategic Brand Management (SBM)", "Financial Statement Analysis (FSA)",
    "Business Valuation (BussV)", "Security and Portfolio Management (SPM)", "International Finance (IF)",
    "Management of Banks (MoB)", "Programing for Analytics (PA)", "Text Mining and Sentiment Analytics (TM&SA)",
    "Data Mining and Visualization (DMV)", "Analytics for Service Operations (ASO)", "AI and Machine Learning (AIML)",
    "Digital Media (DM)", "Media Production and Consumption (MPC)", "Media and Sports Industry (MSI)",
    "Media Research Tools and Analytics (MRTA)", "Media Cost Management & Control (MCMC)", "Performance Management System (PMS)",
    "Talent Acquisition (TA)", "Learnings & Development (L&D)", "Compensation & Reward Management (C&RM)",
    "Purchasing & Inventory Management (P&IM)", "Supply Chain Management (SCM)", "Transportation & Distribution Management (TDM)",
    "Warehousing & Distribution Facilities Management (W&DFM)"
]

# Initialize profiles dictionary
if "profiles" not in st.session_state:
    st.session_state["profiles"] = {}

# Sidebar for navigation
st.sidebar.title("Navigation")
pages = st.sidebar.radio("Go to", ["Create Profile", "Edit/Delete Profile", "Generate Timetable"])

if pages == "Create Profile":
    st.title("Create Profile")
    name = st.text_input("Enter your name")
    enrollment_no = st.text_input("Enter your enrollment number")
    section = st.selectbox("Select your section", ["A", "B", "C"])

    st.subheader("Compulsory Subjects")
    for subject in compulsory_subjects:
        st.checkbox(subject, value=True, disabled=True)

    st.subheader("General Electives 1")
    elective_1 = st.selectbox("Choose one", general_electives_1)

    st.subheader("General Electives 2")
    elective_2 = st.selectbox("Choose one", general_electives_2)

    st.subheader("Major Sector")
    major_sector = st.selectbox("Choose a sector", list(major_sectors.keys()))
    for subject in major_sectors[major_sector]:
        st.checkbox(subject, value=True, disabled=True)

    st.subheader("Additional Subject")
    additional_subject = st.selectbox("Choose one", additional_subjects)

    if st.button("Save Profile"):
        st.session_state["profiles"][enrollment_no] = {
            "name": name,
            "section": section,
            "elective_1": elective_1,
            "elective_2": elective_2,
            "major_sector": major_sector,
            "additional_subject": additional_subject
        }
        st.success("Profile saved successfully!")

elif pages == "Edit/Delete Profile":
    st.title("Edit or Delete Profile")
    enrollment_no = st.text_input("Enter your enrollment number to search")

    if enrollment_no in st.session_state["profiles"]:
        profile = st.session_state["profiles"][enrollment_no]
        st.write(f"Name: {profile['name']}")
        st.write(f"Section: {profile['section']}")
        st.write(f"Elective 1: {profile['elective_1']}")
        st.write(f"Elective 2: {profile['elective_2']}")
        st.write(f"Major Sector: {profile['major_sector']}")
        st.write(f"Additional Subject: {profile['additional_subject']}")

        if st.button("Delete Profile"):
            del st.session_state["profiles"][enrollment_no]
            st.success("Profile deleted successfully!")

        if st.button("Edit Profile"):
            st.session_state["profiles"][enrollment_no] = {
                "name": st.text_input("Enter your name", value=profile['name']),
                "section": st.selectbox("Select your section", ["A", "B", "C"], index=["A", "B", "C"].index(profile['section'])),
                "elective_1": st.selectbox("Choose one", general_electives_1, index=general_electives_1.index(profile['elective_1'])),
                "elective_2": st.selectbox("Choose one", general_electives_2, index=general_electives_2.index(profile['elective_2'])),
                "major_sector": st.selectbox("Choose a sector", list(major_sectors.keys()), index=list(major_sectors.keys()).index(profile['major_sector'])),
                "additional_subject": st.selectbox("Choose one", additional_subjects, index=additional_subjects.index(profile['additional_subject']))
            }
            st.success("Profile edited successfully!")

    else:
        st.info("No profile found for this enrollment number.")

elif pages == "Generate Timetable":
    st.title("Generate Timetable")
    uploaded_file = st.file_uploader("Upload the general timetable", type=["xlsx"])

    if uploaded_file is not None:
        general_timetable = pd.read_excel(uploaded_file)
        enrollment_no = st.selectbox("Select your enrollment number", list(st.session_state["profiles"].keys()))

        if enrollment_no:
            profile = st.session_state["profiles"][enrollment_no]
            selected_subjects = [
                profile["elective_1"], 
                profile["elective_2"], 
                profile["additional_subject"]
            ] + major_sectors[profile["major_sector"]] + compulsory_subjects

            filtered_timetable = general_timetable[general_timetable['Subject'].isin(selected_subjects)]
            
            st.write("Generated Timetable")
            st.dataframe(filtered_timetable)

            # Option to download the generated timetable
            download_timetable = filtered_timetable.to_excel(index=False)
            st.download_button(
                label="Download Timetable",
                data=download_timetable,
                file_name=f"timetable_{enrollment_no}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
