#!/bin/bash
set -e

# Start Ollama service in background
echo "Starting Ollama service..."
ollama serve > /var/log/ollama.log 2>&1 &
sleep 5

# Pull default model
echo "Pulling default LLM model..."
ollama pull qwen2.5:latest

# Handle different commands
case "$1" in
    serve)
        echo "Starting FastAPI application..."
        python app.py
        ;;
    generate)
        echo "Running test generation..."
        shift
        python main.py "$@"
        ;;
    compile)
        echo "Compiling generated tests..."
        ./cicd/run_generated_tests.sh "${2:-GeneratedTest}"
        ;;
    *)
        exec "$@"
        ;;
esac
