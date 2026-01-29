from google import genai

client = genai.Client(api_key="AIzaSyC4umHlt6H7eMVdQhd0B7ja0LK-V-f3P4M")

for m in client.models.list():
    print(m.name)
