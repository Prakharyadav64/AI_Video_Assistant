
import os
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    print("ERROR: MISTRAL_API_KEY was not loaded.")
    raise SystemExit(1)

print("API key loaded: Yes")
print("Sending one test request to Mistral...")

url = "https://api.mistral.ai/v1/chat/completions"

payload = {
    "model": "mistral-small-latest",
    "messages": [
        {"role": "user", "content": "Reply with OK"}
    ],
    "max_tokens": 10
}

request = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        print("HTTP status:", response.status)
        result = json.loads(response.read().decode("utf-8"))
        print("API response:", result["choices"][0]["message"]["content"])

except urllib.error.HTTPError as error:
    print("HTTP status:", error.code)
    print("Error details:", error.read().decode("utf-8"))

except Exception as error:
    print("Connection or other error:", type(error).__name__, str(error))
