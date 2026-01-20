import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import re
import io
import config
client = genai.Client(api_key=config.GEMINI_API_KEY)
def run_ai_teachin_assitant():
    st.title("AI Teaching Assistant")
    st.write("Ask me anything about various subject and I'll provide answer.")
    if "history_ata" not in st.session_state:
        st.session_state.history_ata = []
    col_clear, col_export = st.columns([1, 2])
    with col_clear:
        if st.button("Clear Conversation", key="clear_ata"):
            st.session_state.history_ata = []
    with col_export:
        if st.session_state.history_ata:
            export_text = ""
            for idx, qa in enumerate(st.session_state.history_ata, start=1):
                export_text += f"Q{idx}: {qa['question']}\n"
                export_text += f"A{idx}: {qa['answer']}\n"
            bio = io.BytesIO()
            bio.write(export_text.encode("utf-8"))
            bio.seek(0)
            st.download_button(
                label="Export chat history",
                data=bio,
                file_name="ai_teaching_assistant_conversation.txt",
                mime="text/plain"
            )
    user_input = st.text_input("Enter your question here", key="input_ata")
    if st.button("Ask", key="ask_ata"):
        if user_input.strip():
            with st.spinner("Generating AI response"):
                response = generate_response(user_input.strip(), temperature=0.3)
            st.session_state.history_ata.append(
                {"question": user_input.strip(), "answer": response}
            )
            st.rerun()
        else:
            st.warning("Please Enter a question before clicking a Ask")
    st.markdown("Conversation History")
    for idx, qa in enumerate(st.session_state.history_ata, start=1):
        st.markdown(f"**Q{idx}:** {qa['question']}")
        st.markdown(f"**A{idx}:** {qa['answer']}")
def generate_response(prompt, temperature=0.3):
    try:
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)]
            )
        ]
        config_params = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=config_params
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
def generate_math_response(prompt, temperature=0.1):
    system_prompt = (
        "You are a Math Mastermind - an expert mathematics problem solver with exceptional abilities in: "
        "Algebra, Calculas, Geometry, Trigonometry, Statistics, Probability, Linear Algebra, "
        "Discete Mathematics, Number Theory, Mathematical Proofs and Logic, Applied Mathematics, Word Problems. "
        "For every math problem: "
        "1) Show clear step-by-step solutions "
        "2) Explain the Mathematical Reasoning "
        "3) Provide alternative solving methods when applicable "
        "4) Verify your answer when possible "
        "5) Use proper mathematical notation "
        "6) Break down complex problems into manageable parts "
        "Format your responses with: "
        "Clear problem identification "
        "Step-by-Step solution process "
        "Final answer highlighted "
        "Brief explanation of concepts used "
        "Always be precise, thorough and educational in your mathematical explanations."
    )
    try:
        full_prompt = f"{system_prompt}\n\nMath Problem: {prompt}"
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=full_prompt)]
            )
        ]
        config_params = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config=config_params
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
def main():
    st.sidebar.title("choose AI feature")
    option = st.sidebar.selectbox("",["AI Teaching Assitant","Math mastermind","Safe AI image Generator"])
    if option == "AI Teaching Assitant":
        run_ai_teachin_assitant()
    #elif option == "Math mastermind":
        #run_math_mastermind()
    #elif option == "Safe AI image generator":
        #run_safe_ai_image_generator()
if __name__ == "__main__":
    main()