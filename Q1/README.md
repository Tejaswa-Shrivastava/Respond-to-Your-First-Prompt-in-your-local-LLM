# Local LLM Interface

This script provides a simple interface to interact with a local language model (TinyLlama) for text generation.

## Prerequisites

- Python 3.7 or higher
- Ollama or tinylama installed and running locally
- Required Python packages: `requests`

## Installation

1. First, install the required dependencies:
```bash
pip install requests
```

2. Make sure Ollama is installed and running on your system

## Usage

1. Start the Ollama server (if not already running)
2. Run the script:
```bash
python local_llm.py
```

2. The script will connect to your local LLM server and generate text based on the provided prompt.

## Customization

You can customize the following parameters:

1. Model selection:
   - Default: `tinyllama` (small, efficient model)
   - Change the model by modifying the `model` parameter in the `main()` function

2. Server configuration:
   - Default server URL: `http://127.0.0.1:1234`
   - Update the `base_url` in the `main()` function if your server is running on a different address/port

3. Generation parameters:
   - `max_tokens`: Maximum number of tokens to generate (default: 100)
   - `temperature`: Controls randomness (default: 0.7)

## Example Output

The script will display both the input prompt and the generated response in a clear format:
```
==================================================
=== Prompt ===
[Your prompt here]
==================================================

=== Response ===
[Generated text here]
==================================================
```

## Notes

- The script connects to a local Ollama server
- The default model is TinyLlama, but you can use any model supported by your Ollama installation
- You can modify the prompt in the `main()` function to generate different types of text
- For best performance, ensure your system meets the requirements for running the selected model
