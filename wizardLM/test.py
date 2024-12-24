# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("cognitivecomputations/WizardLM-7B-Uncensored")
model = AutoModelForCausalLM.from_pretrained("cognitivecomputations/WizardLM-7B-Uncensored")

prompt = "Hey, are you conscious? Can you talk to me?"
inputs = tokenizer(prompt, return_tensors="pt")

# Generate
generate_ids = model.generate(inputs.input_ids, max_length=30)
tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]


#This will download a 13.5GB model and may take a while to load.