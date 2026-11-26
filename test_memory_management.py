
import tempfile
from pathlib import Path

import memory


def test_memory_management():

    original_database = memory.DATABASE

    try:
        with tempfile.TemporaryDirectory() as temp_dir:

            memory.DATABASE = Path(temp_dir) / "test_memory.db"

            memory.initialize_memory()

            # Test saving a pending candidate.
            memory.save_memory_candidate(
                "Preference",
                "Likes practical examples",
                "approval"
            )

            candidates = memory.get_pending_candidates()

            assert len(candidates) == 1
            candidate_id = candidates[0]["id"]

            # Test approving a candidate.
            assert memory.approve_memory_candidate(candidate_id)
            assert memory.memory_exists(
                "Preference",
                "Likes practical examples"
            )

            # Test duplicate prevention during approval.
            memory.save_memory_candidate(
                "Preference",
                "Likes practical examples",
                "approval"
            )

            duplicate = memory.get_pending_candidates()[0]

            assert memory.approve_memory_candidate(duplicate["id"])

            assert len(memory.get_all_memories()) == 1

            # Test rejecting a candidate.
            memory.save_memory_candidate(
                "Project",
                "Building SPAMMER",
                "approval"
            )

            rejected_candidate = memory.get_pending_candidates()[0]

            assert memory.reject_memory_candidate(
                rejected_candidate["id"]
            )

            assert len(memory.get_pending_candidates()) == 0

            # Test deleting a permanent memory.
            saved = memory.get_memories_with_ids()
            memory_id = saved[0]["id"]

            assert memory.delete_memory(memory_id)
            assert len(memory.get_all_memories()) == 0

            print("All memory management tests passed!")

    finally:
        memory.DATABASE = original_database


if __name__ == "__main__":
    test_memory_management()
