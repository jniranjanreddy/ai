# Create  

## 1. install Requirements
from langchain_openai import OpenAI
import os

from dotenv import load_dotenv
import langchain
load_dotenv


## 2. Set the OpenAI API Key
openai_key = os.getenv("api_key")  # using niruclone key
OpenAI.api_key = openai_key

## 3. Define youe LLM.
#llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo-instruct", openai_api_key=openai_key)
llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_key)



## 4. Set your Grocery list
list_of_groceries = "tomatoes, yogurt, chicked, cheese, onions, rice, potatoes"


## 5. Create Template
template = """
   please generate a delicious recipe based on the groceries I have available.
   Here's the list of groceries: [{groceries}].
   Create a recipe that incorporates these ingredients and provides
   clear instructions on how to prepare the dish

"""

## 6. Create the promptTemplate using the Template we've Given you.
from langchain import PromptTemplate

prompt = PromptTemplate(
    input_variables=["groceries"],
    template=template
)

## 7. Create your Prompt Template by Passin g it Your List Of Groceries
final_prompt = prompt.format(groceries=list_of_groceries)
final_prompt

## 8. have your LLM Generate the Recipe As Per your Instructions.
output = llm.invoke(final_prompt)
print(output)
