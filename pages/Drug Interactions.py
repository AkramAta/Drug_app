import streamlit as st
import google.generativeai as genai
from main import load_data

# Load API key and configure Gemini
api_key = st.secrets["general"]["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Load your dataset
df = load_data()

# Function to analyze drug interactions with severity
def analyze_interaction(drug1, drug2, interaction_desc):
    prompt = f"""
    The interaction between {drug1} and {drug2} is described as: "{interaction_desc}".
    Classify the interaction as one of the following: "Safe" or "Not Safe".
    Then, provide:
    - A short reason (max 2 sentences)
    - A severity level: "None", "Low", "Moderate", or "High"

    Format your answer exactly as:
    Safety: <Safe/Not Safe>
    Reason: <short reason>
    Severity: <None/Low/Moderate/High>
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit UI
def show_drug_interaction(df):
    st.title("💊 Drug Interaction Checker")

    drug1 = st.selectbox("Select the first drug:", df["Drug 1"].unique())
    drug2 = st.selectbox("Select the second drug:", df["Drug 2"].unique())

    if st.button("Check Interaction"):
        interaction = df[(df["Drug 1"] == drug1) & (df["Drug 2"] == drug2)]

        if not interaction.empty:
            interaction_desc = interaction["Interaction Description"].values[0]
            st.write(f"**Interaction:** {interaction_desc}")

            ai_response = analyze_interaction(drug1, drug2, interaction_desc)
            st.subheader("AI Analysis:")
            display_ai_analysis(ai_response)

        else:
            st.info("No interaction found in the database. Asking AI for analysis...")
            prompt = f"""
            Do {drug1} and {drug2} have any known drug interaction? 
            If yes, describe the interaction briefly, classify it as "Safe" or "Not Safe", and give severity: None, Low, Moderate, or High.
            Use this format:
            Safety: <Safe/Not Safe>
            Reason: <short reason>
            Severity: <None/Low/Moderate/High>
            """
            try:
                response = model.generate_content(prompt)
                st.subheader("AI Analysis:")
                display_ai_analysis(response.text.strip())
            except Exception as e:
                st.error(f"AI analysis failed: {e}")

# Helper to parse and display AI response nicely
def display_ai_analysis(ai_text):
    lines = ai_text.splitlines()
    for line in lines:
        if "Safety:" in line:
            st.write(f"🛡️ **{line.strip()}**")
        elif "Reason:" in line:
            st.write(f"💡 {line.strip()}")
        elif "Severity:" in line:
            severity = line.split(":")[1].strip().capitalize()
            emoji = {
                "None": "🟢",
                "Low": "🟡",
                "Moderate": "🟠",
                "High": "🔴"
            }.get(severity, "⚠️")
            st.write(f"{emoji} **Severity: {severity}**")

# Run the app
show_drug_interaction(df)
