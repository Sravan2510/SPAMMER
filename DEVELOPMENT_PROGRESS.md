# SPAMMER — DEVELOPMENT PROGRESS

**Last Updated:** 20 November 2026  
**Project:** SPAMMER — Personal AI Companion & Research Assistant  
**Current Version:** SPAMMER 1.0 (In Development)  
**Development Status:** Core functionality implemented; Code Assistant Mode is the next milestone.

---

## 1. Project Overview

SPAMMER is a lightweight, locally running AI assistant developed using Python, Ollama, Qwen 3.5 4B and SQLite.

The primary objective is to build a personal AI companion that can:

- Answer general questions locally.
- Explain programming concepts.
- Generate code and help with simple debugging.
- Remember useful personal information.
- Maintain conversation history.
- Work when the internet connection is unreliable.

SPAMMER is a side project. The development approach is to build useful features incrementally without introducing unnecessary complexity.

---

## 2. Development Environment

| Component | Current Configuration |
|---|---|
| Computer | MacBook Pro M4 |
| Memory | 16 GB Unified Memory |
| Operating System | macOS |
| IDE | IntelliJ IDEA |
| Programming Language | Python 3.14.2 |
| Virtual Environment | `.venv` |
| Local Model Runner | Ollama 0.40.16 |
| AI Model | Qwen 3.5 4B |
| Python Ollama Package | 0.6.3 |
| Terminal Interface | Rich 15.0.0 |
| Database | SQLite |

### Project Location

```text
/Users/sravankumar/Desktop/IntellIJ IDEA/SPAMMER
```

### Python Environment

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the application:

```bash
python main.py
```

---

## 3. Project Structure

The following project files have been identified during development:

```text
SPAMMER/
│
├── .idea/
├── .venv/
│
├── main.py
├── main_backup.py
│
├── memory.py
├── memory_backup.py
│
├── memory_extractor.py
│
├── spammer_memory.db
│
├── test_memory.py
│
└── SPAMMER.iml
```

### File Responsibilities

| File | Responsibility |
|---|---|
| `main.py` | Main application, chat loop and terminal commands |
| `memory.py` | SQLite database operations and memory management |
| `memory_extractor.py` | AI-powered memory extraction and validation |
| `spammer_memory.db` | Persistent application database |
| `test_memory.py` | Memory testing |
| `main_backup.py` | Backup of main application |
| `memory_backup.py` | Backup of memory module |
| `.venv/` | Python virtual environment |

---

## 4. Completed Development Milestones

### Milestone 1 — Project Setup

<badge>COMPLETED</badge>

- [x] Created SPAMMER project.
- [x] Configured Python virtual environment.
- [x] Installed Ollama.
- [x] Installed the Ollama Python package.
- [x] Installed Rich.
- [x] Downloaded and configured Qwen 3.5 4B.
- [x] Verified local model communication.

### Milestone 2 — Basic AI Chat

<badge>COMPLETED</badge>

- [x] Connected Python application to Ollama.
- [x] Configured Qwen 3.5 4B.
- [x] Created the main chat loop.
- [x] Implemented user input handling.
- [x] Implemented AI response generation.
- [x] Added Rich terminal formatting.
- [x] Added application exit handling.

**Result:** SPAMMER can communicate with the locally running language model and answer general questions.

### Milestone 3 — SQLite Conversation History

<badge>COMPLETED</badge>

Implemented SQLite-based conversation persistence.

Created the `conversations` table.

Implemented:

- [x] `initialize_memory()`
- [x] `save_message(role, content)`
- [x] `get_recent_messages(limit=20)`

**Result:** SPAMMER can save conversations and retrieve recent messages for context.

### Milestone 4 — Permanent Personal Memory

<badge>COMPLETED</badge>

Created the `personal_memory` table.

Implemented:

- [x] `save_memory(category, information)`
- [x] `get_all_memories()`
- [x] `get_memories_with_ids()`
- [x] `delete_memory(memory_id)`

**Result:** SPAMMER can store, retrieve and delete persistent personal memories.

### Milestone 5 — Memory Candidate System

<badge>COMPLETED</badge>

Created the `memory_candidates` table.

Implemented:

- [x] `save_memory_candidate(category, information, risk_level)`
- [x] `get_pending_candidates()`
- [x] `approve_memory_candidate(candidate_id)`
- [x] `reject_memory_candidate(candidate_id)`

**Result:** Potential memories can be held for user approval before being added to permanent memory.

### Milestone 6 — AI-Powered Memory Extraction

<badge>COMPLETED</badge>

Created `memory_extractor.py`.

Integrated Qwen 3.5 4B into the memory extraction workflow.

Implemented:

- [x] Memory extraction prompt.
- [x] JSON-based extraction response.
- [x] Existing-memory context.
- [x] Memory category identification.
- [x] Risk classification.
- [x] Sensitive-information keyword checks.
- [x] Python-side memory validation.
- [x] Duplicate detection.
- [x] Automatic processing of low-risk memories.
- [x] Pending candidates for approval-required memories.

Main functions:

```python
extract_memories(user_message)

process_memories(user_message)

contains_sensitive_information(information)

determine_memory_risk(category, information, model_risk)
```

**Result:** SPAMMER can identify potentially useful information from conversations and process it according to the current memory rules.

### Milestone 7 — Interactive Memory Management

<badge>COMPLETED</badge>

Integrated memory-management functions into `main.py`.

Implemented the following terminal commands:

| Command | Functionality |
|---|---|
| `help` | Displays available commands |
| `memories` | Displays saved memories |
| `pending` | Displays pending memory candidates |
| `approve` | Approves a candidate |
| `reject` | Rejects a candidate |
| `delete` | Deletes a saved memory after confirmation |
| `exit` | Closes SPAMMER |
| `quit` | Closes SPAMMER |

Additional functions implemented in `main.py`:

```python
show_memories()

show_pending_candidates()

approve_memory()

reject_memory()

remove_memory()

show_help()
```

**Result:** Users can manage their saved memories directly through the terminal without manually modifying the database.

### Milestone 8 — Duplicate Memory Prevention

<badge>COMPLETED</badge>

Implemented:

```python
memory_exists(category, information)

candidate_exists(category, information)
```

Current duplicate checks:

- [x] Check existing permanent memories.
- [x] Check pending candidates.
- [x] Ignore differences in letter casing.
- [x] Ignore leading and trailing whitespace.
- [x] Prevent repeated exact-match memory extraction.
- [x] Check for an existing memory before approving a candidate.

**Current limitation:** Duplicate detection is based on exact matching within the same category. Semantic duplicates and cross-category duplicates are not comprehensively handled.

### Milestone 9 — Code Generation Test

<badge>TESTED</badge>

Tested SPAMMER's ability to generate programming code through normal chat.

Test questions included:

1. What is Python, and what are three practical things I can build with it?
2. Write a simple Python program that creates an SQLite database and a table called students. Explain the code step by step.

SPAMMER successfully generated a Python example using:

- `sqlite3`
- Database connection.
- SQL table creation.
- `CREATE TABLE IF NOT EXISTS`.
- Student table columns.
- Database commit and connection closing.
- Step-by-step explanation.

**Result:** Basic code generation through normal conversation works.

**Important:** Code generation has been tested, but automatic file creation, code execution and execution-based debugging have not yet been implemented.

---

## 5. Current Database Status

Database file:

```text
spammer_memory.db
```

Current database tables:

```text
conversations
personal_memory
memory_candidates
```

### Permanent Memories

The latest verified database state contains six permanent memories:

| ID | Category | Information |
|---:|---|---|
| 1 | Project | Favourite project is Virtual AYUSH Herbal Garden |
| 2 | Preference | Prefers step-by-step explanations |
| 3 | Preference | Prefers learning Python through practical coding examples |
| 5 | Projects | Changing career direction to AI engineering |
| 6 | Preference | Enjoys building small applications using Python and SQLite |
| 7 | Projects | Enjoys building small applications using Python and SQLite |

**Known observation:** IDs 6 and 7 contain the same information under different categories. This is a cross-category duplicate and remains unchanged.

### Memory Candidate Status

At the last verification:

- No pending candidates.
- One rejected test candidate remains in the database.
- The temporary deletion-test memory was successfully deleted.
- The six original permanent memories remained intact.

---

## 6. Testing and Verification

The following functionality has been tested during development.

| Test | Result |
|---|---|
| Python application starts | Passed |
| Ollama communication | Passed |
| Qwen response generation | Passed |
| General questions | Passed |
| SQLite initialization | Passed |
| Conversation saving | Passed |
| Permanent memory saving | Passed |
| Permanent memory retrieval | Passed |
| Memory extraction | Passed |
| Low-risk automatic memory saving | Passed |
| Approval candidate creation | Passed |
| Candidate approval | Passed |
| Candidate rejection | Passed |
| Duplicate exact-match prevention | Passed |
| Memory listing | Passed |
| Memory deletion with confirmation | Passed |
| Help command | Passed |
| Basic programming code generation | Passed |
| Automatic generated-code execution | Not implemented |
| Automatic generated-code file creation | Not implemented |

### Python Compilation Checks

The following compilation check passed during development:

```bash
python -m py_compile main.py
```

Compilation checks were also used while developing the memory modules.

---

## 7. Current Application Capabilities

SPAMMER currently supports:

1. Local AI conversations.
2. General question answering.
3. Programming explanations.
4. Basic code generation.
5. SQLite conversation persistence.
6. Persistent personal memories.
7. AI-powered memory extraction.
8. Automatic saving of eligible low-risk memories.
9. Memory approval and rejection.
10. Memory listing and deletion.
11. Interactive terminal commands.
12. Recent conversation context.

The application is designed to use a locally available model through Ollama. Its core chat functionality does not require a cloud AI API, although Ollama must be running locally.

---

## 8. Current Limitations

The following features are not yet implemented:

### 1. Dedicated Code Assistant Mode

Programming questions currently use the normal chat interface.

A dedicated mode with specialized coding instructions is planned.

### 2. Automatic Code File Creation

SPAMMER can generate code in its response but cannot yet automatically save it to a selected file.

Planned support:

- `.py`
- `.html`
- `.css`
- `.js`
- `.sql`
- Other common development file types.

### 3. Controlled Code Execution

SPAMMER cannot yet execute generated Python programs and return their actual output.

### 4. Execution-Based Debugging

SPAMMER can explain pasted errors and suggest corrections, but it cannot independently execute code to verify a fix.

### 5. Improved Memory Management

Future improvements may include:

- Editing existing memories.
- Better duplicate detection.
- Cross-category duplicate handling.
- Improved sensitive-information detection.

### 6. Better Conversation Context

The current implementation retrieves recent messages using a message limit. More advanced context and token management are not yet implemented.

---

## 9. Simplified Development Roadmap

The project will continue with a practical, lightweight approach.

### Phase 1 — Local AI Foundation

<badge>COMPLETED</badge>

- [x] Python project setup.
- [x] Ollama integration.
- [x] Qwen 3.5 4B.
- [x] Rich terminal interface.
- [x] General question answering.

### Phase 2 — Persistent Memory

<badge>COMPLETED</badge>

- [x] SQLite database.
- [x] Conversation history.
- [x] Permanent memories.
- [x] Memory candidates.
- [x] AI memory extraction.
- [x] Memory approval and rejection.
- [x] Memory deletion.
- [x] Duplicate exact-match checks.

### Phase 3 — Code Assistant Mode

<badge color="info">NEXT MILESTONE</badge>

Planned tasks:

- [ ] Introduce a dedicated coding mode.
- [ ] Improve code-generation prompts.
- [ ] Generate complete, structured code examples.
- [ ] Explain generated code step by step.
- [ ] Allow generated code to be saved into files.
- [ ] Add controlled code execution.
- [ ] Capture program output and errors.
- [ ] Improve debugging through execution feedback.

### Phase 4 — Reliability and Improvements

Planned tasks:

- [ ] Improve error handling.
- [ ] Improve memory management.
- [ ] Improve duplicate detection.
- [ ] Add tests for important application functions.
- [ ] Improve conversation context management.
- [ ] Review database backup and recovery.

### Future Possibilities

Only if required:

- [ ] Small multi-file project generation.
- [ ] More advanced document handling.
- [ ] Optional web-assisted research.
- [ ] Additional useful local tools.

Advanced agents, RAG, cloud deployment and enterprise-level architecture are not immediate priorities.

---

## 10. Immediate Next Development Task

### Code Assistant Mode — First Implementation

The next session should begin by improving SPAMMER's programming assistance.

Recommended implementation order:

**Step 1:** Review the current `main.py` chat loop and system prompt.

**Step 2:** Introduce a simple coding mode without breaking normal chat.

**Step 3:** Test Python code generation with practical examples.

**Step 4:** Add the ability to save generated code into a `.py` file.

**Step 5:** Verify that the generated file contains the correct code.

**Step 6:** Consider controlled execution only after file creation works reliably.

Development should continue incrementally, with each feature tested before moving forward.

---

## 11. Important Development Principles

The following principles should guide future development:

1. Keep SPAMMER lightweight.
2. Prefer simple Python implementations.
3. Continue using the existing project structure.
4. Preserve the working SQLite memory system.
5. Avoid unnecessary dependencies.
6. Test each new feature before adding another.
7. Do not execute generated code without explicit user approval and appropriate safeguards.
8. Keep local model operation as the default.
9. Maintain backups before major modifications.
10. Do not introduce complex architecture unless there is a clear practical need.

---

## 12. Current Development Summary

**SPAMMER has successfully progressed from a basic local chatbot into a personal AI assistant with persistent conversation history, hybrid memory management and basic code-generation capabilities.**

### Completed

- Local AI chat.
- Ollama and Qwen integration.
- Rich terminal interface.
- SQLite database.
- Conversation history.
- Persistent personal memories.
- AI memory extraction.
- Memory approval and rejection.
- Memory deletion.
- Interactive terminal commands.
- Basic code generation.

### Current Focus

**Code Assistant Mode.**

The immediate goal is to make SPAMMER useful for small programming tasks by improving code generation and adding the ability to save generated code into files.

### Overall Direction

Build a simple, reliable, offline-first personal AI assistant that can answer questions, help with programming and remember useful information.

The priority is practical functionality, not unnecessary complexity.

---

**End of Development Progress Report**

**Last verified project status: 20 November 2026.**