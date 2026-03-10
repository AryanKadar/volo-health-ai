import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load explicitly just in case
load_dotenv()

# Singleton client so we don't recreate it on every request
_client = None

def get_client() -> AzureOpenAI:
    global _client
    if _client is None:
        _client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_API_BASE"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION")
        )
    return _client

def call_gpt(messages: list, max_tokens: int, temperature: float) -> tuple[str, dict]:
    """
    Calls Azure OpenAI and returns a tuple: (reply_text, usage_dict)
    """
    client = get_client()
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )
    
    content = response.choices[0].message.content
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens
    }
    
    return content, usage
