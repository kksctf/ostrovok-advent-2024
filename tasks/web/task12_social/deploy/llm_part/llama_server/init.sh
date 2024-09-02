#!/bin/sh
set -euo

MODEL_PATH="/models/Saiga-Llama-3.0-8B-Instruct-Q4_K.gguf"
MODEL_URL="https://huggingface.co/IlyaGusev/saiga_llama3_8b_gguf/resolve/main/model-q4_K.gguf"


# Check if the model file exists, if not, download it
if [ ! -f "$MODEL_PATH" ]; then
    echo "Model file not found. Downloading..."
    wget --no-verbose --show-progress --progress=dot:mega -O "$MODEL_PATH" "$MODEL_URL"
else
    echo "Model file already exists."
fi

nvidia-smi

# Start the Llama server
exec ./llama-server "$@"
