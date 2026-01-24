# Purpose
- Going thru Subconscious's:
    - [repos](https://github.com/subconscious-systems/subconscious)
    - [documentation](https://docs.subconscious.dev/overview)
    - [blog posts](https://www.subconscious.dev/blog/)
    - [papers](https://arxiv.org/pdf/2507.16784)
    - taking notes.

# Worked well
- `e2b_cli` example

# Errors encountered
## The Quickstart guide is outdated and doesn't work.
    - Seems to be using an older library version `subconscious-python` vs `subconscious-sdk`.
## The `examples` have a lot of varying degrees of completeness/polish. 
- Would be nice to have a docker compose to setup examples like this: https://github.com/subconscious-systems/subconscious/blob/main/examples/browser_use/agent.py

## Warming up
When running: https://github.com/subconscious-systems/subconscious/tree/main/examples/search_agent_cli
<img src="imgs/warmup_failure.png" alt="Warming up" width="500" height="auto">

## Main Docs page example 
### Uses a bad string for the engine: `tim-gpt`
- <img src="imgs/main_page_code.png" alt="TIM-GPT engine" width="500" height="auto">
- <img src="imgs/main_page_code_error.png" alt="TIM-GPT engine" width="500" height="auto">
```python
Literal["tim-small-preview", "tim-large", "timini"]
(type) Engine = Literal['tim-small-preview', 'tim-large', 'timini']
```
### Fails consistently
- `Run(run_id='114cc346-d0cd-4c32-bde2-2d52ac5796e8', status='failed', result=RunResult(answer='', reasoning=''), usage=Usage(models=[], platform_tools=[]))`
- 

# Open Questions
- Thought that the TIMRUN runtime was private? (https://github.com/subconscious-systems/subconscious)
- I see the tool defs match the OpenAI's tool definition schema and add on to it, but I wonder if it wouldn't be beneficial to also add a schema for the output to allow for more structured/interpretable outputs?
Cursor's comparison of OpenAI's tool definition schema and Subconscious's tool definition schema:
```json
tools = [
    {
        "type": "function",
        "name": "web_search",
        "description": "Search the web for current information",
        "url": "https://...",  # Subconscious extension
        "method": "GET",       # Subconscious extension
        "timeout": 30,         # Subconscious extension
        "parameters": {        # Same JSON Schema format
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    }
]
```

- Also, can Subconcious's API really hit localhost? 
    - Example: https://github.com/subconscious-systems/subconscious/blob/main/examples/browser_use/agent.py
    - I'm assuming you need it to be a publically accessible endpoint (or local going thru ngrok)? 
        - Or does the library allow for hitting non-public endpoints?

# General notes
