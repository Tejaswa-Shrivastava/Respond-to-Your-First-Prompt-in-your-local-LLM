import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class LocalLLM:
    def __init__(self, model_name: str = "distilgpt2"):
        """
        Initialize the local LLM with a smaller model.
        """
        self.model_name = model_name
        self.device = "cpu"  # Force CPU to avoid any CUDA issues
        
        print(f"Loading model {model_name} on {self.device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)

    def generate(self, prompt: str, max_tokens: int = 100) -> str:
        """
        Generate text using the model with reduced randomness and repetition.
        
        Args:
            prompt: The input prompt for the model
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated response text
        """
        try:
            # Add padding token if not set
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=len(prompt.split()) + max_tokens,
                    do_sample=True,
                    temperature=0.2,  # Lower temperature for less randomness
                    top_p=0.9,      # Use nucleus sampling to reduce randomness
                    repetition_penalty=2.0,  # Penalize repeated words
                    no_repeat_ngram_size=3,  # Prevent 3-gram repetition
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode and clean the response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the original prompt from the response
            response = response.replace(prompt, "").strip()
            
            return response
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return ""

def main():
    # Initialize the local LLM interface
    llm = LocalLLM()
    
    # Example prompt
    prompt = "What is the future of AI in healthcare?"
    
    print("\n=== Prompt ===")
    print(prompt)
    print("\n=== Response ===")
    
    # Generate response
    response = llm.generate(prompt, max_tokens=100)
    print(response)

if __name__ == "__main__":
    main()
