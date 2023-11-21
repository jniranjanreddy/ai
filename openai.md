## tested in Jupiter Notebook
```
#Python3.8
from openai import OpenAI

config = dotenv_values(".env")

openai.api_key = config["OPENAI_API_KEY"]
#client = OpenAI(api_key="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")

client.completions.create(
    model="text-davinci-003",
    prompt="google inc CEO ")
```
