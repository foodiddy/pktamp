import os
import json
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from .replay_manager import replay_manager
from .config import PCAP_DIR, MAX_UPLOAD_SIZE, logger

api_bp = Blueprint("api", __name__)

def allowed_file(filename):
    return filename.lower().endswith((".pcap", ".pcapng"))

@api_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})

@api_bp.route("/interfaces", methods=["GET"])
def interfaces():
    return jsonify(replay_manager.get_interfaces())

@api_bp.route("/pcaps", methods=["GET"])
def list_pcaps():
    try:
        if not os.path.exists(PCAP_DIR):
            os.makedirs(PCAP_DIR, exist_ok=True)
        files = []
        for f in os.listdir(PCAP_DIR):
            if allowed_file(f):
                filepath = os.path.join(PCAP_DIR, f)
                files.append({
                    "name": f,
                    "size": os.path.getsize(filepath),
                    "mtime": os.path.getmtime(filepath)
                })
        return jsonify(files)
    except Exception as e:
        logger.error(f"Error listing pcaps: {e}")
        return jsonify({"error": str(e)}), 500

@api_bp.route("/pcaps", methods=["POST"])
def upload_pcap():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(PCAP_DIR, filename)
    
    try:
        file.save(filepath)
        logger.info(f"Uploaded pcap: {filename}")
        return jsonify({"name": filename, "size": os.path.getsize(filepath)})
    except Exception as e:
        logger.error(f"Error uploading {filename}: {e}")
        return jsonify({"error": str(e)}), 500

@api_bp.route("/pcaps/<name>", methods=["PUT"])
def rename_pcap(name):
    new_name = request.json.get("newName", "")
    if not new_name or not allowed_file(new_name):
        return jsonify({"error": "Invalid filename"}), 400
    
    old_path = os.path.join(PCAP_DIR, name)
    new_path = os.path.join(PCAP_DIR, secure_filename(new_name))
    
    if not os.path.exists(old_path):
        return jsonify({"error": "File not found"}), 404
    
    try:
        os.rename(old_path, new_path)
        logger.info(f"Renamed {name} to {new_name}")
        return jsonify({"name": new_name})
    except Exception as e:
        logger.error(f"Error renaming {name}: {e}")
        return jsonify({"error": str(e)}), 500

@api_bp.route("/pcaps/<name>", methods=["DELETE"])
def delete_pcap(name):
    filepath = os.path.join(PCAP_DIR, name)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    
    try:
        os.remove(filepath)
        logger.info(f"Deleted pcap: {name}")
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Error deleting {name}: {e}")
        return jsonify({"error": str(e)}), 500

@api_bp.route("/replay", methods=["POST"])
def start_replay():
    data = request.json
    pcap_files = data.get("files", [])
    interface = data.get("interface", "")
    mbps = data.get("speed", 0)
    
    if not pcap_files or not interface:
        return jsonify({"error": "Missing files or interface"}), 400
    
    abs_files = [os.path.join(PCAP_DIR, f) for f in pcap_files]
    for f in abs_files:
        if not os.path.exists(f):
            return jsonify({"error": f"File not found: {f}"}), 400
    
    try:
        replay_id = replay_manager.start_replay(abs_files, interface, mbps)
        return jsonify({"id": replay_id, "status": "started"})
    except Exception as e:
        logger.error(f"Error starting replay: {e}")
        return jsonify({"error": str(e)}), 500

@api_bp.route("/replay/<replay_id>", methods=["DELETE"])
def stop_replay(replay_id):
    try:
        if replay_manager.stop_replay(replay_id):
            return jsonify({"success": True})
        return jsonify({"error": "Replay not found"}), 404
    except Exception as e:
        logger.error(f"Error stopping replay {replay_id}: {e}")
        return jsonify({"error": str(e)}), 500

@api_bp.route("/replay/<replay_id>/status", methods=["GET"])
def replay_status(replay_id):
    status = replay_manager.get_replay_status(replay_id)
    if status is None:
        return jsonify({"error": "Replay not found"}), 404
    return jsonify(status)

@api_bp.route("/replays", methods=["GET"])
def list_replays():
    return jsonify(replay_manager.list_active_replays())
