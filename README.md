# agentic-donut-assistant

A small Python agent that uses Claude's tool-use loop. The model can call `get_donut_time` to estimate how long a batch of donuts takes.

## Setup

```bash
pip install anthropic
export ANTHROPIC_API_KEY=your_key_here
python agent.py "How long for 12 donuts?"
```

Set `MODEL` to change the model. The default is `claude-haiku-5-5`.
