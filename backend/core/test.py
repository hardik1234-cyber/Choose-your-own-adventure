import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyCgOKKJ3laETWBnJpc3FnVpKC7MLvDcaTo')

# for m in genai.list_models():
#     print(m.name)

model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)