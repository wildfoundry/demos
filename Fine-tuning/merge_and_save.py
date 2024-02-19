from peft import PeftModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


model_id = "HuggingFaceH4/zephyr-7b-beta"

model_base = AutoModelForCausalLM.from_pretrained(
    model_id, return_dict=True, torch_dtype=torch.float16, device_map='auto', use_cache=False
)
tokenizer = AutoTokenizer.from_pretrained(model_id)
path_to_lora = "marsrover_zephyr_lora"
model = PeftModel.from_pretrained(model_base, path_to_lora)
model = model.merge_and_unload()

model.save_pretrained("marsrover_zephyr_merged")
tokenizer.save_pretrained("marsrover_zephyr_merged")
