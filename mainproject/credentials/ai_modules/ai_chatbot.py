from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY"
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Verify this credential"
        }
    ]
)

print(response.choices[0].message.content)
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-pro")

response = model.generate_content(
    "Verify this credential"
)

print(response.text)