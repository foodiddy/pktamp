# Installation Guide for Pktamp

## Prerequisites

- Linux system (Debian/Ubuntu or RHEL/CentOS/AlmaLinux)
- Root or sudo access
- Internet access (for package installation)
- tcpreplay installed (will be installed by script)

## Installation

Run the installer script:

```bash
./install.sh
```

### Installation Process

1. **Distribution Detection**  
   The script automatically detects whether you're running Debian/Ubuntu or RHEL/CentOS/AlmaLinux.

2. **Package Installation**  
   The script installs:
   - Python 3 and pip
   - tcpreplay
   - Git
   - Firewall manager (ufw or firewalld)

3. **User and Directory Setup**  
   - Creates system user `pktamp` (no login shell)
   - Creates directories:
     - `/opt/pktamp` - application code
     - `/var/lib/pktamp/pcaps` - packet captures storage

4. **Python Environment**  
   - Creates Python virtual environment
   - Installs dependencies from `requirements.txt`

5. **Capabilities Setup**  
   Sets `CAP_NET_RAW` and `CAP_NET_ADMIN` on tcpreplay so it can open raw sockets without running as root.

6. **Firewall Configuration**  
   - Detects whether `ufw` or `firewalld` is active
   - Opens port 8080 for Web UI access

7. **Systemd Service**  
   Installs and enables `pktamp.service` to run at boot.

### Post-Installation

Check service status:
```bash
systemctl status pktamp
```

View logs:
```bash
journalctl -u pktamp -f
```

Access the web UI at `http://<bind_ip>:8080`

## Uninstallation

1. Stop and disable the service:
   ```bash
   sudo systemctl stop pktamp
   sudo systemctl disable pktamp
   ```

2. Remove systemd unit:
   ```bash
   sudo rm /etc/systemd/system/pktamp.service
   sudo systemctl daemon-reload
   ```

3. Remove user and directories:
   ```bash
   sudo userdel pktamp
   sudo rm -rf /opt/pktamp /var/lib/pktamp
   ```

4. Remove firewall rules (if needed):
   ```bash
   sudo ufw delete allow 8080/tcp
   # OR for firewalld:
   sudo firewall-cmd --remove-port=8080/tcp --permanent
   sudo firewall-cmd --reload
   ```

## Troubleshooting

### Service won't start

Check logs:
```bash
journalctl -u pktamp -n 50
```

Verify capabilities:
```bash
getcap $(which tcpreplay)
```

### Cannot access web UI

- Ensure the firewall permits traffic on port 8080
- Check that the service is running: `systemctl status pktamp`
- Verify the bind IP is correct: `grep LISTEN_IP /etc/systemd/system/pktamp.service`

### tcpreplay permission denied

Re-run capability setup:
```bash
sudo setcap cap_net_raw,cap_net_admin+eip $(which tcpreplay)
```

## Firewall Ports

The following port must be open:
- **8080/TCP** - Web UI

If running on a specific IP (e.g., management interface), ensure that IP is accessible from your client.
