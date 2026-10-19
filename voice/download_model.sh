#!/usr/bin/env bash
set -euo pipefail

# Download whisper.cpp tiny model for voice transcription
MODEL_DIR="${1:-./models}"
mkdir -p "$MODEL_DIR"

MODEL_FILE="$MODEL_DIR/ggml-tiny.bin"

if [ -f "$MODEL_FILE" ]; then
    echo "Model already exists at $MODEL_FILE"
    exit 0
fi

echo "Downloading ggml-tiny.bin..."
curl -L -o "$MODEL_FILE" "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin"
echo "Done! Model downloaded to $MODEL_FILE"
