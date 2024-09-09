from composio_openai import ComposioToolSet, Action
from litellm import completion

os.environ["OPENAI_API_KEY"] = ""    # Replace with your actual openai API key


composio_key = ""   # Replace with your actual Composio API key 



composio_toolset = ComposioToolSet(api_key=composio_key)

tools = composio_toolset.get_tools(actions=[Action.GITHUB_ACTIVITY_STAR_REPO_FOR_AUTHENTICATED_USER])

task = "Star the repo composiohq/composio on GitHub"

response = completion(
model="gpt-4o-mini",
tools=tools,
messages=
    [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": task},
    ],
)
result = composio_toolset.handle_tool_calls(response)
print(result)
