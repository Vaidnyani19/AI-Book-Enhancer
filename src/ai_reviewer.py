import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyCQ6CaFPICXXe1XAfWRpax0-3oON4q0wfY")  # Replace with your actual key

# Initialize the Gemini model
model = genai.GenerativeModel("models/gemini-2.0-flash")

def review_chapter(text):
    """
    Reviews the chapter for grammar, tone, coherence, and improvement suggestions.
    """
    prompt = f"""You are a professional editor. Please review the following text for:
- Grammar and punctuation
- Tone and engagement
- Coherence and logical flow
- Suggestions for improvement

Text:
{text}
"""
    response = model.generate_content(prompt)
    return response.text
