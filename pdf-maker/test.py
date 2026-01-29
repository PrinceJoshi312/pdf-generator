from google import genai

client = genai.Client(api_key="AIzaSyC4umHlt6H7eMVdQhd0B7ja0LK-V-f3P4M")

resp = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Reply with OK"
)

print(resp.text)
