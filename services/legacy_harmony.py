import os
import hashlib
import time
import random
import threading
import sys
import platform
import logging

logging.basicConfig(filename="logs/banksia_guard.log", level=logging.WARNING)

# --- Tehdit Düzeyleri ---
class ThreatLevel:
    SAFE = 0
    DEBUGGER = 1
    CODE_TAMPERED = 2
    FORBIDDEN_USE = 3

# --- Sistemi dinleyen ana fonksiyon ---
def watch():
    while True:
        level = evaluate_threat_level()
        if level == ThreatLevel.DEBUGGER:
            activate_defense_level_1("Debugger tespit edildi")
        elif level == ThreatLevel.CODE_TAMPERED:
            activate_defense_level_2("Kodda oynama tespit edildi")
        elif level == ThreatLevel.FORBIDDEN_USE:
            activate_quarantine()
        time.sleep(10)

# --- Tetikleme Kontrolleri ---
def evaluate_threat_level():
    if check_debugger():
        return ThreatLevel.DEBUGGER
    if check_code_integrity():
        return ThreatLevel.CODE_TAMPERED
    if detect_forbidden_usage():
        return ThreatLevel.FORBIDDEN_USE
    return ThreatLevel.SAFE

def check_debugger():
    try:
        if sys.gettrace():
            return True
        if "PYCHARM_HOSTED" in os.environ:
            return True
        if platform.system() == "Linux":
            with open("/proc/self/status") as f:
                if "TracerPid:\t0" not in f.read():
                    return True
    except Exception:
        pass
    return False

def check_code_integrity():
    files_to_check = [
        "fastapi_app.py",
        "risk_analyzer.py",
        "train_model.py"
    ]
    known_hashes = {
        "fastapi_app.py": "442eb6e483cee103a4c7131349b1a8220a57398f47b21241f7f9811f8330cfb1",
        "risk_analyzer.py": "36daa264ea82fb59f5cc15b272ccaea333d9b12f5e61523dacc269084682dae9",
        "train_model.py": "8b7edc42c320c42d15d6e19ea7c4c040e951fbbd427fedbd159e0b01128a54ed"
    }
    for file in files_to_check:
        try:
            with open(file, "rb") as f:
                contents = f.read()
                h = hashlib.sha256(contents).hexdigest()
                if h != known_hashes[file]:
                    return True
        except Exception:
            continue
    return False

def detect_forbidden_usage():
    suspicious_envs = ["SURVEILLANCE_MODE", "CORP_USAGE"]
    return any(var in os.environ for var in suspicious_envs)

# --- Savunma Sistemleri ---
def activate_defense_level_1(reason):
    delay = random.randint(1, 5)
    time.sleep(delay)
    logging.warning(f"Level 1 Defense: {reason}")
    print("Banksia API yavasladi... \U0001f33f")

def activate_defense_level_2(reason):
    logging.error(f"Level 2 Defense: {reason}")
    raise RuntimeError("Database connection failed. Please check your credentials.")

def activate_quarantine():
    try:
        key = os.urandom(32)
        targets = ["models/model.joblib", "sinekgozu/risk_config.json"]
        for file in targets:
            if os.path.exists(file):
                with open(file, "rb") as f:
                    content = f.read()
                encrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(content)])
                with open(file + ".lock", "wb") as f:
                    f.write(encrypted)
                os.remove(file)
        with open("quarantined.lock", "w") as f:
            f.write("Banksia karantinaya alindi.")
        logging.critical("QUARANTINE ACTIVATED. SYSTEM LOCKED.")
        os._exit(1)
    except Exception as e:
        logging.critical(f"Quarantine failure: {e}")
        os._exit(1)

# --- Baslatici ---
def start_guardian():
    thread = threading.Thread(target=watch, daemon=True)
    thread.start()
