#!/bin/bash
# Server fix script for CEM Backend
# Run this on your server to apply migrations and fix errors

set -e  # Exit on any error

echo "========================================"
echo "CEM Backend Server Fix Script"
echo "========================================"

cd /opt/crm-backend

echo ""
echo "[1/5] Pulling latest code from GitHub..."
git pull

echo ""
echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[3/5] Running database migrations..."
PYTHONPATH=/opt/crm-backend alembic upgrade head

echo ""
echo "[4/5] Checking migration status..."
PYTHONPATH=/opt/crm-backend alembic current

echo ""
echo "[5/5] Restarting the service..."
if systemctl is-active --quiet crm-backend; then
    sudo systemctl restart crm-backend
    echo "Service restarted successfully!"
elif systemctl is-active --quiet cem; then
    sudo systemctl restart cem
    echo "Service restarted successfully!"
else
    echo "No systemd service found. You may need to manually restart your server."
    echo "If using supervisor: sudo supervisorctl restart crm-backend"
    echo "If using PM2: pm2 restart crm-backend"
fi

echo ""
echo "========================================"
echo "Done! Server should now be fixed."
echo "========================================"
