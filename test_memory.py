
import tempfile
from pathlib import Path

import memory


def test_memory():

    # Use a temporary database instead of the personal database.
    with tempfile.TemporaryDirectory() as temp_dir:

        memory.DATABASE = Path(temp_dir) / "test_spammer.db"

        memory.initialize_memory()

        memory.save_message("user", "Hello SPAMMER!")
        memory.save_message("assistant", "Hello! How can I help you?")

        messages = memory.get_recent_messages()

        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[1]["role"] == "assistant"

        print("Memory test passed successfully!")


if __name__ == "__main__":
    test_memory()
