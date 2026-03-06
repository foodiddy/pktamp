# Pktamp - Web interface for packet capture replays

## Overview

Pktamp provides a Winamp-themed web interface for managing and replaying packet capture files using tcpreplay.

## Installation

```bash
./install.sh
```

The installer:
- Detects your Linux distribution (Debian/Ubuntu or RHEL/CentOS/AlmaLinux)
- Installs required packages (Python, tcpreplay, pip, git)
- Creates the `pktamp` system user
- Configures TCP_REPLAY capabilities
- Sets up the systemd service
- Configures firewall (ufw or firewalld)

## Usage

Access the web interface at: **http://<bind_ip>:8080**

### File Management
- Upload `.pcap` or `.pcapng` files
- Rename or delete files via API

### Replay
1. Select one or more packet captures
2. Choose network interface (including loopback)
3. Set replay speed (0 = unlimited, up to 10 Gbps)
4. Click START
5. Click STOP to pause

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ping` | Health check |
| GET | `/api/interfaces` | List interfaces |
| GET | `/api/pcaps` | List pcap files |
| POST | `/api/pcaps` | Upload pcap |
| PUT | `/api/pcaps/<name>` | Rename pcap |
| DELETE | `/api/pcaps/<name>` | Delete pcap |
| POST | `/api/replay` | Start replay |
| DELETE | `/api/replay/<id>` | Stop replay |
| GET | `/api/replay/<id>/status` | Replay status |

## Docker

Not yet implemented. Consider using.

## License

CC0 1.0 Universal

## Author

Original author: Scott Hall (foodiddy)
