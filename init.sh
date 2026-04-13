#!/bin/bash
# HiveFind development startup script

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
EMBED_DIR="$PROJECT_DIR/services/embed"
RUNWAY_DIR="$PROJECT_DIR/runwayagents"

echo "=== HiveFind Init ==="
echo "Project: $PROJECT_DIR"

# 1. Check embed service venv
if [ -d "$EMBED_DIR/venv" ]; then
    echo "✓ Embed service venv exists"
else
    echo "✗ Embed service venv missing — run: cd $EMBED_DIR && python3 -m venv venv && pip install -e ."
    exit 1
fi

# 2. Check .env
if [ -f "$PROJECT_DIR/.env" ]; then
    echo "✓ .env file exists"
    # Verify required keys (names only, not values)
    for key in GEMINI_API_KEY PINECONE_API_KEY; do
        if grep -q "^$key=" "$PROJECT_DIR/.env"; then
            echo "  ✓ $key set"
        else
            echo "  ✗ $key MISSING"
        fi
    done
else
    echo "✗ .env file missing"
    exit 1
fi

# 3. Start embed service (localhost only)
echo ""
echo "Starting embed service on localhost:8766..."
cd "$EMBED_DIR"
source venv/bin/activate
uvicorn src.main:app --host 127.0.0.1 --port 8766 &
EMBED_PID=$!
sleep 3

# 4. Health check
if curl -sf http://127.0.0.1:8766/health > /dev/null 2>&1; then
    echo "✓ Embed service healthy (PID: $EMBED_PID)"
else
    echo "✗ Embed service FAILED to start"
    kill $EMBED_PID 2>/dev/null
    exit 1
fi

# 5. Check runwayagents (optional)
if [ -f "$RUNWAY_DIR/package.json" ]; then
    echo "✓ Runway agents app present"
else
    echo "⚠ Runway agents app not found (optional)"
fi

echo ""
echo "=== Ready ==="
echo "Embed service: http://127.0.0.1:8766"
echo "Health check:  http://127.0.0.1:8766/health"
echo "PID: $EMBED_PID (kill $EMBED_PID to stop)"
