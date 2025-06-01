# Local LLM Interface

This script provides a simple interface to interact with a local language model for text generation.

## Prerequisites

- Python 3.7 or higher
- PyTorch
- Transformers library
- Accelerate library

## Installation

1. First, install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python local_llm.py
```

2. The script will initialize a language model and generate text based on the provided prompt.

## Customization

You can customize the following parameters:

1. Model selection:
   - Default: `distilgpt2` (smaller, faster model)
   - Change the model by modifying the `model_name` parameter in the `LocalLLM` class initialization

2. Generation parameters:
   - `max_tokens`: Maximum number of tokens to generate (default: 100)
   - The script automatically handles temperature and repetition penalties for better output quality

## Example Output

The script will display both the input prompt and the generated response in a clear format:
```
=== Prompt ===
[Your prompt here]

=== Response ===
[Generated text here]
```

## Notes

- The script runs on CPU by default to avoid any CUDA-related issues
- The model generates text with reduced randomness and repetition
- Feel free to modify the prompt in the `main()` function to generate different types of text
