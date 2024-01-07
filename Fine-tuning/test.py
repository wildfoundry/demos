from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "HuggingFaceH4/zephyr-7b-beta",
    add_bos_token=True,
    add_eos_token=True,
)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

input_text = "Front: crater, mineral, Right: dust clouds, Left: clear space, Rear: high rocks, container: full, base: rear"
response = "{'reasoning': 'Container is empty, so the priority is to explore. High rocks at left are impassable. Crater at front is risky to navigate. Low rocks at rear are slightly risky. Clear space at right is the best option. Move right.', 'direction': 'Right'}"
prompt = "[INST]" + input_text + "[/INST]\n" + response

print(tokenizer(" Front'}"))
template = tokenizer.apply_chat_template([{"role": "user", "content": "What is your favourite condiment?"}])
print(template)
