import google.generativeai as genai

genai.configure(api_key="AIzaSyAzC61EdUc5DAojnWs9PdlnowsWXxeTdEk")
model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-1219",warning=True)
response = model.generate_content("Explain how AI works(in 3 sentences)")
print(response.text)