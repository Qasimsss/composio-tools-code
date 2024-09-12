from composio_openai import ComposioToolSet

# API keys should be stored in environment variables for security
composio_key = "" # Replace with your actual Composio API key

# Initialize ComposioToolSet with your API key
composio_toolset = ComposioToolSet(api_key=composio_key)

# Create a trigger listener
listener = composio_toolset.create_trigger_listener()

# Define callback function for the trigger
@listener.callback(filters={"trigger_name": "GMAIL_NEW_GMAIL_MESSAGE"})  # Correct trigger name
def callback_function(event):
    try:
        # Extract the payload from the event
        payload = event.payload
        
        # Extracting necessary fields from the payload
        thread_id = payload.get("threadId")
        message_text = payload.get("messageText")
        sender = payload.get("sender")
        
        
        # Print extracted information for debugging
        print(f"New Email Received:")
        print(f"Thread ID: {thread_id}")
        print(f"Sender: {sender}")
        print(f"Message: {message_text}")
        

    except Exception as e:
        # Handle errors gracefully and print error message
        print(f"An error occurred: {e}")

# Start listening for triggers
print("Starting to listen for triggers...")
try:
    listener.listen()
except Exception as e:
    print(f"An error occurred while listening: {e}")

