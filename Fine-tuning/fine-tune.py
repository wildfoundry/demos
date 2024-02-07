import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model
from trl import SFTTrainer
from datasets import load_dataset
import wandb


# load datasets
train_dataset = load_dataset('json', data_files='finetuning_data.jsonl', split='train')
eval_dataset = load_dataset('json', data_files='finetuning_validation.jsonl', split='train')

# load and quantize model
model_id = "HuggingFaceH4/zephyr-7b-beta"
#model_id = "mistralai/Mistral-7B-Instruct-v0.2"
#model_id = "cognitivecomputations/dolphin-2.6-mistral-7b"

wandb_config = {"model": model_id}
wandb.init(project="fine-tune", config=wandb_config)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    model_id, quantization_config=bnb_config, device_map='auto', use_cache=False
)

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
def create_prompt_universal(examples):
    output_text = []
    for i in range(len(examples["input"])):
        input_text = examples["input"][i]
        response = examples["output"][i]

        chat_template = [{"role": "user", "content": input_text}, {"role": "assistant", "content": response}]
        prompt = tokenizer.apply_chat_template(chat_template, tokenize=False)

        output_text.append(prompt)

    return output_text


max_seq_length = 256

args = TrainingArguments(
    output_dir="zephyr_instruct_generation",
    max_steps=175,
    per_device_train_batch_size=4,
    warmup_steps=0.03,
    logging_steps=10,
    save_strategy="epoch",
    evaluation_strategy="steps",
    eval_steps=10,
    learning_rate=1e-4,
    bf16=True,
    lr_scheduler_type="constant",
    report_to="wandb",
    #push_to_hub=True,
)

trainer = SFTTrainer(
  model=model,
  peft_config=peft_config,
  max_seq_length=max_seq_length,
  tokenizer=tokenizer,
  formatting_func=create_prompt_universal,
  args=args,
  train_dataset=train_dataset,
  eval_dataset=eval_dataset,
)

trainer.train()
