#!/bin/bash
# OpenCode Research Team - Linux/macOS Installation Script
# Run: chmod +x scripts/install.sh && ./scripts/install.sh

echo "🔬 OpenCode Research Team - Installation Script"
echo "================================================"

# Configuration paths
OPENCODE_CONFIG_DIR="$HOME/.config/opencode"
DOCS_DIR="$HOME"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo ""
echo "📂 Installation Directories:"
echo "   Config: $OPENCODE_CONFIG_DIR"
echo "   Docs:   $DOCS_DIR"

# Create config directory if it doesn't exist
if [ ! -d "$OPENCODE_CONFIG_DIR" ]; then
    echo ""
    echo "📁 Creating OpenCode config directory..."
    mkdir -p "$OPENCODE_CONFIG_DIR"
fi

# Copy configuration files
echo ""
echo "📋 Copying configuration files..."

# oh-my-opencode.json
if [ -f "$PROJECT_DIR/config/oh-my-opencode.json" ]; then
    cp "$PROJECT_DIR/config/oh-my-opencode.json" "$OPENCODE_CONFIG_DIR/oh-my-opencode.json"
    echo "   ✅ oh-my-opencode.json -> $OPENCODE_CONFIG_DIR/oh-my-opencode.json"
else
    echo "   ❌ oh-my-opencode.json not found!"
fi

# AGENTS.md
if [ -f "$PROJECT_DIR/docs/AGENTS.md" ]; then
    cp "$PROJECT_DIR/docs/AGENTS.md" "$DOCS_DIR/AGENTS.md"
    echo "   ✅ AGENTS.md -> $DOCS_DIR/AGENTS.md"
else
    echo "   ❌ AGENTS.md not found!"
fi

# RESEARCH_TEAM.md
if [ -f "$PROJECT_DIR/docs/RESEARCH_TEAM.md" ]; then
    cp "$PROJECT_DIR/docs/RESEARCH_TEAM.md" "$DOCS_DIR/RESEARCH_TEAM.md"
    echo "   ✅ RESEARCH_TEAM.md -> $DOCS_DIR/RESEARCH_TEAM.md"
else
    echo "   ❌ RESEARCH_TEAM.md not found!"
fi

echo ""
echo "✨ Installation Complete!"
echo ""
echo "📖 Usage:"
echo "   1. Start OpenCode: opencode"
echo "   2. Enter Research Mode: /rt [your research topic]"
echo "   3. Example: /rt BTC momentum strategy"
echo ""
echo "🔗 Documentation:"
echo "   - AGENTS.md: $DOCS_DIR/AGENTS.md"
echo "   - RESEARCH_TEAM.md: $DOCS_DIR/RESEARCH_TEAM.md"
echo ""
