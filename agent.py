import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = os.environ.get("MODEL", "claude-haiku-5-5")


def get_donut_time(servings: int) -> str:
    """Return a simple time estimate for a batch of donuts."""
    minutes = 90 + servings * 2
    return f"About {minutes} minutes total, including a 1 hour prove."


TOOLS = [
    {
        "name": "get_donut_time",
        "description": "Estimate total time to make a batch of donuts.",
        "input_schema": {
            "type": "object",
            "properties": {"servings": {"type": "integer", "description": "Number of donuts"}},
            "required": ["servings"],
        },
    }
]

HANDLERS = {"get_donut_time": get_donut_time}


def run(user_message: str, max_steps: int = 5) -> str:
    messages = [{"role": "user", "content": user_message}]
    for _ in range(max_steps):
        response = client.messages.create(
            model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages
        )
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")

        messages.append({"role": "assistant", "content": response.content})
        results = []
        for block in response.content:
            if block.type == "tool_use":
                output = HANDLERS[block.name](**block.input)
                results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": output}
                )
        messages.append({"role": "user", "content": results})
    return "Stopped after max steps."


if __name__ == "__main__":
    import sys

    print(run(sys.argv[1] if len(sys.argv) > 1 else "How long for 12 donuts?"))
