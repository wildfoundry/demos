import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model
from trl import SFTTrainer
from datasets import load_dataset
import wandb


wandb.init(project="fine-tune")

# load datasets
train_dataset = load_dataset('json', data_files='finetuning_data.jsonl', split='train')
eval_dataset = load_dataset('json', data_files='finetuning_validation.jsonl', split='train')

# load and quantize model
model_id = "HuggingFaceH4/zephyr-7b-beta"
#model_id = "mistralai/Mistral-7B-Instruct-v0.2"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    model_id, quantization_config=bnb_config, device_map='auto', use_cache=False)

# set up tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    model_id,
    add_bos_token=True,
    add_eos_token=True,
)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"


# Lora (fine-tuning) Config
peft_config = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r=64,
    bias="none",
    task_type="CAUSAL_LM"
)

model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, peft_config)


# constructs prompt the way model understands
def create_prompt_mistral(examples):
    output_text = []
    for i in range(len(examples["input"])):
        input_text = examples["input"][i]
        response = examples["output"][i]

        full_prompt = "<s>"
        full_prompt += "### Instruction:"
        full_prompt += "\n\n### Input:"
        full_prompt += "\n" + input_text
        full_prompt += "\n\n### Response:"
        full_prompt += "\n" + response
        full_prompt += "</s>"

        output_text.append(full_prompt)

    return output_text


def create_my_prompt_mistral(examples):
    output_text = []
    for i in range(len(examples["input"])):
        input_text = examples["input"][i]
        response = examples["output"][i]

        full_prompt = "[INST]" + input_text + "[/INST]\n" + response
        print(full_prompt)
        output_text.append(full_prompt)

    return output_text


def create_prompt_zephyr(examples):
    output_text = []
    for i in range(len(examples["input"])):
        input_text = examples["input"][i]
        response = examples["output"][i]

        full_prompt = "<|system|>\n"
        full_prompt += "Act as Mars rover</s>\n"
        full_prompt += "<|user|>\n"
        full_prompt += input_text + "</s>\n"
        full_prompt += "<|assistant|>\n"
        full_prompt += response

        output_text.append(full_prompt)

    return output_text

max_seq_length = 256

args = TrainingArguments(
    output_dir="mistral_instruct_generation",
    #output_dir="zephyr_instruct_generation",
    #num_train_epochs=5,
    max_steps=150, # comment out this line if you want to train in epochs
    per_device_train_batch_size=4,
    warmup_steps=0.03,
    logging_steps=10,
    save_strategy="epoch",
    #evaluation_strategy="epoch",
    evaluation_strategy="steps",
    eval_steps=10, # comment out this line if you want to evaluate at the end of each epoch
    learning_rate=1e-4,
    bf16=True,
    lr_scheduler_type='constant',
    report_to="wandb",
    push_to_hub=True,
)

trainer = SFTTrainer(
  model=model,
  peft_config=peft_config,
  max_seq_length=max_seq_length,
  tokenizer=tokenizer,
  formatting_func=create_prompt_zephyr,
  args=args,
  train_dataset=train_dataset,
  eval_dataset=eval_dataset,
)

trainer.train()

#trainer.save_model("mistral_finetuned")

# push to hugging face
#trainer.push_to_hub("Grigorij/Mistral-Mars-Rover")
# Testing
#merged_model = model.merge_and_unload()
