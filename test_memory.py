
from memory import (
    initialize_memory,
    save_message,
    get_recent_messages
)

initialize_memory()

save_message("user", "Hello SPAMMER!")
save_message("assistant", "Hello! How can I help you?")

messages = get_recent_messages()

print("\nSaved conversations:")

for message in messages:
    print(f"{message['role']}: {message['content']}")
