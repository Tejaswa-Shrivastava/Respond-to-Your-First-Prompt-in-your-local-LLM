import requests
import json
import sys

class LocalLLM:
    def __init__(self, base_url: str = "http://127.0.0.1:1234", model: str = "tinyllama"):
        """
        Initialize the Local LLM client.
        
        Args:
            base_url: Base URL of the Local LLM server (default: http://127.0.0.1:1234)
            model: Model name (default: tinyllama)
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        # Using the chat completions endpoint which is more standard
        self.api_url = f"{self.base_url}/v1/chat/completions"
        self.tags_url = f"{self.base_url}/api/tags"
        
    def generate(self, prompt: str, max_tokens: int = 100) -> str:
        """
        Generate text using the Local LLM API.
        
        Args:
            prompt: The input prompt for the model
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated response text
        """
        try:
            print(f"\nSending request to: {self.api_url}")
            print(f"Using model: {self.model}")
            
            headers = {'Content-Type': 'application/json'}
            data = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "stream": False
            }
            
            print("\nRequest data:", json.dumps(data, indent=2))
            
            # Try to make the request directly
            try:
                response = requests.post(
                    self.api_url, 
                    headers=headers, 
                    json=data,
                    timeout=60
                )
            except requests.exceptions.RequestException as e:
                return f"Failed to connect to Local LLM server: {str(e)}\nPlease make sure the Local LLM server is running and the URL is correct."
            
            print(f"\nStatus code: {response.status_code}")
            print("Response headers:", response.headers)
            
            response.raise_for_status()
            
            result = response.json()
            print("\nFull response:", json.dumps(result, indent=2))
            
            # Extract response text from the chat completions response
            if 'choices' in result and len(result['choices']) > 0:
                message = result['choices'][0].get('message', {})
                if 'content' in message:
                    return message['content'].strip()
            
            # Fallback to check other possible response formats
            if 'response' in result:
                return result['response'].strip()
            elif 'message' in result and 'content' in result['message']:
                return result['message']['content'].strip()
            
            return f"Response received but couldn't extract text. Full response: {result}"
            
        except requests.exceptions.RequestException as e:
            return f"Request failed: {str(e)}"
        except json.JSONDecodeError as e:
            return f"Failed to parse JSON response: {str(e)}\nResponse text: {response.text}"
        except Exception as e:
            return f"Unexpected error: {str(e)}\nType: {type(e).__name__}"

def check_local_llm_server(url):
    """Check if Local LLM server is reachable"""
    try:
        response = requests.get(f"{url.rstrip('/')}/api/tags", timeout=5)
        if response.status_code == 200:
            print("✓ Local LLM server is running and accessible")
            try:
                models = response.json().get('models', [])
                if models:
                    print("\nAvailable models:")
                    for model in models:
                        print(f"- {model.get('name', 'Unknown')}")
                else:
                    print("\nNo models found. Make sure to pull the model first.")
            except:
                print("\nCould not parse models list")
            return True
    except Exception as e:
        print(f"✗ Could not connect to Local LLM server: {str(e)}")
        print("\nPlease make sure the Local LLM server is running and accessible at:", url)
        return False

def main():
    # Server and model configuration
    base_url = "http://127.0.0.1:1234"  # Using port 1234 as per your setup
    model = "tinyllama"  # Using TinyLlama model
    
    print(f"\n{'='*50}")
    print("Local LLM API Tester")
    print(f"{'='*50}")
    
    # First check if server is reachable
    if not check_local_llm_server(base_url):
        return
    
    # Initialize the LLM
    print(f"\nInitializing LLM with model: {model}")
    llm = LocalLLM(base_url=base_url, model=model)
    
    # Example prompt
    prompt = "What is the future of AI in healthcare?"
    print(f"\n{'='*50}")
    print("=== Prompt ===")
    print(prompt)
    print(f"{'='*50}")
    
    # Generate response
    print("\nSending request to Local LLM...")
    response = llm.generate(prompt, max_tokens=100)
    
    print(f"\n{'='*50}")
    print("=== Response ===")
    print(response)
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
