#LLM service to handle prompt formatting, model calling, and response parsing
# Dependencies imports for LLM generation
from openai import OpenAI
import openai
import os
import time
from dotenv import load_dotenv
from services.cache_service import build_cache_key, get_or_set_cache
from tenacity import retry, wait_exponential, stop_after_attempt

# load env variables securely
load_dotenv()

# import your API key here
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0.7
LLM_CACHE_TTL_SECONDS = int(os.getenv("LLM_CACHE_TTL_SECONDS", os.getenv("CACHE_TTL_SECONDS", "3600")))

# LLM generation error handling | prompt generation errors, instruction following, retries for rate limit constraints

# Exponential backoff given 2 retries for API call failures
# Currently uses basic implementation to test, can use 
# jitter after to prevent retry storms
@retry(
        wait=wait_exponential(multiplier=1, min=2, max=60),
        stop=stop_after_attempt(5)
)

def call_llm_api(prompt):
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=LLM_TEMPERATURE
    )
    return response.choices[0].message.content

# response generation handled with given AI context of task and type of user message provided
def generate_response(message: str, context: str = "", retries=3) -> str:
    cache_key = build_cache_key(
        "llm_response",
        {
            "message": message,
            "context": context,
            "model": LLM_MODEL,
            "temperature": LLM_TEMPERATURE,
        },
    )

    return get_or_set_cache(
        cache_key,
        lambda: _generate_response_uncached(message, context=context, retries=retries),
        ttl_seconds=LLM_CACHE_TTL_SECONDS,
    )


def _generate_response_uncached(message: str, context: str = "", retries=3) -> str:

    for attempt in range(retries):
        try:
            prompt = f"""

    You are a helpful assistant.

    Context:
    {context}

    User message:
    {message}
    """
            # gpt-4o-mini is used to for simplicity and lower cost of token usage for testing
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages = [
                    {"role": "user", "content": prompt}
                ],
                # temperature value can be adjusted for specifications
                temperature=LLM_TEMPERATURE
            )
            
            # Extract the next content from the response object
            return response.choices[0].message.content
        
        # Rate limit error handling
        except openai.RateLimitError:
            wait_time = 2 ** attempt
            print(f"Rate Limited. Retrying in {wait_time}s...")
            time.sleep(wait_time)
