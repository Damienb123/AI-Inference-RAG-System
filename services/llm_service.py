# This file supports model calls, prompt formatting, retries of failed task completion, timeout handling, and response parsing

# Current setup is foundational until enhanced

# Goal of the LLM is to queue up and manage upcoming tasks.

from openai import OpenAI
import os
# import your API key here
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_response(prompt):
    response = client.chat.completions.create(
        # Use this particular model for efficiency, quicker parsing, and optimal execution time per task
        model="gpt-3.5-turbo",
        message=[
            {"role": "system", "content": "You are a helpful task manager."},
            {"role": "user", "content": prompt}
        ]
    )
    # Extract the next content from the response object
    return response.choices[0].message.content
# provides output of the queued tasks
print(get_ai_response("What is the next job in the queue?"))