import streamlit as st
import pandas as pd
import openai
from datetime import datetime

api_key = "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"

# Load API Key
openai.api_key = api_key

st.title("Dr. Swamy's Ayurvedic Assistant")

# Doctor-only access
password = st.text_input("Enter Doctor Access Code", type="password")
if password != "drswamy123":
    st.warning("Access Denied.")
    st.stop()

# User Inputs
st.subheader("🧾 Patient Information")
name = st.text_input("Full Name")
age = st.number_input("Age", 1, 120)
gender = st.radio("Gender", ["Male", "Female"])
symptom = st.text_area("Describe the health issue:")
duration = st.text_input("How long have they had this issue?")

if st.button("Get Ayurvedic Recommendation"):
    # Store to Excel
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {
        "Timestamp": timestamp,
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Symptom": symptom,
        "Duration": duration
    }
    
    file = "dr_swamy_consultations.xlsx"
    try:
        existing = pd.read_excel(file)
        updated = pd.concat([existing, pd.DataFrame([record])], ignore_index=True)
    except FileNotFoundError:
        updated = pd.DataFrame([record])
    
    updated.to_excel(file, index=False)

    # Prompt ChatGPT
    prompt = f"""
    You are an expert Ayurvedic doctor. Based on this patient info:
    - Age: {age}
    - Gender: {gender}
    - Symptom: {symptom}
    - Duration: {duration}

    Please:
    1. Explain the issue in Ayurvedic terms (briefly)
    2. Recommend Ayurvedic medicines/remedies
    3. Suggest dietary/lifestyle advice
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }]
    )

    result = response.choices[0].message.content
    st.subheader("🪔 Ayurvedic Recommendation")
    st.markdown(result)

    st.markdown("📞 **Contact Dr. Swamy at +91-9876543210**")
