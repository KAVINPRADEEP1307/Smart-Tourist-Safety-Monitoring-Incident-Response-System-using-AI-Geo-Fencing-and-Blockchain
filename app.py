
import streamlit as st

st.set_page_config(
page_title="Smart Tourist Safety Monitoring System",
page_icon="🛡️",
layout="wide"
)

st.title("🛡️ Smart Tourist Safety Monitoring & Incident Response System")
st.subheader("Using AI, Geo-Fencing and Blockchain")

menu = st.sidebar.selectbox(
"Navigation",
[
"Login",
"Tourist Dashboard",
"Geo-Fencing",
"SOS",
"AI Risk",
"Incident Report",
"Admin Dashboard"
]
)

if menu == "Login":
st.header("Login")
st.text_input("Username")
st.text_input("Password", type="password")
if st.button("Login"):
st.success("Login Successful (Demo)")

elif menu == "Tourist Dashboard":
st.header("Tourist Dashboard")
c1, c2, c3 = st.columns(3)
c1.metric("Current Status", "Safe")
c2.metric("Risk Level", "Low")
c3.metric("Alerts", "0")

elif menu == "Geo-Fencing":
st.header("Geo-Fencing")
st.success("Tourist is inside Safe Zone")

elif menu == "SOS":
st.header("Emergency SOS")
if st.button("🚨 SEND SOS"):
st.error("Emergency Alert Sent Successfully!")

elif menu == "AI Risk":
st.header("AI Risk Prediction")
score = st.slider("Risk Score", 0, 100, 20)
if score < 30:
st.success("Low Risk")
elif score < 70:
st.warning("Medium Risk")
else:
st.error("High Risk")

elif menu == "Incident Report":
st.header("Incident Report")
st.text_area("Describe Incident")
if st.button("Submit Report"):
st.success("Incident Saved Successfully")

elif menu == "Admin Dashboard":
st.header("Admin Dashboard")
st.metric("Total Tourists", 120)
st.metric("Active Alerts", 2)
st.metric("Incidents", 15)
