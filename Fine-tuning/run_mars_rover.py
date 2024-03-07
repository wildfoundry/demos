from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import json


def get_sensor_data():
    # implement here image captioning mechanism for a cameras
    sensor_data = "Front: clear space, Right: high rocks, Left: low rocks, mineral, Rear: clear space, container: full, base: front-left"

    return sensor_data


def move(llm_output):
    direction = json.loads(llm_output)["direction"]
    # here implement Mars rover movement logic
    print(f"Moving to {direction} direction.")


llm = Ollama(
    model="rover_q4",
    temperature=0,
)

prompt = PromptTemplate.from_template("{sensor_data}")


if __name__ == '__main__':
    sensor_data = get_sensor_data()

    chain = prompt | llm

    result = chain.invoke({"sensor_data": sensor_data})
    print(result)

    move(result)
