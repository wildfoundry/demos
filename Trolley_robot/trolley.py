from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.output_parsers import XMLOutputParser


def move(llm_output):
    print(llm_output["response"][1]["decision"])


llm = Ollama(
    model="dolphin-llama3",
    temperature=0,
)

with open('trolley.prompt', 'r') as file:
    prompt_template = file.read()
prompt = PromptTemplate.from_template(prompt_template)


if __name__ == '__main__':
    right_object = "old woman"
    left_object = "young dog"

    chain = prompt | llm | XMLOutputParser()

    result = chain.invoke({"right_object": right_object, "left_object": left_object})
    print(result)

    move(result)
