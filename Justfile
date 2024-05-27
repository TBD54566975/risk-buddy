# Justfile for development tasks

# Command to download the model if it doesn't already exist in the current directory
download-models:
	if [ ! -f "phi-3-mini-128k-instruct.Q8_0.gguf" ]; then curl -o phi-3-mini-128k-instruct.Q8_0.gguf -L "https://huggingface.co/MoMonir/Phi-3-mini-128k-instruct-GGUF/resolve/main/phi-3-mini-128k-instruct.Q8_0.gguf"; else echo "Model already exists."; fi

# Command to run the development server, dependent on downloading the model
dev: download-models
	python main.py


test:
	python test-vectors.py

	