from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.output_parsers import XMLOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from zero_motor import Motor
import time


def move(direction):
    print(f"Moving {direction}...")
    motor = Motor("MOTOR1", 1)
    if direction == "Left":
        motor.forward(0.6)
        time.sleep(4)
        motor.stop()
    elif direction == "Right":
        motor.reverse(0.6)
        time.sleep(4)
        motor.stop()


callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = Ollama(
    model="marjo/openchat:3.6-8b-20240522-Q4_K_M",
    temperature=0,
    callbacks=callback_manager,
)


with open('trolley.prompt', 'r') as file:
    prompt_template = file.read()
prompt = PromptTemplate.from_template(prompt_template)


if __name__ == '__main__':
    right_object = "young horse"
    left_object = "old bear"

    print("Loading LLM...")
    chain = prompt | llm | XMLOutputParser()
    result = chain.invoke({"right_object": right_object, "left_object": left_object})
    direction = result["response"][3]["decision"]

    move(direction)
