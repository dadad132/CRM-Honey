#!/bin/bash
###############################################################################
# CRM-Honey — Universal Linux Installer
#
# Supports: AlmaLinux 8/9, Rocky Linux, RHEL 8/9, CentOS Stream,
#           Fedora, Ubuntu 20+, Debian 11+
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/dadad132/CRM-Honey/main/install.sh | sudo bash
#   # or
#   sudo bash install.sh
#
# Options (environment variables):
#   INSTALL_DIR=/opt/crm-backend   – installation directory
#   APP_PORT=8000                  – application port
#   SKIP_FIREWALL=1                – skip firewall configuration
#   GIT_BRANCH=main                – git branch to clone
###############################################################################

set -euo pipefail

# ── Configurable defaults ───────────────────────────────────────────────────
INSTALL_DIR="${INSTALL_DIR:-/opt/crm-backend}"
APP_PORT="${APP_PORT:-8000}"
GIT_BRANCH="${GIT_BRANCH:-main}"
REPO_URL="https://github.com/dadad132/CRM-Honey.git"
SERVICE_NAME="crm-backend"
APP_USER="crm"
APP_GROUP="crm"
MIN_PYTHON="3.10"

# ── logging ─────────────────────────────────────────────────────────────────
LOG_DIR="${INSTALL_DIR}/logs"
LOG_FILE=""  # set after INSTALL_DIR is created
STEP=0
TOTAL_STEPS=11
ERRORS=()

init_log() {
    mkdir -p "$LOG_DIR"
    LOG_FILE="${LOG_DIR}/install-$(date +%Y%m%d_%H%M%S).log"
    exec > >(tee -a "$LOG_FILE") 2>&1
}

# colours (disabled when piped)
if [ -t 1 ]; then
    GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
else
    GREEN=''; YELLOW=''; RED=''; CYAN=''; NC=''
fi

step() {
    STEP=$((STEP + 1))
    echo ""
    echo -e "${CYAN}[$STEP/$TOTAL_STEPS]${NC} $1"
    echo "────────────────────────────────────────"
}

ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
warn() { echo -e "  ${YELLOW}⚠${NC} $1"; }
fail() {
    echo -e "  ${RED}✗${NC} $1"
    ERRORS+=("Step $STEP: $1")
}

die() {
    echo ""
    echo -e "${RED}FATAL: $1${NC}"
    write_report
    echo -e "\nInstallation log saved to: ${LOG_FILE}"
    exit 1
}

# ── distro detection ────────────────────────────────────────────────────────
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO_ID="${ID:-unknown}"
        DISTRO_VERSION="${VERSION_ID:-0}"
        DISTRO_NAME="${PRETTY_NAME:-$DISTRO_ID $DISTRO_VERSION}"
    else
        die "Cannot detect distribution — /etc/os-release not found"
    fi

    case "$DISTRO_ID" in
        almalinux|rocky|rhel|centos|ol)  PKG_MANAGER="dnf" ;;
        fedora)                          PKG_MANAGER="dnf" ;;
        ubuntu|debian|linuxmint|pop)     PKG_MANAGER="apt" ;;
        *)
            # fall back to whatever is available
            if command -v dnf &>/dev/null; then
                PKG_MANAGER="dnf"
            elif command -v yum &>/dev/null; then
                PKG_MANAGER="yum"
            elif command -v apt-get &>/dev/null; then
                PKG_MANAGER="apt"
            else
                die "Unsupported distribution: $DISTRO_NAME (no apt/dnf/yum found)"
            fi
            ;;
    esac
}

# ── python version helper ──────────────────────────────────────────────────
version_gte() {
    # returns 0 (true) if $1 >= $2 in semver
    printf '%s\n%s' "$2" "$1" | sort -V -C
}

find_python() {
    # Try python3.12, python3.11, python3.10, python3 in that order
    for candidate in python3.12 python3.11 python3.10 python3; do
        if command -v "$candidate" &>/dev/null; then
            local ver
            ver=$("$candidate" --version 2>&1 | awk '{print $2}')
            if version_gte "$ver" "$MIN_PYTHON"; then
                PYTHON_BIN=$(command -v "$candidate")
                PYTHON_VER="$ver"
                return 0
            fi
        fi
    done
    return 1
}

# ── report writer ───────────────────────────────────────────────────────────
write_report() {
    local report_file="${LOG_DIR}/install-report.txt"
    mkdir -p "$LOG_DIR"
    {
        echo "═══════════════════════════════════════════════════════════"
        echo "  CRM-Honey Installation Report"
        echo "  Generated: $(date '+%Y-%m-%d %H:%M:%S %Z')"
        echo "═══════════════════════════════════════════════════════════"
        echo ""
        echo "System Information"
        echo "  Distribution : ${DISTRO_NAME:-unknown}"
        echo "  Kernel       : $(uname -r)"
        echo "  Architecture : $(uname -m)"
        echo "  Hostname     : $(hostname)"
        echo "  Package mgr  : ${PKG_MANAGER:-unknown}"
        echo ""
        echo "Installation Details"
        echo "  Install dir  : $INSTALL_DIR"
        echo "  Python       : ${PYTHON_BIN:-not found} (${PYTHON_VER:-unknown})"
        echo "  App port     : $APP_PORT"
        echo "  Service      : $SERVICE_NAME"
        echo "  User/Group   : $APP_USER:$APP_GROUP"
        echo "  Git branch   : $GIT_BRANCH"
        echo ""
        if [ ${#ERRORS[@]} -eq 0 ]; then
            echo "Result: SUCCESS ✓"
            echo ""
            echo "All $TOTAL_STEPS steps completed without errors."
        else
            echo "Result: COMPLETED WITH ERRORS"
            echo ""
            echo "Errors encountered (${#ERRORS[@]}):"
            for err in "${ERRORS[@]}"; do
                echo "  • $err"
            done
        fi
        echo ""
        echo "Full log: $LOG_FILE"
        echo "═══════════════════════════════════════════════════════════"
    } > "$report_file"
    echo ""
    echo -e "${CYAN}Report saved to:${NC} $report_file"
}

# ── pre-flight ──────────────────────────────────────────────────────────────
preflight() {
    if [ "$(id -u)" -ne 0 ]; then
        die "This script must be run as root (use sudo)"
    fi
    detect_distro
    init_log

    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}   CRM-Honey Installer${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "  Distribution : $DISTRO_NAME"
    echo "  Package mgr  : $PKG_MANAGER"
    echo "  Install dir  : $INSTALL_DIR"
    echo "  Port         : $APP_PORT"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1 — System packages
# ═══════════════════════════════════════════════════════════════════════════
install_system_packages() {
    step "Installing system packages"

    case "$PKG_MANAGER" in
        dnf|yum)
            "$PKG_MANAGER" install -y epel-release 2>/dev/null || true
            "$PKG_MANAGER" install -y \
                git gcc make rsync \
                python3 python3-devel python3-pip \
                sqlite sqlite-libs \
                curl wget \
                || die "Failed to install system packages via $PKG_MANAGER"
            # AlmaLinux 8 may need python3.11 from appstream
            if ! find_python; then
                "$PKG_MANAGER" install -y python3.11 python3.11-devel python3.11-pip 2>/dev/null || true
            fi
            ;;
        apt)
            export DEBIAN_FRONTEND=noninteractive
            apt-get update -qq
            apt-get install -y -qq \
                git gcc make rsync \
                python3 python3-dev python3-pip python3-venv \
                sqlite3 libsqlite3-dev \
                curl wget \
                || die "Failed to install system packages via apt"
            ;;
    esac
    ok "System packages installed"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 2 — Verify Python
# ═══════════════════════════════════════════════════════════════════════════
verify_python() {
    step "Verifying Python $MIN_PYTHON+"

    if ! find_python; then
        die "Python $MIN_PYTHON or newer not found. Install python3.11+ and retry."
    fi
    ok "Found $PYTHON_BIN ($PYTHON_VER)"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 3 — Create app user and directories
# ═══════════════════════════════════════════════════════════════════════════
create_user_and_dirs() {
    step "Creating user '$APP_USER' and directories"

    if ! id "$APP_USER" &>/dev/null; then
        useradd --system --shell /sbin/nologin --home-dir "$INSTALL_DIR" "$APP_USER"
        ok "Created system user '$APP_USER'"
    else
        ok "User '$APP_USER' already exists"
    fi

    mkdir -p "$INSTALL_DIR"
    ok "Created $INSTALL_DIR"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4 — Clone / update repository
# ═══════════════════════════════════════════════════════════════════════════
clone_or_update_repo() {
    step "Cloning repository (branch: $GIT_BRANCH)"

    if [ -d "$INSTALL_DIR/.git" ]; then
        cd "$INSTALL_DIR"
        git fetch origin
        git checkout "$GIT_BRANCH"
        git reset --hard "origin/$GIT_BRANCH"
        ok "Updated existing repository"
    else
        # Clone into a temp dir and move contents (INSTALL_DIR may already have logs/)
        local tmp_dir
        tmp_dir=$(mktemp -d)
        git clone --branch "$GIT_BRANCH" --depth 1 "$REPO_URL" "$tmp_dir"
        # Move everything except logs which we already created
        rsync -a --ignore-existing "$tmp_dir/" "$INSTALL_DIR/" 2>/dev/null \
            || cp -rn "$tmp_dir/." "$INSTALL_DIR/" 2>/dev/null \
            || cp -r "$tmp_dir/." "$INSTALL_DIR/"
        rm -rf "$tmp_dir"
        ok "Cloned $REPO_URL"
    fi

    cd "$INSTALL_DIR"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 5 — Create Python virtual environment
# ═══════════════════════════════════════════════════════════════════════════
setup_venv() {
    step "Creating Python virtual environment"

    local venv_dir="$INSTALL_DIR/venv"
    if [ -d "$venv_dir" ]; then
        ok "Virtual environment already exists"
    else
        "$PYTHON_BIN" -m venv "$venv_dir" || die "Failed to create virtual environment"
        ok "Created venv at $venv_dir"
    fi

    # Activate for the rest of the script
    # shellcheck disable=SC1091
    source "$venv_dir/bin/activate"
    pip install --upgrade pip setuptools wheel -q
    ok "pip upgraded"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 6 — Install Python dependencies
# ═══════════════════════════════════════════════════════════════════════════
install_python_deps() {
    step "Installing Python dependencies"

    cd "$INSTALL_DIR"
    pip install -r requirements.txt -q || die "pip install failed — check requirements.txt"
    ok "All Python packages installed"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 7 — Generate .env configuration
# ═══════════════════════════════════════════════════════════════════════════
generate_env() {
    step "Generating configuration (.env)"

    local env_file="$INSTALL_DIR/.env"
    if [ -f "$env_file" ]; then
        ok ".env already exists — skipping (will not overwrite)"
        return
    fi

    local secret_key
    secret_key=$("$INSTALL_DIR/venv/bin/python" -c "import secrets; print(secrets.token_urlsafe(48))")

    cat > "$env_file" <<ENVEOF
# CRM-Honey Configuration
# Generated by installer on $(date '+%Y-%m-%d %H:%M:%S')

APP_NAME=CRM Backend
APP_DEBUG=False
APP_HOST=0.0.0.0
APP_PORT=$APP_PORT

SECRET_KEY=$secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_MINUTES=10080

DATABASE_URL=sqlite+aiosqlite:///./data.db

# Google OAuth (optional)
# GOOGLE_CLIENT_ID=
# GOOGLE_CLIENT_SECRET=
# GOOGLE_REDIRECT_URI=https://yourdomain.com/web/auth/google/callback

# SMTP (optional)
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=
# SMTP_PASSWORD=
# SMTP_FROM=
# SMTP_USE_TLS=true
ENVEOF

    chmod 600 "$env_file"
    ok "Generated .env with random SECRET_KEY"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 8 — Create required directories
# ═══════════════════════════════════════════════════════════════════════════
create_app_dirs() {
    step "Creating application directories"

    cd "$INSTALL_DIR"
    local dirs=(
        "app/uploads/comments"
        "app/uploads/chat_messages"
        "app/uploads/profile_pictures"
        "app/uploads/branding"
        "app/uploads/tickets"
        "app/static"
        "backups"
        "logs"
        "updates"
    )
    for d in "${dirs[@]}"; do
        mkdir -p "$d"
    done

    ok "Created upload, backup, log, and static directories"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 9 — Database initialisation & migrations
# ═══════════════════════════════════════════════════════════════════════════
run_all_migrations() {
    step "Initializing database and running migrations"

    cd "$INSTALL_DIR"
    local VENV_PYTHON="$INSTALL_DIR/venv/bin/python"

    # 9a — Let SQLModel create all tables (init_models)
    echo "  → Initializing database schema..."
    "$VENV_PYTHON" -c "
import asyncio
import sys, os
sys.path.insert(0, '$INSTALL_DIR')
os.chdir('$INSTALL_DIR')

async def init():
    from app.core.database import init_models
    await init_models()
    print('    Database tables created')

asyncio.run(init())
" || {
        fail "Database init_models() failed"
        return
    }
    ok "Database schema initialized"

    # 9b — Run all individual migration scripts in migrations/
    echo "  → Running migration scripts..."
    local migration_dir="$INSTALL_DIR/migrations"
    local migration_count=0
    local migration_fail=0

    if [ -d "$migration_dir" ]; then
        for script in "$migration_dir"/*.py; do
            [ -f "$script" ] || continue
            local name
            name=$(basename "$script")
            echo "    Running $name ..."
            if PYTHONPATH="$INSTALL_DIR" "$VENV_PYTHON" "$script" 2>&1; then
                migration_count=$((migration_count + 1))
            else
                warn "Migration $name had errors (non-fatal)"
                migration_fail=$((migration_fail + 1))
            fi
        done
    fi

    # 9c — Run root-level migration scripts
    for script in \
        add_performance_indexes.py \
        add_task_billing_columns.py \
        add_task_customer_columns.py \
        run_migrations.py; do
        if [ -f "$INSTALL_DIR/$script" ]; then
            echo "    Running $script ..."
            if (cd "$INSTALL_DIR" && PYTHONPATH="$INSTALL_DIR" "$VENV_PYTHON" "$INSTALL_DIR/$script") 2>&1; then
                migration_count=$((migration_count + 1))
            else
                warn "$script had errors (non-fatal)"
                migration_fail=$((migration_fail + 1))
            fi
        fi
    done

    # 9d — Run Alembic migrations if alembic directory exists
    if [ -f "$INSTALL_DIR/alembic.ini" ] && [ -d "$INSTALL_DIR/alembic" ]; then
        echo "  → Running Alembic migrations..."
        if "$INSTALL_DIR/venv/bin/alembic" upgrade head 2>&1; then
            ok "Alembic migrations applied"
        else
            warn "Alembic migrations had errors (non-fatal — likely already applied)"
        fi
    fi

    if [ "$migration_fail" -eq 0 ]; then
        ok "All $migration_count migration scripts completed successfully"
    else
        warn "$migration_count succeeded, $migration_fail had non-fatal errors"
        fail "$migration_fail migration script(s) had errors"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 10 — Set ownership and permissions
# ═══════════════════════════════════════════════════════════════════════════
set_permissions() {
    step "Setting file ownership and permissions"

    chown -R "$APP_USER:$APP_GROUP" "$INSTALL_DIR"
    # Ensure data files are writable
    chmod 660 "$INSTALL_DIR/data.db" 2>/dev/null || true
    chmod 600 "$INSTALL_DIR/.env" 2>/dev/null || true

    ok "Ownership set to $APP_USER:$APP_GROUP"
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 11 — systemd service + firewall
# ═══════════════════════════════════════════════════════════════════════════
setup_systemd_and_firewall() {
    step "Configuring systemd service and firewall"

    # ── systemd unit ────────────────────────────────────────────────
    local service_file="/etc/systemd/system/${SERVICE_NAME}.service"
    cat > "$service_file" <<SVCEOF
[Unit]
Description=CRM-Honey Backend Application
After=network.target
Documentation=https://github.com/dadad132/CRM-Honey

[Service]
Type=simple
User=$APP_USER
Group=$APP_GROUP
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONUNBUFFERED=1"

ExecStart=$INSTALL_DIR/venv/bin/python start_server.py --port $APP_PORT

TimeoutStopSec=30
KillMode=mixed
KillSignal=SIGTERM

Restart=on-failure
RestartSec=5

StandardOutput=journal
StandardError=journal
SyslogIdentifier=$SERVICE_NAME

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$INSTALL_DIR

[Install]
WantedBy=multi-user.target
SVCEOF

    systemctl daemon-reload
    systemctl enable "$SERVICE_NAME"
    ok "systemd service created and enabled"

    # ── firewall ────────────────────────────────────────────────────
    if [ "${SKIP_FIREWALL:-0}" = "1" ]; then
        ok "Firewall configuration skipped (SKIP_FIREWALL=1)"
    elif command -v firewall-cmd &>/dev/null; then
        # RHEL/AlmaLinux/Rocky — firewalld
        firewall-cmd --permanent --add-port="${APP_PORT}/tcp" 2>/dev/null && \
        firewall-cmd --reload 2>/dev/null && \
        ok "firewalld: opened port $APP_PORT/tcp" || \
        warn "Could not configure firewalld"
    elif command -v ufw &>/dev/null; then
        # Ubuntu/Debian — ufw
        ufw allow "$APP_PORT/tcp" 2>/dev/null && \
        ok "ufw: allowed port $APP_PORT/tcp" || \
        warn "Could not configure ufw"
    else
        warn "No firewall tool detected — please open port $APP_PORT manually"
    fi

    # ── start the service ───────────────────────────────────────────
    systemctl start "$SERVICE_NAME"
    sleep 2

    if systemctl is-active --quiet "$SERVICE_NAME"; then
        ok "Service $SERVICE_NAME is running"
    else
        fail "Service $SERVICE_NAME failed to start — check: journalctl -u $SERVICE_NAME"
    fi
}

# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════
main() {
    preflight
    install_system_packages
    verify_python
    create_user_and_dirs
    clone_or_update_repo
    setup_venv
    install_python_deps
    generate_env
    create_app_dirs
    run_all_migrations
    set_permissions
    setup_systemd_and_firewall

    write_report

    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}   Installation Complete!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "  URL            : http://$(hostname -I 2>/dev/null | awk '{print $1}' || echo 'your-server-ip'):$APP_PORT"
    echo "  Service        : systemctl status $SERVICE_NAME"
    echo "  Logs           : journalctl -u $SERVICE_NAME -f"
    echo "  Install log    : $LOG_FILE"
    echo "  Install report : ${LOG_DIR}/install-report.txt"
    echo ""
    if [ ${#ERRORS[@]} -gt 0 ]; then
        echo -e "${YELLOW}  ⚠ ${#ERRORS[@]} warning(s) — see report for details${NC}"
    fi
    echo ""
}

main "$@"
