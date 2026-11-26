# SPAMMER Installation Guide

SPAMMER is a lightweight, offline-first personal AI assistant powered by Python, Ollama and locally running language models.

This guide covers installation on macOS and Windows.

## Prerequisites

Before installing SPAMMER, make sure you have:

- Python 3.10 or newer
- Ollama installed
- Git installed (recommended)
- An internet connection for initial setup and model download

Once the required model is downloaded, SPAMMER can run without an internet connection.

## 1. Download SPAMMER

Clone the repository:

```bash
git clone https://github.com/Sravan2510/SPAMMER.git
cd SPAMMER
```

Alternatively, download the repository as a ZIP file from GitHub and extract it.

## 2. Create a Python virtual environment

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
```

## 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Install Ollama

Download Ollama from:

https://ollama.com/download

Install the version suitable for your operating system.

## 5. Download the AI model

SPAMMER currently uses:

```bash
ollama pull qwen3.5:4b
```

This download requires an internet connection and sufficient disk space.

## 6. Start SPAMMER

Make sure Ollama is running, activate your virtual environment, and execute:

```bash
python main.py
```

## Offline usage

After installing Ollama and downloading the model, SPAMMER can operate locally without an internet connection, provided the Ollama service and downloaded model are available.

## Troubleshooting

### Python is not recognized

Check your Python installation and PATH configuration.

### Ollama connection error

Make sure Ollama is installed and running.

### Model not found

Run:

```bash
ollama pull qwen3.5:4b
```

### Missing Python modules

Activate the virtual environment and run:

```bash
python -m pip install -r requirements.txt
```

## Privacy

SPAMMER is designed to process conversations using a locally running model. Conversation history and personal memory are stored in a local SQLite database.

Do not assume that local storage automatically protects data from other users or applications with access to your computer.
