from subconscious import Subconscious
from time import sleep
client = Subconscious(
    api_key="sk-9bba1e741450302349165a78b005082cd232e17f10ae506398def9604e2589f2"
)

from pydantic import BaseModel


class HN_Sentiment(BaseModel):
    '''Sentiment score + examples, can be applied to either a post or a category.'''
    average_sentiment: float
    lower_bound: float
    upper_bound: float
    general_description: str # Ex: Tone varies; comments often critical or concerned, with occasional optimism when solutions are discussed.
    positive_examples: list[str]
    negative_examples: list[str]
class HN_Post(BaseModel):
    '''A post on Hacker News.'''
    summary: str
    link: str
    sentiment: HN_Sentiment

class HN_Category(BaseModel):
    '''A category of posts on Hacker News, contains posts (grouped by a model determined topic)'''
    name: str
    topics: list[str]
    sentiment: HN_Sentiment
    posts: list[HN_Post]

class HN_Sentiment_Analysis(BaseModel):
    '''A analysis of sentiments, broadly (across categories) and specifically (for individual posts).'''
    categories: list[HN_Category]


hn_instructions_simpler = """
Find the top 10 posts (measured by number of comments) on Hacker News (https://news.ycombinator.com/) for the last week.
Provide the title of the post, a link to it, the # of upvotes, the # of comments, a sentimental analysis of the comments(1-5), provide a positive and negative example of a comment.
"""

hn_instructions = """Provide a breakdown of the topics currently (within the last week) being discussed on Hacker News (https://news.ycombinator.com/). 
I want 2 breakdowns:
1. Group by broad categories and the sentiment of the comments of the grouped posts.
2  Provide a heirarchical breakdown of each broad category into posts that were incorporated into it. 
Include the top 5 posts as measured by number of comments. 
The Post entries should have a summary (1-2 sentences), a link to it, and a sentiment score (1-5)."""

interview_project = """
I am currently interviewing for a position as a software engineer at a subconscious.dev. As part of this I was asked to create a project that exercises the platform.
You can find docs at: https://docs.subconscious.dev/
Based on the docs and what the platform offers, suggest 3 projects that would be impressive. Bear in mind I have roughly $5 in credits and 
a few hours (manual labor) to spend on the project. 
"""


run = client.run(
    engine="tim-gpt",
    input={
        "instructions": hn_instructions,
        "tools": [
            {"type": "platform", "id": "parallel_search"},
            {"type": "platform", "id": "exa_crawl"},
            {"type": "platform", "id": "parallel_extract"},
        ],
        "answerFormat": HN_Sentiment_Analysis,
    },
    options={"await_completion": True},
)

# if not run.result or run.result.answer == "":
#     sleep(10) #I'm assuming its missing due to some timing/finalization of processing, hence the sleep.
#     run = client.get(run_id=run.run_id)

print(run.result.answer)
