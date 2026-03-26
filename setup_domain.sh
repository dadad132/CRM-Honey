#!/bin/bash
# Setup nginx reverse proxy for CRM-Honey
# Usage: sudo bash setup_domain.sh yourdomain.com
set -e

DOMAIN="${1:-}"
APP_PORT="${APP_PORT:-8000}"

if [ -z "$DOMAIN" ]; then
    echo "Usage: sudo bash setup_domain.sh yourdomain.com"
    echo "Example: sudo bash setup_domain.sh task.honeypottask.co.za"
    exit 1
fi

if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root (use sudo)"
    exit 1
fi

echo "Setting up nginx for: $DOMAIN -> localhost:$APP_PORT"

# Install nginx if not present
if ! command -v nginx &>/dev/null; then
    echo "Installing nginx..."
    if command -v dnf &>/dev/null; then
        dnf install -y nginx
    elif command -v apt-get &>/dev/null; then
        apt-get install -y nginx
    fi
fi

# Determine config directory
if [ -d /etc/nginx/conf.d ]; then
    NGINX_CONF="/etc/nginx/conf.d/${DOMAIN}.conf"
elif [ -d /etc/nginx/sites-available ]; then
    NGINX_CONF="/etc/nginx/sites-available/${DOMAIN}"
else
    NGINX_CONF="/etc/nginx/conf.d/${DOMAIN}.conf"
    mkdir -p /etc/nginx/conf.d
fi

cat > "$NGINX_CONF" <<NGINXEOF
server {
    listen 80;
    server_name $DOMAIN;

    client_max_body_size 50M;

    # Proxy all requests to the CRM backend
    location / {
        proxy_pass http://127.0.0.1:$APP_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # WebSocket support (for live updates)
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 300s;
    }
}
NGINXEOF

# Enable site (Debian/Ubuntu style)
if [ -d /etc/nginx/sites-enabled ] && [ -d /etc/nginx/sites-available ]; then
    ln -sf "/etc/nginx/sites-available/${DOMAIN}" "/etc/nginx/sites-enabled/${DOMAIN}"
fi

# Test and reload nginx
echo "Testing nginx config..."
nginx -t || { echo "Nginx config test failed!"; exit 1; }

systemctl enable nginx
systemctl restart nginx

# Open port 80 in firewall
if command -v firewall-cmd &>/dev/null; then
    firewall-cmd --permanent --add-service=http 2>/dev/null || true
    firewall-cmd --reload 2>/dev/null || true
    echo "Firewall: opened port 80 (http)"
elif command -v ufw &>/dev/null; then
    ufw allow 80/tcp 2>/dev/null || true
    echo "Firewall: opened port 80 (http)"
fi

echo ""
echo "Done! Nginx is proxying $DOMAIN -> localhost:$APP_PORT"
echo ""
echo "Make sure your DNS A record points to this server's IP:"
echo "  $DOMAIN -> $(hostname -I 2>/dev/null | awk '{print $1}')"
echo ""
echo "Test it: curl -I http://$DOMAIN"
