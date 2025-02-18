import streamlit as st
import pandas as pd

# Sample user credentials (Replace with database authentication in production)
USER_CREDENTIALS = {
    "Labour": {"username": "labour", "password": "lab123"},
    "Contractor": {"username": "contractor", "password": "con123"}
}

# Database Simulation
if "labour_db" not in st.session_state:
    st.session_state.labour_db = []  # Stores Labour details

if "job_postings" not in st.session_state:
    st.session_state.job_postings = []  # Stores job postings by contractors

if "inbox" not in st.session_state:
    st.session_state.inbox = {}  # Labour Inbox

# Login Page
def login_page():
    st.title("Job Management System")
    role = st.selectbox("Select User Role", ["Labour", "Contractor"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == USER_CREDENTIALS[role]["username"] and password == USER_CREDENTIALS[role]["password"]:
            st.session_state["user_role"] = role
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid username or password!")

# Labour Dashboard
def labour_dashboard():
    st.title("Labour Dashboard")
    st.subheader("Enter Your Details")
    emp_id = st.text_input("Employee ID")
    name = st.text_input("Name")
    dob = st.date_input("Date of Birth")
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    skill_set = st.text_input("Skill Set (e.g., Plumber, Electrician)")
    current_job = st.text_input("Currently Working Job")

    if st.button("Save Details"):
        labour_details = {"emp_id": emp_id, "name": name, "dob": dob, "age": age, "skill_set": skill_set, "current_job": current_job}
        st.session_state.labour_db.append(labour_details)
        st.success("Details Saved Successfully!")

    st.subheader("Job Offers")
    if emp_id in st.session_state.inbox:
        for job in st.session_state.inbox[emp_id]:
            st.write(f"**Job:** {job['job_title']} | **Salary:** {job['salary']} | **Company:** {job['company']}")
            if st.button(f"Accept Job - {job['job_title']}"):
                st.success(f"You accepted the job: {job['job_title']}")
                st.session_state.inbox[emp_id].remove(job)
                st.experimental_rerun()
            if st.button(f"Reject Job - {job['job_title']}"):
                st.warning(f"You rejected the job: {job['job_title']}")
                st.session_state.inbox[emp_id].remove(job)
                st.experimental_rerun()
    else:
        st.info("No job offers yet.")

# Contractor Dashboard
def contractor_dashboard():
    st.title("Contractor Dashboard")
    st.subheader("Post a Job")
    job_title = st.text_input("Job Title")
    skill_required = st.text_input("Required Skill")
    salary = st.number_input("Salary", min_value=1000, step=100)
    company = st.text_input("Company Name")
    contact_details = st.text_input("Contact Details")

    if st.button("Post Job"):
        job = {"job_title": job_title, "skill_required": skill_required, "salary": salary, "company": company, "contact_details": contact_details}
        st.session_state.job_postings.append(job)
        st.success("Job Posted Successfully!")

    st.subheader("Search Labour by Skill")
    search_skill = st.text_input("Enter Skill to Search")
    
    if st.button("Search"):
        matching_labours = [l for l in st.session_state.labour_db if search_skill.lower() in l["skill_set"].lower()]
        if matching_labours:
            for labour in matching_labours:
                st.write(f"**{labour['name']}** - Skill: {labour['skill_set']} | Current Job: {labour['current_job']}")
                if st.button(f"Send Job Offer to {labour['name']}"):
                    job_offer = {"job_title": job_title, "salary": salary, "company": company, "contact_details": contact_details}
                    if labour["emp_id"] not in st.session_state.inbox:
                        st.session_state.inbox[labour["emp_id"]] = []
                    st.session_state.inbox[labour["emp_id"]].append(job_offer)
                    st.success(f"Job offer sent to {labour['name']}")
        else:
            st.warning("No labour found with the given skill.")

# Main function
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page()
    else:
        if st.session_state["user_role"] == "Labour":
            labour_dashboard()
        elif st.session_state["user_role"] == "Contractor":
            contractor_dashboard()

if __name__ == "__main__":
    main()
