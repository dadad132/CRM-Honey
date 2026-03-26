#!/bin/bash
# Fix login issue: pull latest code and add FORCE_HTTPS=false
set -e

INSTALL_DIR="/opt/crm-backend"
SERVICE_NAME="crm-backend"

echo "Pulling latest code..."
cd "$INSTALL_DIR"
sudo -u crm git pull origin main

# Add FORCE_HTTPS=false if not already present
if ! grep -q "FORCE_HTTPS" "$INSTALL_DIR/.env" 2>/dev/null; then
    echo "FORCE_HTTPS=false" | sudo tee -a "$INSTALL_DIR/.env"
    echo "Added FORCE_HTTPS=false to .env"
else
    echo "FORCE_HTTPS already set in .env"
fi

echo "Restarting service..."
sudo systemctl restart "$SERVICE_NAME"
sleep 2

if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "Done! Service is running. Try logging in now."
else
    echo "Warning: Service failed to start. Check: journalctl -u $SERVICE_NAME -n 30"
fi
