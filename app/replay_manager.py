import os
import subprocess
import uuid
from psutil import net_if_addrs
from .config import PCAP_DIR, logger

class ReplayManager:
    def __init__(self):
        self.active_replays = {}

    def get_interfaces(self):
        interfaces = []
        for iface, addrs in net_if_addrs().items():
            display_name = "Loopback" if iface == "lo" else iface
            interfaces.append({"name": iface, "display": display_name})
        return interfaces

    def start_replay(self, pcap_files, interface, mbps):
        replay_id = str(uuid.uuid4())
        cmd = ["tcpreplay"]
        cmd.extend(["--intf1", interface])
        if mbps > 0:
            cmd.extend(["--mbps", str(mbps)])
        cmd.extend(pcap_files)
        
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        self.active_replays[replay_id] = {
            "process": proc,
            "pcap_files": pcap_files,
            "interface": interface,
            "speed_mbps": mbps,
            "status": "running"
        }
        logger.info(f"Started replay {replay_id} on {interface} at {mbps} Mbps")
        return replay_id

    def stop_replay(self, replay_id):
        if replay_id in self.active_replays:
            proc = self.active_replays[replay_id]["process"]
            proc.terminate()
            proc.wait(timeout=5)
            del self.active_replays[replay_id]
            logger.info(f"Stopped replay {replay_id}")
            return True
        return False

    def get_replay_status(self, replay_id):
        if replay_id not in self.active_replays:
            return None
        return self.active_replays[replay_id]

    def list_active_replays(self):
        return {rid: info for rid, info in self.active_replays.items()}

replay_manager = ReplayManager()
