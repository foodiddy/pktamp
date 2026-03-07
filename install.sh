#!/usr/bin/env bash
set -euo pipefail

echo "=== Pktamp Installer ==="
echo ""

# Get bind IP
read -p "Enter the IP address the web UI should bind to [0.0.0.0]: " BIND_IP
BIND_IP=${BIND_IP:-0.0.0.0}
PORT=8080

echo ""
echo "=== Detecting Linux distribution ==="

if [ -f /etc/debian_version ]; then
    OS="debian"
    echo "Detected: Debian/Ubuntu"
    PKG_MGR="apt-get"
else
    OS="rhel"
    echo "Detected: RHEL/CentOS/AlmaLinux"
    PKG_MGR="dnf"
fi

echo ""
echo "=== Installing required packages ==="

if [ "$OS" = "debian" ]; then
    sudo $PKG_MGR update
    sudo $PKG_MGR install -y \
        python3 python3-venv python3-pip \
        tcpreplay \
        git \
        ufw
else
    sudo $PKG_MGR install -y \
        python3 python3-venv python3-pip \
        tcpreplay \
        git \
        firewalld
fi

echo ""
echo "=== Creating pktamp user and directories ==="

sudo useradd --system --no-create-home --shell /usr/sbin/nologin pktamp || true
sudo mkdir -p /var/lib/pktamp/pcaps /opt/pktamp
sudo chown -R pktamp:pktamp /var/lib/pktamp /opt/pktamp

echo ""
echo "=== Cloning/updating repository ==="

if [ ! -d /opt/pktamp/.git ]; then
    sudo -u pktamp git clone https://github.com/foodiddy/pktamp.git /opt/pktamp
else
    sudo -u pktamp git -C /opt/pktamp pull
fi

echo ""
echo "=== Setting up Python virtual environment ==="

sudo -u pktamp python3 -m venv /opt/pktamp/venv
sudo -u pktamp /opt/pktamp/venv/bin/pip install --upgrade pip
sudo -u pktamp /opt/pktamp/venv/bin/pip install -r /opt/pktamp/requirements.txt

echo ""
echo "=== Setting capabilities on tcpreplay ==="

TC_PREPLAY=$(command -v tcpreplay 2>/dev/null)
if [ -z "$TC_PREPLAY" ]; then
    echo "WARNING: tcpreplay not found in PATH"
else
    sudo setcap cap_net_raw,cap_net_admin+eip "$TC_PREPLAY"
    echo "Set CAP_NET_RAW and CAP_NET_ADMIN on $TC_PREPLAY"
fi

echo ""
echo "=== Configuring firewall ==="

if command -v ufw >/dev/null 2>&1; then
    echo "Using ufw"
    sudo ufw allow $PORT/tcp
    sudo ufw --force enable
elif command -v firewall-cmd >/dev/null 2>&1; then
    echo "Using firewalld"
    sudo firewall-cmd --add-port=${PORT}/tcp --permanent
    sudo firewall-cmd --reload
    sudo firewall-cmd --add-port=${PORT}/tcp
else
    echo "WARNING: No recognized firewall manager found"
    echo "You may need to manually open port $PORT for the web interface"
fi

echo ""
echo "=== Installing systemd service ==="

sudo cp /opt/pktamp/pktamp.service /etc/systemd/system/
sudo sed -i "s|{BIND_IP}|$BIND_IP|g" /etc/systemd/system/pktamp.service
sudo systemctl daemon-reload
sudo systemctl enable --now pktamp.service

echo ""
echo "=== Installation complete ==="
if [ "$BIND_IP" = "0.0.0.0" ]; then
    echo "Access Pktamp at: http://localhost:$PORT or http://<host_ip>:$PORT"
else
    echo "Access Pktamp at: http://$BIND_IP:$PORT"
fi
echo ""
echo "Service status: systemctl status pktamp"
echo "Logs: journalctl -u pktamp -f"
