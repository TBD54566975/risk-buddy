# Justfile for development tasks

# Command to download the model if it doesn't already exist in the current directory
download-models:
	if [ ! -f "Meta-Llama-3-8B.Q4_0.gguf" ]; then curl -o Meta-Llama-3-8B.Q4_0.gguf -L "https://huggingface.co/QuantFactory/Meta-Llama-3-8B-GGUF/resolve/main/Meta-Llama-3-8B.Q4_0.gguf"; else echo "Model already exists."; fi

# Command to run the development server, dependent on downloading the model
dev: download-models
	python main.py


test:
	python test-vectors.py

	