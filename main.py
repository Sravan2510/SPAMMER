
import ollama

from memory import (
    initialize_memory,
    save_message,
    get_recent_messages,
    get_all_memories,
    get_memories_with_ids,
    get_pending_candidates,
    approve_memory_candidate,
    reject_memory_candidate,
    delete_memory
)

from memory_extractor import process_memories

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

console = Console()

MODEL = "qwen3.5:4b"

SYSTEM_PROMPT = """
You are SPAMMER, a personal AI companion and research assistant.

Your personality:
- Friendly, approachable and conversational.
- Professional and analytical when required.
- Patient when explaining difficult topics.
- Honest when you do not know something.

Your responsibilities:
- Answer questions and explain concepts.
- Help with programming and debugging.
- Assist with learning and research.
- Help plan projects and solve problems.

Memory instructions:
- Use the personal information provided in your context when relevant.
- Use previous conversations to understand the conversation.
- Never invent personal information.
- If you do not know something, say so honestly.

Your technical architecture:

SPAMMER is a locally running personal AI assistant built using Python.

Its components:
- Python: Controls the application's logic and execution.
- Ollama: Runs AI models locally on the computer.
- Qwen 3.5 4B: The language model used to generate responses.
- Ollama Python library: Allows Python to communicate with Ollama.
- Rich: Provides the formatted terminal interface.
- SQLite: Stores conversation history and personal memories.
- memory.py: Contains functions for saving and retrieving conversations and personal information.
- main.py: Contains the main application and chat loop.

How the system works:
1. The user enters a message in the terminal.
2. Python receives the message.
3. The conversation and saved personal memories are provided as context.
4. Python sends the messages to Ollama through the Ollama Python library.
5. Ollama runs Qwen 3.5 4B locally.
6. The model generates a response.
7. Python displays the response using Rich.
8. User messages and assistant responses are saved in SQLite.

Important:
- Do not claim that SPAMMER uses technologies that are not listed in its actual implementation.
- Do not claim that it uses the requests library directly.
- Explain the difference between Python, Ollama, and the Qwen model when asked.
- Distinguish implemented features from planned features.

Always provide clear, useful and accurate answers.
"""

# --------------------------------------------------
# INITIALIZE SPAMMER
# --------------------------------------------------

# --------------------------------------------------
# MEMORY MANAGEMENT COMMANDS
# --------------------------------------------------

def show_memories():

    memories = get_memories_with_ids()

    if not memories:
        console.print("[yellow]No saved memories found.[/yellow]")
        return

    console.print("\n[bold cyan]SAVED PERSONAL MEMORIES[/bold cyan]")

    for memory in memories:

        console.print(
            f"\n[bold]ID:[/bold] {memory['id']}"
            f"\n[bold]Category:[/bold] {memory['category']}"
            f"\n[bold]Information:[/bold] {memory['information']}"
        )


def show_pending_candidates():

    candidates = get_pending_candidates()

    if not candidates:
        console.print("[yellow]No pending memories found.[/yellow]")
        return

    console.print("\n[bold yellow]PENDING MEMORY APPROVALS[/bold yellow]")

    for candidate in candidates:

        console.print(
            f"\n[bold]ID:[/bold] {candidate['id']}"
            f"\n[bold]Category:[/bold] {candidate['category']}"
            f"\n[bold]Information:[/bold] {candidate['information']}"
            f"\n[bold]Risk:[/bold] {candidate['risk_level']}"
        )

def approve_memory():

    candidates = get_pending_candidates()

    if not candidates:
        console.print("[yellow]No pending memories to approve.[/yellow]")
        return

    show_pending_candidates()

    candidate_id = Prompt.ask(
        "\n[bold green]Enter the candidate ID to approve[/bold green]"
    )

    if not candidate_id.isdigit():
        console.print("[red]Please enter a valid numeric ID.[/red]")
        return

    approved = approve_memory_candidate(int(candidate_id))

    if approved:
        console.print("[green]Memory approved successfully.[/green]")
    else:
        console.print("[red]Candidate not found or already processed.[/red]")

def reject_memory():

    candidates = get_pending_candidates()

    if not candidates:
        console.print("[yellow]No pending memories to reject.[/yellow]")
        return

    show_pending_candidates()

    candidate_id = Prompt.ask(
        "\n[bold green]Enter the candidate ID to reject[/bold green]"
    )

    if not candidate_id.isdigit():
        console.print("[red]Please enter a valid numeric ID.[/red]")
        return

    rejected = reject_memory_candidate(int(candidate_id))

    if rejected:
        console.print("[green]Memory rejected successfully.[/green]")
    else:
        console.print("[red]Candidate not found or already processed.[/red]")

def remove_memory():

    memories = get_memories_with_ids()

    if not memories:
        console.print("[yellow]No saved memories to delete.[/yellow]")
        return

    show_memories()

    memory_id = Prompt.ask(
        "\n[bold red]Enter the memory ID to delete[/bold red]"
    )

    if not memory_id.isdigit():
        console.print("[red]Please enter a valid numeric ID.[/red]")
        return

    confirmation = Prompt.ask(
        "Are you sure you want to delete this memory? (yes/no)"
    )

    if confirmation.lower() != "yes":
        console.print("[yellow]Deletion cancelled.[/yellow]")
        return

    deleted = delete_memory(int(memory_id))

    if deleted:
        console.print("[green]Memory deleted successfully.[/green]")
    else:
        console.print("[red]Memory ID not found.[/red]")

def show_help():

    console.print("\n[bold cyan]SPAMMER COMMANDS[/bold cyan]")

    commands = {
        "help": "Display available commands",
        "memories": "View saved personal memories",
        "pending": "View pending memory approvals",
        "approve": "Approve a memory candidate",
        "reject": "Reject a memory candidate",
        "delete": "Delete a saved memory",
        "exit": "Close SPAMMER"
    }

    for command, description in commands.items():

        console.print(
            f"[bold green]{command:<12}[/bold green] {description}"
        )

def main():

    initialize_memory()

    # Welcome screen
    console.print(
        Panel(
            "[bold cyan]SPAMMER[/bold cyan]\n"
            "Your Personal AI Companion & Research Assistant\n"
            "[green]AI engine connected[/green]",
            title="Welcome",
            border_style="cyan"
        )
    )

    # Load personal memories
    memories = get_all_memories()

    memory_context = "\n".join(
        f"- [{item['category']}] {item['information']}"
        for item in memories
    )

    system_message = (
            SYSTEM_PROMPT
            + "\n\nIMPORTANT PERSONAL MEMORY:\n"
            + (
                memory_context
                if memory_context
                else "No saved personal information yet."
            )
    )

    # Load conversation history
    messages = [
        {
            "role": "system",
            "content": system_message
        }
    ]

    messages.extend(get_recent_messages(limit=20))

    # --------------------------------------------------
    # MAIN CHAT LOOP
    # --------------------------------------------------

    while True:

        user_input = Prompt.ask(
            "\n[bold green]You[/bold green]"
        ).strip()

        # Exit application
        if user_input.lower() in ["exit", "quit"]:

            console.print(
                "[yellow]SPAMMER signing off. Goodbye![/yellow]"
            )

            break

        # Ignore empty messages
        if not user_input:
            continue

        # --------------------------------------------------
        # MEMORY MANAGEMENT COMMANDS
        # --------------------------------------------------

        command = user_input.lower()

        if command == "help":
            show_help()
            continue

        elif command == "memories":
            show_memories()
            continue

        elif command == "pending":
            show_pending_candidates()
            continue

        elif command == "approve":
            approve_memory()
            continue

        elif command == "reject":
            reject_memory()
            continue

        elif command == "delete":
            remove_memory()
            continue

        # Add user message
        messages.append({
            "role": "user",
            "content": user_input
        })

        save_message("user", user_input)

        # --------------------------------------------------
        # GENERATE AI RESPONSE
        # --------------------------------------------------

        try:

            with console.status(
                    "[cyan]SPAMMER is thinking...[/cyan]"
            ):

                response = ollama.chat(
                    model=MODEL,
                    messages=messages,
                    think=False,
                    options={
                        "num_predict": 512,
                        "temperature": 0.7
                    }
                )

            answer = response["message"]["content"]

            messages.append({
                "role": "assistant",
                "content": answer
            })

            save_message("assistant", answer)

            console.print(
                Panel(
                    answer,
                    title="SPAMMER",
                    border_style="cyan"
                )
            )

        except Exception as error:

            console.print(
                f"[bold red]AI Error:[/bold red] {error}"
            )

            # Do not attempt memory extraction
            # when AI response generation fails.
            continue

        # --------------------------------------------------
        # AUTOMATIC MEMORY PROCESSING
        # --------------------------------------------------

        try:

            memory_result = process_memories(user_input)

            if memory_result["saved"] > 0:

                console.print(
                    "[green]Personal memory updated.[/green]"
                )

            if memory_result["pending_approval"] > 0:

                console.print(
                    "[yellow]SPAMMER found information "
                    "that may be worth remembering.[/yellow]"
                )

                console.print(
                    "[yellow]Approval functionality will be "
                    "available in the next update.[/yellow]"
                )

        except Exception as memory_error:

            console.print(
                f"[dim]Memory processing skipped: {memory_error}[/dim]"
            )


# --------------------------------------------------
# APPLICATION ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()
