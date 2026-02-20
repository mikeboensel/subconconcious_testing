from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client with Subconscious endpoint
client = OpenAI(
    base_url="https://api.subconscious.dev/v1",
    api_key=os.getenv(
        "sk-37e64a33a98cb3c362cea5f55c3ffffd8059544fdbcc2dfa7279ebf0fe8c51be"
    ),
)

# Make a simple request without tools
response = client.chat.completions.create(
    model="tim-large",
    messages=[
        {"role": "user", "content": "Find the derivative of f(x) = x^3 * sin(x)"}
    ],
)

print(response.choices[0].message.content)
