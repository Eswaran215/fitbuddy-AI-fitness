import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(page_title="FitBuddy AI Fitness Generator", page_icon="💪", layout="centered")

# Load API Key from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found in Streamlit Secrets!")

st.title("💪 FitBuddy - AI Fitness Plan Generator")
st.write("Generate your personalized workout and diet plan instantly using Google Gemini AI.")

# User Input Form
with st.form("fitness_form"):
    name = st.text_input("Your Name")
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
    goal = st.selectbox("What are you moving toward?", ["Lose Weight", "Build Muscle", "Stay Fit"])
    challenge = st.selectbox("How much challenge sounds right?", ["Beginner", "Moderate", "Advanced"])
    
    submitted = st.form_submit_button("Build my plan")

if submitted:
    if not name:
        st.warning("Please enter your name.")
    else:
        with st.spinner("Generating your personalized plan... Please wait..."):
            try:
                # Using the stable gemini-3.6-flash model
                model = genai.GenerativeModel('gemini-3.6-flash')
                
                prompt = f"""
                Create a personalized 3-day fitness and diet plan for:
                - Name: {name}
                - Age: {age}
                - Weight: {weight} kg
                - Goal: {goal}
                - Fitness Level: {challenge}
                
                Give a structured workout routine and a simple meal/diet plan.
                """
                
                response = model.generate_content(prompt)
                
                st.success("Here is your custom FitBuddy Plan!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
