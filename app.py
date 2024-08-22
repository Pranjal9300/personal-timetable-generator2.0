import json
import os
import streamlit as st

# Define the path to the profiles file
PROFILES_FILE = 'profiles.json'

def load_profiles():
    if not os.path.exists(PROFILES_FILE):
        return {}  # Return an empty dictionary if the file doesn't exist
    
    try:
        with open(PROFILES_FILE, 'r') as file:
            data = file.read()
            if not data:
                return {}  # Return an empty dictionary if the file is empty
            return json.loads(data)
    except json.JSONDecodeError:
        st.error("Error reading the profiles file. The file might be corrupted or invalid.")
        return {}  # Return an empty dictionary if there's an error

def save_profiles(profiles):
    with open(PROFILES_FILE, 'w') as file:
        json.dump(profiles, file, indent=4)

def create_profile(name, enrollment_no, section, subjects):
    profiles = load_profiles()
    profiles[enrollment_no] = {
        'name': name,
        'section': section,
        'subjects': subjects
    }
    save_profiles(profiles)
    st.success("Profile created successfully!")

def update_profile(enrollment_no, section, subjects):
    profiles = load_profiles()
    if enrollment_no in profiles:
        profiles[enrollment_no].update({
            'section': section,
            'subjects': subjects
        })
        save_profiles(profiles)
        st.success("Profile updated successfully!")
    else:
        st.error("No profile found with the given enrollment number.")

def delete_profile(enrollment_no):
    profiles = load_profiles()
    if enrollment_no in profiles:
        del profiles[enrollment_no]
        save_profiles(profiles)
        st.success("Profile deleted successfully!")
    else:
        st.error("No profile found with the given enrollment number.")

def display_all_profiles():
    profiles = load_profiles()
    if profiles:
        for enrollment_no, profile in profiles.items():
            name = profile.get('name', 'N/A')
            section = profile.get('section', 'N/A')
            subjects = profile.get('subjects', [])
            st.write(f"**Name**: {name} | **Enrollment No**: {enrollment_no} | **Section**: {section} | **Subjects**: {', '.join(subjects)}")
            st.write("---")
    else:
        st.write("No profiles available.")

# Streamlit app UI
st.title("Profile Management")

menu = st.sidebar.selectbox("Menu", ["Create Profile", "Update Profile", "Delete Profile", "View Profiles"])

if menu == "Create Profile":
    st.header("Create Profile")
    name = st.text_input("Name")
    enrollment_no = st.text_input("Enrollment Number")
    section = st.selectbox("Select Section", ["A", "B", "C"])
    # Add subject selection logic here
    subjects = st.text_input("Subjects (comma-separated)").split(",")  # Example, adapt as needed
    if st.button("Create Profile"):
        create_profile(name, enrollment_no, section, subjects)

elif menu == "Update Profile":
    st.header("Update Profile")
    enrollment_no = st.text_input("Enter your enrollment number")
    if enrollment_no:
        profiles = load_profiles()
        if enrollment_no in profiles:
            name = st.text_input("Name", value=profiles[enrollment_no]['name'])
            section = st.selectbox("Select Section", ["A", "B", "C"], index=["A", "B", "C"].index(profiles[enrollment_no]['section']))
            subjects = st.text_input("Subjects (comma-separated)", value=", ".join(profiles[enrollment_no]['subjects'])).split(",")
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
