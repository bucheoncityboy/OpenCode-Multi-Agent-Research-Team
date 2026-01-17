# OpenCode Research Team - Windows Installation Script
# Run: .\scripts\install.ps1

Write-Host "🔬 OpenCode Research Team - Installation Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Configuration paths
$OPENCODE_CONFIG_DIR = "$env:USERPROFILE\.config\opencode"
$DOCS_DIR = "$env:USERPROFILE"

# Check if running as correct user
Write-Host "`n📂 Installation Directories:" -ForegroundColor Yellow
Write-Host "   Config: $OPENCODE_CONFIG_DIR"
Write-Host "   Docs:   $DOCS_DIR"

# Create config directory if it doesn't exist
if (-not (Test-Path $OPENCODE_CONFIG_DIR)) {
    Write-Host "`n📁 Creating OpenCode config directory..." -ForegroundColor Green
    New-Item -ItemType Directory -Path $OPENCODE_CONFIG_DIR -Force | Out-Null
}

# Copy configuration files
Write-Host "`n📋 Copying configuration files..." -ForegroundColor Green

# oh-my-opencode.json
$sourceConfig = Join-Path $PSScriptRoot "..\config\oh-my-opencode.json"
$destConfig = Join-Path $OPENCODE_CONFIG_DIR "oh-my-opencode.json"
if (Test-Path $sourceConfig) {
    Copy-Item $sourceConfig $destConfig -Force
    Write-Host "   ✅ oh-my-opencode.json -> $destConfig"
} else {
    Write-Host "   ❌ oh-my-opencode.json not found!" -ForegroundColor Red
}

# AGENTS.md
$sourceAgents = Join-Path $PSScriptRoot "..\docs\AGENTS.md"
$destAgents = Join-Path $DOCS_DIR "AGENTS.md"
if (Test-Path $sourceAgents) {
    Copy-Item $sourceAgents $destAgents -Force
    Write-Host "   ✅ AGENTS.md -> $destAgents"
} else {
    Write-Host "   ❌ AGENTS.md not found!" -ForegroundColor Red
}

# RESEARCH_TEAM.md
$sourceResearch = Join-Path $PSScriptRoot "..\docs\RESEARCH_TEAM.md"
$destResearch = Join-Path $DOCS_DIR "RESEARCH_TEAM.md"
if (Test-Path $sourceResearch) {
    Copy-Item $sourceResearch $destResearch -Force
    Write-Host "   ✅ RESEARCH_TEAM.md -> $destResearch"
} else {
    Write-Host "   ❌ RESEARCH_TEAM.md not found!" -ForegroundColor Red
}

Write-Host "`n✨ Installation Complete!" -ForegroundColor Green
Write-Host "`n📖 Usage:" -ForegroundColor Yellow
Write-Host "   1. Start OpenCode: opencode"
Write-Host "   2. Enter Research Mode: /rt [your research topic]"
Write-Host "   3. Example: /rt BTC momentum strategy"

Write-Host "`n🔗 Documentation:" -ForegroundColor Yellow
Write-Host "   - AGENTS.md: $destAgents"
Write-Host "   - RESEARCH_TEAM.md: $destResearch"
Write-Host ""
