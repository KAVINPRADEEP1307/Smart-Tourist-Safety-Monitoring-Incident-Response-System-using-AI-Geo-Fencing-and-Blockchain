import streamlit as st

st.set_page_config(
    page_title="Smart Tourist Safety System",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Smart Tourist Safety Monitoring & Incident Response System")
st.write("Using AI, Geo-Fencing and Blockchain (Demo)")

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Login",
        "Tourist Dashboard",
        "Geo-Fencing",
        "SOS Emergency",
        "AI Risk Prediction",
        "Incident Report",
        "Admin Dashboard"
    ]
)

if menu == "Login":
    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.success("Login Successful")
        else:
            st.error("Invalid Username or Password")

elif menu == "Tourist Dashboard":
    st.header("Tourist Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("Tourists", "125")
    c2.metric("Risk Level", "Low")
    c3.metric("Alerts", "2")

    st.info("Tourist is currently in a safe area.")

elif menu == "Geo-Fencing":
    st.header("Geo-Fencing")

    status = st.selectbox(
        "Current Status",
        ["Inside Safe Zone", "Outside Safe Zone"]
    )

    if status == "Inside Safe Zone":
        st.success("Tourist is inside the safe zone.")
    else:
        st.warning("Warning! Tourist has left the safe zone.")

elif menu == "SOS Emergency":
    st.header("SOS Emergency")

    if st.button("🚨 SEND SOS"):
        st.error("Emergency Alert Sent Successfully!")

elif menu == "AI Risk Prediction":
    st.header("AI Risk Prediction")

    score = st.slider("Risk Score", 0, 100, 25)

    if score < 30:
        st.success("Low Risk")
    elif score < 70:
        st.warning("Medium Risk")
    else:
        st.error("High Risk")

elif menu == "Incident Report":
    st.header("Incident Report")

    incident = st.text_area("Describe the Incident")

    if st.button("Submit Report"):
        st.success("Incident Report Submitted Successfully")
        st.write("Report:")
        st.write(incident)

elif menu == "Admin Dashboard":
    st.header("Admin Dashboard")

    st.metric("Total Tourists", "125")
    st.metric("Active Alerts", "2")
    st.metric("Incidents", "18")

    st.table({
        "Tourist": ["Alice", "Bob", "Charlie"],
        "Status": ["Safe", "Alert", "Safe"]
    })
