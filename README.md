# pktamp

Web interface for packet capture replays

## About

Pktamp provides a Winamp-styled web interface for managing and replaying packet capture files using tcpreplay.

## Features

- Upload packet capture files (`.pcap`, `.pcapng`)
- Manage stored files (rename, delete)
- Select network interface for replay (including loopback)
- Adjust replay speed from 0 (unlimited) to 10 Gbps in 0.5 Mbps increments
- Start/stop replay
- Replay multiple packet captures simultaneously

## Requirements

- Linux system (Debian/Ubuntu or RHEL/CentOS/AlmaLinux)
- Python 3.11+
- tcpreplay
- Root/sudo access for installation

## Installation

Run the installation script:

```bash
./install.sh
```

The script will:
1. Detect your Linux distribution
2. Install required packages
3. Create the `pktamp` user
4. Set up file permissions
5. Configure capabilities for tcpreplay
6. Set up the firewall (ufw or firewalld)
7. Install and enable the systemd service

The installer will ask for the IP address to bind to (default: 127.0.0.1).

## Usage

Access the web interface at `http://<bind_ip>:8080`

### File Management

- Click "Upload" or drag files to the upload area
- Click a file in the playlist to select it
- Click "Delete" to remove selected files

### Replay

1. Select one or more packet capture files
2. Choose the network interface from the dropdown
3. Set the replay speed using the slider (0 = unlimited)
4. Click "START" to begin replay
5. Click "STOP" to stop replay

## API

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/ping` | Health check |
| GET | `/api/interfaces` | List available network interfaces |
| GET | `/api/pcaps` | List stored packet captures |
| POST | `/api/pcaps` | Upload a packet capture |
| PUT | `/api/pcaps/<name>` | Rename a packet capture |
| DELETE | `/api/pcaps/<name>` | Delete a packet capture |
| POST | `/api/replay` | Start replay |
| DELETE | `/api/replay/<id>` | Stop replay |
| GET | `/api/replay/<id>/status` | Get replay status |
| GET | `/api/replays` | List active replays |

## Directory Structure

```
/opt/pktamp/
├── app/                 # Flask application
├── static/             # Static files (CSS, JS)
├── templates/          # HTML templates
├── venv/               # Python virtual environment
└── pktamp.service      # Systemd unit file
```

```
/var/lib/pktamp/
└── pcaps/              # Stored packet capture files
```

## License

CC0 1.0 Universal (Public Domain Dedication)
