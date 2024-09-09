from composio_openai import ComposioToolSet, Action
from litellm import completion
import os

## set ENV variables
os.environ["OPENAI_API_KEY"] = ""   # Replace with your actual openai API key

composio_key = ""  # Replace with your actual Composio API key
composio_toolset = ComposioToolSet(api_key=composio_key)

# Create a trigger listener
listener = composio_toolset.create_trigger_listener()

def generate_auto_reply(email_message):
    prompt = (
        f"The user received the following email: '{email_message}'. "
        "Please generate a polite and helpful response in a formal tone."
    )
    try:
        response = completion(
        model="gpt-3.5-turbo",
        messages=[ {"role": "system", "content": "You are an Email Auto Replier"},
                {"role": "user", "content": prompt}]
)
      
       
        reply_message = response.choices[0].message.content
        print(reply_message)
        return reply_message
    except Exception as e:
        print(f"An error occurred during the OpenAI API call: {e}")
        return None

@listener.callback(filters={"trigger_name": "GMAIL_NEW_GMAIL_MESSAGE"})
def callback_function(event):
    try:
        payload = event.payload
        thread_id = payload.get("threadId")
        message_text = payload.get("messageText")
        sender = payload.get("sender")

        if message_text and sender:
            print(f"New Email Received:")
            print(f"Thread ID: {thread_id}")
            print(f"Sender: {sender}")
            print(f"Message: {message_text}")
            


            tool_set = ComposioToolSet()
            tools = tool_set.get_tools(actions=[Action.GMAIL_SEND_EMAIL])
            response = completion(
            model="gpt-4o-mini",
            tools=tools,
            messages=
                [
                    {"role": "system", "content": "You are a helpful assistant for auto email reply."},
                    {"role": "user", "content": f"You have to be reply to {sender} about this message {message_text}"},
                ],
            )
            print(response.choices[0].message.content)
        else:
            print("Message or sender information is missing from the event payload.")
    except Exception as e:
        print(f"An error occurred in the callback function: {e}")

print("Starting to listen for triggers...")
try:
    listener.listen()
except Exception as e:
    print(f"An error occurred while listening: {e}")