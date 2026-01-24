# Purpose
- Going thru Subconscious's:
    - [repos](https://github.com/subconscious-systems/subconscious)
    - [documentation](https://docs.subconscious.dev/overview)
    - [blog posts](https://www.subconscious.dev/blog/)
    - [papers](https://arxiv.org/pdf/2507.16784)
    - [Published Model](https://huggingface.co/papers/2507.16784)
    - taking notes.

# Worked well
- `e2b_cli` example

# Errors encountered
## Engines documented in the docs vs what the SDK actually supports
- `type Engine = 'tim-small-preview' | 'tim-large' | 'timini' | (string & {});`
- `https://docs.subconscious.dev/engines#available-engines`

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

# Nitpicky stuff
- [CURL example for Streaming](https://docs.subconscious.dev/core-concepts/streaming#basic-usage)
    - I'm guessing you get back a `runId` and then you can poll for the result? Should be explicit about usage example. 
- Write the engine specific costs in as constants, provide cost values directly vs making the user look it up in the docs. [here](https://docs.subconscious.dev/guides/response-handling#tracking-costs)

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
    - Answered [here](https://docs.subconscious.dev/core-concepts/tools#registering-with-subconscious)
        - IMO should be made more clear in the example code (which has a lot of localhost usage)
    - Example: https://github.com/subconscious-systems/subconscious/blob/main/examples/browser_use/agent.py
    - I'm assuming you need it to be a publically accessible endpoint (or local going thru ngrok)? 
        - Or does the library allow for hitting non-public endpoints?
- Subtasks run serially?
    - Verify as `Thread` implies parallelism
    - https://www.subconscious.dev/blog/the-cure-for-context-rot

# General notes
-  We believe this is an early phase in the cycle of AI agents, and soon agents will live closer to the metal at the model and runtime layer. The underlying large agent model will generate its next steps on the fly, use external tools, and follow its instructions to get the job done without a rigidly defined software workflow.
    - `Model Agents` vs `Framework Agents`
        - Whether the model guides itself and creates its own workflow OR is orchestrated broadly by software (control structures).

- Teams can mitigate rot with context engineering. One option is multi-agent systems that break the task into smaller pieces for subagents to handle. Another is pruning the context between steps to keep relevant information that matters. Both approaches can work, but they add engineering complexity and overhead. Walden Yan at Cognition wrote about building single-agent systems that manage their own context, and we agree with him that single agent systems are the better approach.

- The core of our system is a model and runtime designed to work together: TIM and TIMRUN. TIM handles task decomposition and tool use. TIMRUN understands the structure of TIM’s output and prunes irrelevant context between steps. Together they expertly break down tasks and extend agent usefulness beyond their context limits.

- [Article advocating for single-agent systems (rather than multi-agent systems)](https://cognition.ai/blog/dont-build-multi-agents)