from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client with Subconscious endpoint
client = OpenAI(
    base_url="https://api.subconscious.dev/v1",
    api_key=os.getenv("SUBCONSCIOUS_API_KEY"),
)

# Make a simple request without tools
response = client.chat.completions.create(
    model="tim-large",
    messages=[
        {"role": "user", "content": "Find the derivative of f(x) = x^3 * sin(x)"}
    ],
)

print(response.choices[0].message.content)
