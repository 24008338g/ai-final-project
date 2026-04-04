from fireworks import Fireworks
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

fireworks_api_key = os.getenv("FIREWORKS_API_KEY")

client = Fireworks()

response = client.chat.completions.create(
  model="accounts/fireworks/models/deepseek-v3p1",
  messages=[{
    "role": "user",
    "content": "Say hello in Spanish",
  }],
)

print(response.choices[0].message.content)

