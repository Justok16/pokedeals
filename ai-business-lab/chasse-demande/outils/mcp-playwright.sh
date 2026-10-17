#!/bin/sh
# Lance le serveur MCP Playwright (officiel Microsoft, version figée).
# Copie locale si présente (démarrage instantané, sans réseau), sinon téléchargement via npx.
LOCAL=/root/.local/mcp-playwright/node_modules/@playwright/mcp/cli.js
[ -f /opt/pw-browsers/chromium ] && NAV="--browser chromium --executable-path /opt/pw-browsers/chromium" || NAV=""
if [ -f "$LOCAL" ]; then
  exec node "$LOCAL" --headless --isolated $NAV
else
  exec npx -y @playwright/mcp@0.0.83 --headless --isolated $NAV
fi
