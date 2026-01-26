from pydantic import BaseModel


class HN_Sentiment(BaseModel):
    """Sentiment score + examples, can be applied to either a post or a category."""

    average_sentiment: float
    lower_bound: float
    upper_bound: float
    general_description: str  # Ex: Tone varies; comments often critical or concerned, with occasional optimism when solutions are discussed.
    positive_examples: list[str]
    negative_examples: list[str]


class HN_Post(BaseModel):
    """A post on Hacker News."""

    summary: str
    link: str
    sentiment: HN_Sentiment


class HN_Category(BaseModel):
    """A category of posts on Hacker News, contains posts (grouped by a model determined topic)"""

    name: str
    topics: list[str]
    sentiment: HN_Sentiment
    posts: list[HN_Post]


class HN_Sentiment_Analysis(BaseModel):
    """A analysis of sentiments, broadly (across categories) and specifically (for individual posts)."""

    categories: list[HN_Category]
