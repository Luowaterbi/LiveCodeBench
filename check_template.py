from transformers import AutoTokenizer, AutoModelForCausalLM
import os

PATH = "/mnt/jfs/xysj/code/checkpoints/"
models = os.listdir(PATH)

for model in models:
    checkpoints = os.listdir(PATH + model)
    # get
    check_path = PATH + model + "/" + checkpoints[-1]
    print("checkpoint:", check_path)
    tokenizer = AutoTokenizer.from_pretrained(check_path, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(check_path)
    # 打印chat template
    # print(f"Chat template for {model}:")
    # print(tokenizer.chat_template)
    
    # 可选:打印default chat template
    # if hasattr(tokenizer, "default_chat_template"):
    #     print("\nDefault chat template:")
    #     print(tokenizer.default_chat_template)

    messages = [
        {
            "role": "user",
            "content": "write a quick sort!"
        }
    ]
    # 生成chat history
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
    outputs = model.generate(input_ids=inputs.to(model.device), max_new_tokens=150)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))

