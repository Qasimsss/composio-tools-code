from composio_openai import ComposioToolSet, Action
from litellm import completion
import os
import json

composio_key = ""  # Replace with your actual Composio API key
composio_toolset = ComposioToolSet(api_key=composio_key)

# Create a trigger listener
listener = composio_toolset.create_trigger_listener()


@listener.callback(filters={"trigger_name": "GMAIL_NEW_GMAIL_MESSAGE"})
def callback_function(event):
    try:
        # Extracting payload from event
        payload = event.payload
        thread_id = payload.get("threadId")
        message_text = payload.get("messageText")
        sender = payload.get("sender")

        if message_text and sender:
            print(f"New Email Received:")
            print(f"Thread ID: {thread_id}")
            print(f"Sender: {sender}")
            print(f"Message: {message_text}")

            # Getting the available tools (GMAIL_SEND_EMAIL)
            tools = composio_toolset.get_tools(actions=[Action.GMAIL_SEND_EMAIL])

            # Calling GPT model to generate the reply
            response = completion(
                model="gpt-4o-mini",
                tools=tools,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for auto email reply."},
                    {"role": "user", "content": f"You have to reply to {sender} about this message: {message_text}"},
                ],
            )

            tool_call = response.choices[0].message.tool_calls[0]

            # Assuming tool_call.function.arguments contains a dict or a serialized string
            arguments = tool_call.function.arguments

            # If the arguments are in string format, convert them to a dictionary
            if isinstance(arguments, str):
                
                arguments = json.loads(arguments)

            # Extract the necessary fields from arguments
            recipient = arguments.get("recipient_email")
            subject = arguments.get("subject")
            body = arguments.get("body")

            # Construct the email message
            email_data = {
                "to": recipient,
                "subject": subject,
                "body": body,
            }

            # Execute the GMAIL_SEND_EMAIL tool
            result = composio_toolset.get_tools(Action.GMAIL_SEND_EMAIL, email_data)
            print(f"Email sent: {result}")
        else:
            print("No tool calls found in the GPT response.")

    except Exception as e:
        print(f"An error occurred in the callback function: {e}")

print("Starting to listen for triggers...")
try:
    listener.listen()
except Exception as e:
    print(f"An error occurred while listening: {e}")

