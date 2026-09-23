import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FitBuddy AI", page_icon="🏋️‍♂️")

st.title("🏋️‍♂️ FitBuddy - AI Fitness Plan Generator")
st.write("Personalized Workout & Diet Plan Generator using Gemini AI")

api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")
name = st.text_input("What should we call you?")
age = st.number_input("Age", min_value=10, max_value=100, value=25)
weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
goal = st.text_input("What are you moving toward?", placeholder="e.g., Build muscle, Lose weight")
level = st.selectbox("How much challenge sounds right?", ["Beginner", "Moderate", "Advanced"])

if st.button("Build my plan"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar!")
    elif not name or not goal:
        st.warning("Please fill in all details!")
    else:
        with st.spinner("Generating your personalized plan..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Create a detailed personalized fitness and diet plan for:
                - Name: {name}
                - Age: {age}
                - Weight: {weight} kg
                - Goal: {goal}
                - Fitness Level: {level}
                
                Provide daily workout routine and meal recommendations clearly.
                """
                
                response = model.generate_content(prompt)
                st.success("Your plan is ready!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}") 
