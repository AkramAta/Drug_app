import streamlit as st
import google.generativeai as genai

api_key = st.secrets["general"]["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash-latest")
 
from main import load_data
df = load_data()

# Function to analyze drug interactions
def analyze_interaction(drug1, drug2, interaction_desc):
    prompt = f"""
    The interaction between {drug1} and {drug2} is described as: "{interaction_desc}".
    Reply with only one of the following: "Safe" or "Not Safe", followed by a very short reason (max 2 sentences).
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit UI
def show_drug_interaction(df):
    st.title("Drug Interaction Checker")

    drug1 = st.selectbox("Select the first drug:", df["Drug 1"].unique())
    drug2 = st.selectbox("Select the second drug:", df["Drug 2"].unique())

    if st.button("Check Interaction"):
        interaction = df[(df["Drug 1"] == drug1) & (df["Drug 2"] == drug2)]

        if not interaction.empty:
            interaction_desc = interaction["Interaction Description"].values[0]
            st.write(f"**Interaction:** {interaction_desc}")

            ai_response = analyze_interaction(drug1, drug2, interaction_desc)
            st.subheader("AI Analysis:")
            st.write(f"🩺 **{ai_response}**")
        else:
            st.info("No interaction found in the database. Asking AI for analysis...")
            prompt = f"""
            Do {drug1} and {drug2} have any known drug interaction? 
            If yes, describe the interaction briefly and classify it as "Safe" or "Not Safe".
            If no known interaction, say "Safe – No known interaction reported".
            """
            try:
                response = model.generate_content(prompt)
                st.subheader("AI Analysis:")
                st.write(f"🧠 **{response.text.strip()}**")
            except Exception as e:
                st.error(f"AI analysis failed: {e}")

# Run the app
show_drug_interaction(df)
