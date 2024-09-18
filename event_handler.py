from openai import AssistantEventHandler
from typing_extensions import override

class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        text_value = text.value if hasattr(text, 'value') else text
        print(f"\nassistant > {text_value}", end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > Tool call initiated: {tool_call.type}\n", flush=True)

    @override
    def on_message_done(self, message) -> None:
        print("DEBUG: on_message_done triggered")  # Debug
        
        if message.content:
            if hasattr(message.content[0], 'text') and hasattr(message.content[0].text, 'value'):
                message_content = message.content[0].text.value
                print("Assistant: " + message_content + "\n")
            else:
                print("DEBUG: No valid text found in message content.")  # Debug
        else:
            print("DEBUG: No content in the message.")  # Debug
