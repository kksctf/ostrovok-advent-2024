FROM ghcr.io/ggerganov/llama.cpp:server-cuda-9fe94ccac92693d4ae1bc283ff0574e8b3f4e765

# Install wget
RUN apt-get update && apt-get install -y wget

# Create a directory for the models
RUN mkdir -p /models

# Add the initialization script
COPY init.sh /init.sh
RUN chmod +x /init.sh

# Run the initialization script before starting the server
ENTRYPOINT ["/init.sh"]
CMD ["-m", "/models/Saiga-Llama-3.0-8B-Instruct-Q4_K.gguf", "--port", "8000", "--host", "::", "--ctx-size", "32000", "--threads", "16", "--n-gpu-layers", "99"]
