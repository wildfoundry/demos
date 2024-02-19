from unsloth import FastLanguageModel


model, tokenizer = FastLanguageModel.from_pretrained("marsrover_zephyr_lora", load_in_4bit=True)
model.save_pretrained_gguf("gguf_model", tokenizer, quantization_method = "q6_k")