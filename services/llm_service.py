#LLM service to handle prompt formatting, model calling, and response parsing

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# import your API key here
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(message: str, context: str = "") -> str:
    prompt = f"""

    You are a helpful assistant.

    Context:
    {context}

    User message:
    {message}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        message = [
            {"role": "user", "content": prompt}
        ],
        temperature=2.0
    )
      
    # Extract the next content from the response object
    return response.choices[0].message.content
