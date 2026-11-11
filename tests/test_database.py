
from database.db import (
    initialize_database,
    create_conversation,
    save_message,
    get_conversations,
    get_messages
)


def main():

    print("Initializing TRUJARVIS database...")

    initialize_database()

    chat_id = create_conversation("Database Test")

    save_message(
        chat_id,
        "user",
        "Hello TRUJARVIS!"
    )

    save_message(
        chat_id,
        "assistant",
        "Hello Aditya! Database is working."
    )

    conversations = get_conversations()
    messages = get_messages(chat_id)

    print("\nConversations:", len(conversations))
    print("Messages:", len(messages))

    for message in messages:
        print(message["role"], ":", message["content"])

    print("\nDatabase test completed!")


if __name__ == "__main__":
    main()
