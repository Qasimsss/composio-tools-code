from composio_openai import ComposioToolSet, Action
from litellm import completion

composio_key = ""  # Replace with your actual Composio API key



composio_toolset = ComposioToolSet(entity_id="default" , api_key=composio_key)

tools = composio_toolset.get_tools(actions=[Action.GOOGLECALENDAR_CREATE_EVENT])

task = "Create a 1 hour meeting event at 5:30PM tomorrow"

response = completion(
    model="gpt-4o-mini",
    tools=tools,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": task},
    ],
)

result = composio_toolset.handle_tool_calls(response)
print(result)