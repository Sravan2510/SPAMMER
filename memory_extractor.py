
import json
import ollama

from memory import (
    save_memory,
    save_memory_candidate,
    get_all_memories,
    memory_exists,
    candidate_exists
)


# Common sensitive information keywords.
SENSITIVE_KEYWORDS = [
    "password",
    "passcode",
    "one-time password",
    "otp",
    "credit card number",
    "cvv",
    "bank account number",
    "api key",
    "secret key",
    "access token",
    "private key",
    "recovery phrase"
]


def contains_sensitive_information(information):
    """
    Check for common sensitive credentials
    and financial information.
    """

    text = information.casefold()

    return any(
        keyword in text
        for keyword in SENSITIVE_KEYWORDS
    )



def determine_memory_risk(category, information, model_risk):
    """
    Independently determine how a memory should be handled.
    Python rules take priority over the model's classification.
    """

    if contains_sensitive_information(information):
        return "blocked"

    approval_keywords = [
        "major decision",
        "career change",
        "change career",
        "career direction",
        "decided to",
        "long-term plan",
        "life decision",
        "resign",
        "relocate",
        "move abroad",
        "marriage",
        "financial decision"
    ]

    combined_text = (
            category + " " + information
    ).casefold()

    if any(
            keyword in combined_text
            for keyword in approval_keywords
    ):
        return "approval"

    if model_risk == "approval":
        return "approval"

    if model_risk == "low":
        return "low"

    return "blocked"

MEMORY_EXTRACTION_PROMPT = """
You are the memory extraction engine for SPAMMER,
a personal AI assistant.

Your task is to identify useful information from
the user's conversation that may be worth remembering.

IDENTIFY:
- Personal preferences
- Learning interests
- Technical skills
- Projects and career goals
- Long-term plans
- Frequently mentioned requirements

MEMORY RULES:

1. Extract only information explicitly stated by the user.
2. Do not invent facts or make assumptions.
3. Ignore temporary questions and casual conversation.
4. Avoid duplicate or already-known memories.
5. Do not save passwords, financial credentials,
   or other sensitive personal information.
6. Do not treat hypothetical statements as facts.

RISK CLASSIFICATION:

- low: Ordinary preferences, learning interests,
  technical skills and project information.

- approval: Important personal decisions,
  major changes and information requiring confirmation.

- blocked: Sensitive information that must not
  be saved or submitted for approval.

OUTPUT FORMAT:

Return ONLY valid JSON in this format:

{
    "memories": [
        {
            "category": "Preference",
            "information": "Prefers practical examples",
            "risk_level": "low"
        }
    ]
}

If no useful information is found, return:

{
    "memories": []
}

Do not include explanations or Markdown formatting.
"""


def extract_memories(user_message):
    """
    Analyse a user message and identify useful
    information that may be worth remembering.

    This function only extracts suggestions.
    It does not save anything to the database.
    """

    existing_memories = get_all_memories()

    memory_context = "\n".join(
        f"- [{item['category']}] {item['information']}"
        for item in existing_memories
    )

    try:
        response = ollama.chat(
            model="qwen3.5:4b",
            messages=[
                {
                    "role": "system",
                    "content": MEMORY_EXTRACTION_PROMPT
                },
                {
                    "role": "user",
                    "content": (
                            "Existing memories:\n"
                            + (
                                memory_context
                                if memory_context
                                else "No existing memories."
                            )
                            + "\n\nAnalyse this user message:\n"
                            + user_message
                    )
                }
            ],
            format="json",
            think=False,
            options={
                "temperature": 0.1,
                "num_predict": 512
            }
        )

        result = json.loads(response.message.content)

        if not isinstance(result, dict):
            return []

        memories = result.get("memories", [])

        if not isinstance(memories, list):
            return []

        valid_memories = []

        for item in memories:

            if not isinstance(item, dict):
                continue

            category = item.get("category")
            information = item.get("information")
            model_risk = item.get("risk_level")

            if not all(
                    isinstance(value, str) and value.strip()
                    for value in (category, information, model_risk)
            ):
                continue

            if len(category) > 50 or len(information) > 500:
                continue

            category = category.strip()
            information = information.strip()

            # Python independently determines memory risk.
            risk_level = determine_memory_risk(
                category,
                information,
                model_risk
            )

            # Never save blocked information.
            if risk_level == "blocked":
                continue

            # Skip existing permanent memories.
            if memory_exists(category, information):
                continue

            # Skip existing pending candidates.
            if candidate_exists(category, information):
                continue

            valid_memories.append({
                "category": category,
                "information": information,
                "risk_level": risk_level
            })

        return valid_memories

    except (ValueError, TypeError, KeyError) as error:
        print(f"Memory extraction error: {error}")
        return []

    except Exception as error:
        print(f"AI extraction error: {error}")
        return []

def process_memories(user_message):
    """
    Extract memories and save them according to risk level.

    Low-risk memories are saved automatically.
    Approval-required memories become pending candidates.
    Blocked memories are discarded.
    """

    memories = extract_memories(user_message)

    saved_count = 0
    approval_count = 0

    for memory in memories:

        category = memory["category"]
        information = memory["information"]
        risk_level = memory["risk_level"]

        if risk_level == "low":

            if not memory_exists(category, information):
                save_memory(category, information)
                saved_count += 1

        elif risk_level == "approval":

            if not candidate_exists(category, information):
                save_memory_candidate(
                    category,
                    information,
                    risk_level
                )
                approval_count += 1

    return {
        "saved": saved_count,
        "pending_approval": approval_count
    }