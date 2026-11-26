# SPAMMER

### Your Personal AI Companion & Research Assistant

SPAMMER is a lightweight, locally running, Python-based AI assistant designed to answer questions, support programming and learning, and retain useful information across conversations.

It uses **Ollama** to run a language model locally, **Qwen 3.5 4B** as its configured model, **SQLite** for conversation and memory storage, and **Rich** for a formatted terminal interface.

> **Project status — 26 November 2026:** The local chat foundation, conversation persistence, hybrid memory extraction, and interactive memory-management commands have been implemented. Basic code generation has also been tested through normal chat. A dedicated Code Assistant Mode, automatic code-file creation, and controlled code execution are not yet implemented.

---

## Table of contents

1. [What SPAMMER is designed to do](#1-what-spammer-is-designed-to-do)
2. [Technology stack](#2-technology-stack)
3. [How the application works](#3-how-the-application-works)
4. [Project structure](#4-project-structure)
5. [Database and memory design](#5-database-and-memory-design)
6. [Current capabilities](#6-current-capabilities)
7. [Setup and prerequisites](#7-setup-and-prerequisites)
8. [Installation guide](INSTALLATION.md)
9. [Run SPAMMER](#9-run-spammer)
10. [Available terminal commands](#10-available-terminal-commands)
11. [Useful development commands](#11-useful-development-commands)
12. [Current limitations](#12-current-limitations)
13. [Development roadmap](#13-development-roadmap)
14. [Privacy and local data](#14-privacy-and-local-data)

---

## 1. What SPAMMER is designed to do

SPAMMER is intended to be a friendly personal AI companion and practical offline-first assistant.

The current project scope focuses on:

- Answering general questions using a locally hosted language model.
- Explaining programming concepts and generating code.
- Helping with simple debugging and technical learning.
- Retaining conversation history between application runs.
- Remembering useful preferences, interests and project details.
- Retrieving saved memories as context in later conversations.
- Giving the user control over memory approval, rejection and deletion.
- Remaining useful when the internet connection is unreliable.

SPAMMER is a side project. Its development is intentionally incremental and practical. Advanced agents, cloud deployment, enterprise architecture and complex retrieval systems are outside the immediate SPAMMER 1.0 scope.

## 2. Technology stack

| Technology | Role in SPAMMER |
|---|---|
| Python | Main application language and control logic |
| Ollama | Runs the language model locally |
| Qwen 3.5 4B | Configured language model |
| `ollama` Python package | Sends chat requests to Ollama and receives responses |
| SQLite | Stores conversations, permanent memories and memory candidates |
| Rich | Formats the terminal interface |
| JSON | Structures memory-extraction results |

### Understanding the main components

**Python — Application controller**

Python runs the application. It receives user input, prepares conversation and memory context, calls the model, processes memory suggestions, saves messages and displays responses.

**Ollama — Local model runner**

Ollama manages and runs the selected language model on the computer. The Python application communicates with it through the Ollama Python package.

**Qwen 3.5 4B — Language model**

Qwen processes the prompt and generates the response. Python and Ollama handle application control and local model execution.

**SQLite — Persistent storage**

SQLite stores application data in the local database file `spammer_memory.db`.

**Rich — Terminal presentation**

Rich improves terminal readability through formatted text and panels.

## 3. How the application works

### Current chat flow

```text
User enters a message
        |
        v
Python receives the input
        |
        v
Check whether it is a local command
        |
        +-----------------------------+
        |                             |
        v                             v
Run command locally             Continue chat
                                      |
                                      v
                         Prepare system instructions,
                         recent conversation and memories
                                      |
                                      v
                         Send chat request through
                         the Ollama Python package
                                      |
                                      v
                         Ollama runs Qwen locally
                                      |
                                      v
                         Python receives the response
                                      |
                         +------------+------------+
                         |                         |
                         v                         v
                  Save assistant reply       Display with Rich
                  in SQLite                  in the terminal
                         |
                         v
                  Process the user's message
                  for possible useful memories
```

The application saves the user's message before sending the model request and saves the assistant response after a successful response.

### Current hybrid memory flow

```text
User message
     |
     v
Qwen analyses the message for useful information
     |
     v
Return structured JSON suggestions
     |
     v
Python validates the response and applies memory rules
     |
     +-------------------------+-------------------------+
     |                         |                         |
     v                         v                         v
 Low-risk information   Needs user approval       Sensitive/blocked
     |                         |                         |
     v                         v                         v
Save to permanent       Save as pending            Discard
personal memory         candidate
                              |
                              v
                     User reviews the candidate
                              |
                       +------+------+
                       |             |
                       v             v
                    Approve        Reject
                       |             |
                       v             v
                Save permanently   Do not add to
                                   permanent memory
```

The current implementation uses Qwen for extraction and Python rules for validation and risk handling. Sensitive-information detection is based on a limited keyword list and is not a comprehensive guarantee.

## 4. Project structure

The public project files are organized as follows:

```text
SPAMMER/
├── main.py
├── memory.py
├── memory_extractor.py
├── test_memory.py
├── requirements.txt
├── README.md
├── INSTALLATION.md
└── .gitignore
```

| File | Description |
|---|---|
| `main.py` | Main application, terminal chat loop and command handling |
| `memory.py` | SQLite database setup, conversation functions and memory operations |
| `memory_extractor.py` | Qwen-powered memory extraction, validation and hybrid memory processing |
| `test_memory.py` | Test file for memory-related functionality |
| `requirements.txt` | Python dependency list |
| `README.md` | Project overview, architecture, capabilities and development information |
| `INSTALLATION.md` | Installation instructions for macOS and Windows |
| `.gitignore` | Excludes local files and other files that should not be committed |

### Local development files

The following files and folders may exist in a developer's local copy but are not part of the public application structure:

- `.venv/` — Python virtual environment.
- `.idea/` — IntelliJ IDEA project settings.
- `spammer_memory.db` — Local SQLite database.
- `main_backup.py` and `memory_backup.py` — Local backup copies.
- `SPAMMER.iml` — IntelliJ IDEA module file.

These files are not required to be included in the public repository.

## 5. Database and memory design

SPAMMER uses SQLite. The database file is:

```text
spammer_memory.db
```

The database contains three tables.

### 5.1 `conversations`

Stores messages exchanged with SPAMMER.

| Column | Meaning |
|---|---|
| `id` | Unique, automatically generated message ID |
| `role` | Sender role, such as `user` or `assistant` |
| `content` | Message text |
| `timestamp` | When the message was stored |

Related functions:

- `save_message(role, content)` — stores a message.
- `get_recent_messages(limit=20)` — retrieves recent messages.

### 5.2 `personal_memory`

Stores accepted, persistent memories.

| Column | Meaning |
|---|---|
| `id` | Unique memory ID |
| `category` | Memory category, such as `Project` or `Preference` |
| `information` | Information being remembered |
| `created_at` | When the memory was saved |

Related functions:

- `save_memory(category, information)` — adds a permanent memory.
- `get_all_memories()` — retrieves saved memories.
- `get_memories_with_ids()` — retrieves saved memories with their IDs.
- `delete_memory(memory_id)` — deletes a permanent memory by ID.

Example memory categories include:

- Preferences
- Projects
- Learning interests
- Skills

The examples above describe possible categories, not actual user records.

### 5.3 `memory_candidates`

Stores possible memories before they are accepted into permanent memory.

| Column | Meaning |
|---|---|
| `id` | Unique candidate ID |
| `category` | Proposed memory category |
| `information` | Proposed memory content |
| `risk_level` | Classification attached to the candidate |
| `status` | Workflow state |
| `created_at` | When the candidate was created |

Candidate statuses:

- `pending` — awaiting a decision.
- `approved` — accepted and processed.
- `rejected` — declined and not copied to permanent memory.

Related functions:

- `save_memory_candidate(category, information, risk_level)`
- `get_pending_candidates()`
- `approve_memory_candidate(candidate_id)`
- `reject_memory_candidate(candidate_id)`

### Why have memory candidates?

A candidate is a temporary holding area for information that may be worth remembering. This prevents every sentence in a conversation from becoming a permanent memory and gives the user control over information that needs confirmation.

### Hybrid memory policy

| Type of information | Handling |
|---|---|
| Ordinary preferences and learning interests | Eligible for automatic saving |
| Skills and project details | Eligible for automatic saving |
| Important personal decisions and major changes | Ask for approval |
| Sensitive information | Block from memory processing |

Python applies additional rules rather than relying only on the model's risk classification. The current sensitive-information keyword list is limited; it cannot guarantee detection of every sensitive detail.

### Duplicate handling

The current duplicate checks compare category and information using trimmed, case-insensitive exact matching. They do not perform semantic matching and do not automatically detect duplicates across different categories.

## 6. Current capabilities

The following capabilities have been implemented:

- [x] Python virtual environment and local project setup.
- [x] Ollama integration.
- [x] Qwen 3.5 4B configured for chat.
- [x] Terminal chat interface using Rich.
- [x] SQLite database initialization.
- [x] Conversation message saving and recent-message retrieval.
- [x] Permanent memory saving and retrieval.
- [x] Memory-candidate creation and retrieval.
- [x] Qwen-powered memory extraction.
- [x] Python validation and memory-risk handling.
- [x] Automatic saving of eligible low-risk memories.
- [x] Pending candidates for information requiring approval.
- [x] Candidate approval and rejection.
- [x] Exact-match duplicate checks.
- [x] Memory listing with IDs.
- [x] Memory deletion with confirmation.
- [x] `help` command.
- [x] Basic general-question and programming/code-generation tests.

### Code generation test

SPAMMER has generated a Python example that creates an SQLite database and a `students` table. The generated example included:

- Importing `sqlite3`.
- Connecting to a database file.
- Creating the `students` table if it does not already exist.
- Defining `id`, `name`, `age` and `grade` columns.
- Executing the SQL statement, committing and closing the connection.

This verifies code generation through normal chat. It does not mean SPAMMER can automatically save, execute or validate generated code.

### Interactive memory commands tested

The following workflows were tested through the running application:

- `memories` displayed saved memories and their IDs.
- `pending` displayed pending candidates.
- `approve` successfully approved a temporary test candidate.
- `reject` successfully rejected a temporary test candidate.
- `delete` requested confirmation and successfully deleted a temporary test memory.
- `help` displayed the available commands.
- `exit` closed the application normally.

Temporary test records were used to verify the memory-management workflows.

## 7. Setup and prerequisites

The current development environment:

- macOS on a MacBook Pro M4 with 16 GB unified memory.
- Python 3.14.2.
- IntelliJ IDEA.
- Ollama installed locally.
- Qwen 3.5 4B available in Ollama.

The project uses a Python virtual environment named `.venv`.

### Create a virtual environment (if setting up from scratch)

From the project root:

```bash
python3 -m venv .venv
```

### Activate the environment

On macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

The terminal prompt should begin with `(.venv)` when the environment is active.

### Install Python packages

```bash
python -m pip install -r requirements.txt
```

### Confirm Ollama and the model are available

Check the Ollama installation:

```bash
ollama --version
```

Check available local models:

```bash
ollama list
```

The configured model identifier is:

```text
qwen3.5:4b
```

If it is not already available locally, obtain it with:

```bash
ollama pull qwen3.5:4b
```

Ollama must be running for SPAMMER to generate model responses.

For complete installation instructions covering macOS and Windows, see the [SPAMMER Installation Guide](INSTALLATION.md).

## 8. Installation guide

New users should follow the separate installation guide:

**[Read the SPAMMER Installation Guide](INSTALLATION.md)**

It covers:

- Downloading the project.
- Creating a Python virtual environment.
- Installing Python dependencies.
- Installing Ollama.
- Downloading the configured AI model.
- Starting SPAMMER.
- Basic troubleshooting.

## 9. Run SPAMMER

Open the SPAMMER project in a terminal or in IntelliJ IDEA.

Activate the virtual environment if necessary.

On macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Run the application:

```bash
python main.py
```

To exit the chat, enter:

```text
exit
```

or:

```text
quit
```

### IntelliJ interpreter note

Configure the project interpreter to use the Python executable inside the project's `.venv` directory.

On macOS, the path is:

```text
<project-folder>/.venv/bin/python
```

On Windows, the path is:

```text
<project-folder>\.venv\Scripts\python.exe
```

## 10. Available terminal commands

Enter these commands at the SPAMMER prompt:

| Command | Description |
|---|---|
| `help` | Display available commands |
| `memories` | View saved personal memories |
| `pending` | View pending memory approvals |
| `approve` | Review and approve a pending candidate |
| `reject` | Review and reject a pending candidate |
| `delete` | Select and delete a saved memory after confirmation |
| `exit` / `quit` | Close SPAMMER |

These are local application commands. They are handled by Python and are not sent to Qwen as ordinary chat messages.

## 11. Useful development commands

Run these from the project root with `.venv` activated.

| Purpose | Command |
|---|---|
| Activate virtual environment (macOS) | `source .venv/bin/activate` |
| Activate virtual environment (Windows) | `.venv\Scripts\activate` |
| Run SPAMMER | `python main.py` |
| Install dependencies | `python -m pip install -r requirements.txt` |
| Check dependencies | `python -m pip check` |
| Compile main application | `python -m py_compile main.py` |
| Compile memory modules | `python -m py_compile memory.py memory_extractor.py` |
| List Ollama models | `ollama list` |
| Check Ollama version | `ollama --version` |

## 12. Current limitations

SPAMMER is a working local assistant, but some capabilities are not yet implemented:

1. **No dedicated Code Assistant Mode:** Programming requests are currently handled through normal conversation.
2. **No automatic code-file creation:** SPAMMER can generate code in its response, but it does not yet save generated code into `.py`, `.html`, `.css` or other project files.
3. **No controlled code execution:** SPAMMER does not yet run generated code and capture its output or errors.
4. **No execution-verified debugging:** It can explain code and reason about pasted errors, but it cannot independently reproduce and verify a fix by executing the program.
5. **Basic sensitive-information detection:** The current keyword-based safeguard is limited and should not be treated as comprehensive.
6. **Exact-match duplicate detection:** Semantically similar memories and duplicates across different categories are not comprehensively handled.
7. **No dedicated memory-editing workflow:** There is no complete workflow for safely updating an existing memory.
8. **Simple context management:** Conversation history uses a recent-message limit rather than advanced token budgeting.
9. **Generated-code safety:** Generated code should be reviewed before execution. Any future execution feature must use a controlled approach rather than blindly running arbitrary model output.

## 13. Development roadmap

The roadmap is intentionally small and focused on a useful SPAMMER 1.0.

### Completed

- [x] Local Python application connected to Ollama.
- [x] Qwen-powered terminal chat.
- [x] Rich terminal formatting.
- [x] SQLite conversation history.
- [x] Persistent personal memory storage.
- [x] Qwen-powered memory extraction.
- [x] Hybrid memory processing and Python-side risk handling.
- [x] Memory approval and rejection.
- [x] Memory listing and deletion with confirmation.
- [x] Help command.
- [x] Basic general-question and code-generation tests.

### Next milestone — Code Assistant Mode

The next development focus is to make coding assistance more useful while keeping the implementation local and simple.

Planned work:

1. Improve prompts for code generation and simple debugging.
2. Allow SPAMMER to save generated code to a user-selected file.
3. Add a deliberate, controlled way to run code when requested.
4. Capture execution output and errors.
5. Let SPAMMER explain errors and suggest corrections.
6. Test with small Python programs before considering broader project support.

Code generation, file creation and code execution are separate capabilities. The first milestone should focus on generating and saving code; controlled execution can follow after that works reliably.

### Later, only if useful

- Improve memory editing and cross-category duplicate handling.
- Improve conversation context management.
- Add support for creating small multi-file projects.
- Improve automated tests and error handling.
- Complete clean-install testing on supported operating systems.

Advanced agents, cloud deployment, RAG and a graphical interface are not immediate priorities.

## 14. Privacy and local data

SPAMMER is designed as a local-first assistant.

The current chat model runs through Ollama on the user's computer, and application memory is stored in the local SQLite database.

Important considerations:

- The database contains conversation and personal information; protect it like other personal files.
- Do not store passwords, API keys, financial credentials or other secrets as memories.
- Keep backups of important project and database files.
- Review pending memory candidates before approving information that needs confirmation.
- Generated code should be reviewed before execution.
- Future integrations such as web research or external services may involve network communication; assess their privacy implications separately.

Local model execution and local SQLite storage do not, by themselves, guarantee that every future feature will remain offline. Review each new integration before enabling it.

---

## Project status summary

**Implemented:** Local chat foundation, Ollama/Qwen integration, Rich terminal interface, SQLite conversation history, persistent personal memory, hybrid memory extraction and risk handling, interactive memory approval/rejection/listing/deletion, help command and basic code generation.

**Next:** Build Code Assistant Mode, beginning with improved code generation and saving generated code to files.

**Not yet implemented:** Automatic code-file creation, controlled code execution and execution-result-based debugging.

SPAMMER is more than a basic local chatbot. It has a working conversational foundation, persistent memory and interactive memory management. The next practical milestone is to make its coding assistance more useful without making the project unnecessarily complicated.