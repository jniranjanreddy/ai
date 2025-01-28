## Lesson-1
## Basics
## pip install openai --quiet

from openai import OpenAI
import os
import json
from datetime import datetime
import pandas as pd




OPENAI_API_KEY=os.getenv("api_key")  # using niruclone key


client = OpenAI(
  api_key=os.getenv(OPENAI_API_KEY)
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=False,
  temperature=1,
  max_tokens=64,
  messages=[
    {"role": "user", "content": "How many years of education does Apple steve jobs have"}
  ]
)

print(completion.choices[0].message);

# print(api_key)
