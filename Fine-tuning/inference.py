from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM


model_name = "zephyr_instruct_generation/checkpoint-100"

#config = PeftConfig.from_pretrained("Grigorij/mistral_instruct_generation")
config = PeftConfig.from_pretrained(model_name)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model_id = "HuggingFaceH4/zephyr-7b-beta"
#model_id = "mistralai/Mistral-7B-Instruct-v0.2"

model = AutoModelForCausalLM.from_pretrained(
    model_id, quantization_config=bnb_config, device_map='auto', use_cache=False)
model = PeftModel.from_pretrained(model, model_name)

tokenizer = AutoTokenizer.from_pretrained(
    model_id,
    add_bos_token=True,
)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

closing_curly_bracket_token_nr = 14491


def generate_response(prompt, model):
    encoded_input = tokenizer(prompt,  return_tensors="pt", add_special_tokens=True)
    model_inputs = encoded_input.to('cuda')
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=200,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        #eos_token_id=tokenizer.eos_token_id,
        eos_token_id=closing_curly_bracket_token_nr,    # cutting out response on the particular token. Not a good practice.
    )

    decoded_output = tokenizer.batch_decode(generated_ids)

    return decoded_output[0]


prompt_chat_template = [{
    "role": "user",
    "content": "Front: dust clouds, Right: crater, Left: clear space, Rear: clear space, container: empty, base: front-left"
}]
prompt = tokenizer.apply_chat_template(prompt_chat_template, tokenize=False, add_generation_prompt=True)

response = generate_response(prompt, model)
print(response)
