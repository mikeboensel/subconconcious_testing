import os
from dotenv import load_dotenv
from subconscious import Subconscious
from time import sleep
from tools.requests_registration import get_requests_tool
from models import HN_Sentiment_Analysis

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("SUBCONSCIOUS_API_KEY")
if not api_key:
    raise ValueError(
        "SUBCONSCIOUS_API_KEY not found in environment variables. "
        "Please set it in .env file."
    )


client = Subconscious(api_key="sk-4c8b4065efeef70367209eb7c8d97064c40777068f23cb4b230c4d526b1ba8a1", 
    base_url="http://localhost:8000/v1",
)

# Note: This will change, should point to a stood up version of the requests_tool_impl.py
NGROK_URL = "https://b6b0-209-160-132-134.ngrok-free.app"


#####
# Struggled to get things to work consistently + return what was desired.
# Prompts
#####

# Just trying to get it to call my requests tool.
simple_tool_check = """
Make a GET request to https://httpbin.org/get.
Return the status code, headers, and body."""

# Original desired prompt. I added some constraints.
hn_instructions = """Provide a breakdown of the topics currently (within the last week) being discussed on Hacker News (https://news.ycombinator.com/). 
Limit yourself to 20 posts total.
I want 2 breakdowns:
1. Group by 3 broad categories and the sentiment of the comments of the grouped posts.
2  Provide a heirarchical breakdown of each broad category into posts that were incorporated into it. 
Include the top 5 posts as measured by number of comments. 
The Post entries should have a summary (1-2 sentences), a link to it, and a sentiment score (1-5)."""

# Simplified when the above prompt failed
hn_instructions_simpler = """
Find the top 10 posts (measured by number of comments) on Hacker News (https://news.ycombinator.com/) for the last week.
Provide the title of the post, a link to it, the # of upvotes, the # of comments, a sentimental analysis of the comments(1-5), provide a positive and negative example of a comment."""


# Having fun. Let's task this agent with figuring out a good project.
interview_project = """
I am currently interviewing for a position as a software engineer at a subconscious.dev. As part of this I was asked to create a project that exercises the platform.
You can find docs at: https://docs.subconscious.dev/
Based on the docs and what the platform offers, suggest 3 projects that would be impressive. Bear in mind I have roughly $5 in credits and 
a few hours (manual labor) to spend on the project. 
"""


run = client.run(
    engine="tim-gpt",
    input={
        "instructions": "I need to understand Tailwind CSS and how to make a blinking banner with it.",
        "tools": [
            {"type": "mcp", "server": "https://mcp.context7.com/mcp", "name": "context7", "auth": {"type": "api_key", "token": "ctx7sk-53b3fe12-159f-4180-87fb-95e91ac87289"}},
            {"type": "platform", "id": "parallel_search"},
            # {"type": "platform", "id": "parallel_extract"},
            get_requests_tool(NGROK_URL),
        ],
        # "answerFormat": HN_Sentiment_Analysis,
    },
    options={"await_completion": False},
)


# Context7
## API Key: ctx7sk-53b3fe12-159f-4180-87fb-95e91ac87289
## Endpoint: https://mcp.context7.com/mcp

# {
#   type: "mcp";
#   server: string; // MCP server URL
#   name?: string; // Specific tool (omit to use all tools from server)
#   auth?: {
#     type: "bearer" | "api_key";
#     token?: string;
#     header?: string; // Header name for api_key auth
#   };
# }

# if not run.result or run.result.answer == "":
#     sleep(10) #I'm assuming its missing due to some timing/finalization of processing, hence the sleep.
#     run = client.get(run_id=run.run_id)

# print(run.result.answer)
