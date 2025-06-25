import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY") #get it from google ai stuido
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")


def chat_with_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()
