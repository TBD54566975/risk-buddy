# Use a pipeline as a high-level helper
from transformers import pipeline

# note: this seems really really super slow
pipe = pipeline("text-generation", model="microsoft/Phi-3-mini-4k-instruct", trust_remote_code=True)

print(pipe("hey"))
print(pipe("hey again"))
