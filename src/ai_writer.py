import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyCQ6CaFPICXXe1XAfWRpax0-3oON4q0wfY")  # Replace with your actual key

# Initialize the Gemini model
model = genai.GenerativeModel("models/gemini-2.0-flash")

def spin_chapter(text):
    """
    Rewrite the input chapter in an engaging and descriptive style.
    """
    prompt = "Rewrite the following text to be more engaging and descriptive:\n\n" + text
    response = model.generate_content(prompt)
    return response.text
