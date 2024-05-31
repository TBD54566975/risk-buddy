# Justfile for development tasks



# Command to download the model if it doesn't already exist in the current directory
download-models:
	if [ ! -f "Phi-3-medium-128k-instruct-Q5_K_M.gguf" ]; then curl -o phi-3-medium-128k-instruct.Q5_K_M.gguf -L "https://huggingface.co/bartowski/Phi-3-medium-128k-instruct-GGUF/resolve/main/Phi-3-medium-128k-instruct-Q5_K_M.gguf?download=true"; else echo "Model already exists."; fi

# Command to run the development server, dependent on downloading the model
dev: download-models
	python main.py


test:
	python test-vectors.py

	