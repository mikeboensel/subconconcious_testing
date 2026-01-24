import os
from dotenv import load_dotenv
from subconscious import Subconscious

load_dotenv()

client = Subconscious(api_key=os.getenv("SUBCONSCIOUS_API_KEY") or "")

run = client.run(
    engine="tim-large",
    input={
        "instructions": "Search for the latest AI news and summarize the top 3 stories",
        "tools": [{"type": "platform", "id": "web_search"}],
    },
    options={"await_completion": True},
)

# Failing consistently with errors like this:
# Run(run_id='114cc346-d0cd-4c32-bde2-2d52ac5796e8', status='failed', result=RunResult(answer='', reasoning=''), usage=Usage(models=[], platform_tools=[]))
# Run(run_id='bf0484ba-4fbc-49c8-ba16-71489899ed56', status='failed', result=RunResult(answer='', reasoning=''), usage=Usage(models=[], platform_tools=[]))
print(run)
