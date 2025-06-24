import google.generativeai as genai
genai.configure(api_key="AIzaSyD-WsuKcYaY8xAKhUjLfi-j8XT1CoJREVU")
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")


def chat_with_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()