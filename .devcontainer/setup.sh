#!/bin/bash
set -e

echo "🔧 Starting setup..."

# 1. Install Python, pip3, and curl if missing
echo "📦 Checking for Python and curl..."
if ! command -v python3 &>/dev/null || ! command -v pip3 &>/dev/null || ! command -v curl &>/dev/null; then
    echo "🔄 Installing python3, pip3, and curl..."
    apt-get update
    apt-get install -y python3 python3-pip curl
else
    echo "✅ Python3, pip3, and curl already installed."
fi

# 2. Install Go only if missing
if ! command -v go &>/dev/null; then
    echo "🐹 Installing Go..."
    curl -sSL https://go.dev/dl/go1.22.0.linux-amd64.tar.gz -o go.tar.gz
    rm -rf /usr/local/go
    tar -C /usr/local -xzf go.tar.gz
    ln -s /usr/local/go/bin/go /usr/local/bin/go
else
    echo "✅ Go already installed: $(go version)"
fi

# 3. Install Docker Compose only if missing
if ! command -v docker-compose &>/dev/null; then
    echo "🐳 Installing Docker Compose..."
    curl -sSL "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo "✅ Docker Compose already installed: $(docker-compose --version)"
fi

# 4. Install Python requirements if missing
REQ_FILE="/workspaces/multi-app-project/python-app/requirements.txt"
if [ -f "$REQ_FILE" ]; then
    echo "🐍 Checking Python requirements..."

    INSTALLED=$(pip3 freeze)
    MISSING=$(grep -v -Fxf <(echo "$INSTALLED") "$REQ_FILE" || true)

    if [ -n "$MISSING" ]; then
        echo "📦 Installing missing Python packages..."
        pip3 install -r "$REQ_FILE"
    else
        echo "✅ Python requirements already satisfied."
    fi
else
    echo "⚠️ requirements.txt not found in python-app"
fi

echo "✅ Setup complete!"
