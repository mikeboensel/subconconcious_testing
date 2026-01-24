import os
from dotenv import load_dotenv
from subconscious import Client

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("SUBCONSCIOUS_API_KEY")
if not api_key:
    raise ValueError(
        "SUBCONSCIOUS_API_KEY not found in environment variables. Please set it in .env file."
    )

# Initialize the client
client = Client(
    base_url="https://api.subconscious.dev/v1",  # can be omitted
    api_key=api_key,  # get it from https://subconscious.dev
)

# Define tools
tools = [
    {
        "type": "function",
        "name": "calculator",
        "url": "http://localhost:8000/calculate",  # the server url of your own tool
        "method": "POST",
        "timeout": 5,  # seconds
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {"type": "string"},
                "a": {"type": "number"},
                "b": {"type": "number"},
            },
            "required": ["operation", "a", "b"],
        },
    }
]

# Build toolkit
client.build_toolkit(tools, agent_name="math_agent")

# Run agent
messages = [{"role": "user", "content": "What is 2 + 3?"}]
response = client.agent.run(messages, agent_name="math_agent")
print(response)
