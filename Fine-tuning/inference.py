from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM


model_name = "mistral_instruct_generation/checkpoint-125"

#config = PeftConfig.from_pretrained("Grigorij/mistral_instruct_generation")
config = PeftConfig.from_pretrained(model_name)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model_id = "HuggingFaceH4/zephyr-7b-beta"
# base_model = "mistralai/Mistral-7B-Instruct-v0.2"
model = AutoModelForCausalLM.from_pretrained(
    model_id, quantization_config=bnb_config, device_map='auto', use_cache=False)
model = PeftModel.from_pretrained(model, model_name)

tokenizer = AutoTokenizer.from_pretrained(
    model_id,
    add_bos_token=True,
)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

def generate_response(prompt, model):
  encoded_input = tokenizer(prompt,  return_tensors="pt", add_special_tokens=True)
  model_inputs = encoded_input.to('cuda')
  generated_ids = model.generate(**model_inputs, max_new_tokens=1000, do_sample=True, pad_token_id=tokenizer.eos_token_id) #, eos_token_id=14491

  decoded_output = tokenizer.batch_decode(generated_ids)

  return decoded_output[0]


response = generate_response("<|system|>\nAct as Mars rover</s>\n<|user|>\nFront: low rocks, mineral, Right: crater, Left: clear space, Rear: clear space, container: empty, base: rear-left</s>\n<|assistant|>\n", model)
print(response)