import hashlib
import os
import json
import sys

# Color codes terminal me RED aur GREEN alert dikhane ke liye
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

SECURITY_DB = "security_registry.json"

class IntrusionDetectionSystem:
    @staticmethod
    def calculate_file_checksum(filepath):
        """
        SHA-256 Checksum: Yeh file ka unique biometric fingerprint nikalta hai.
        Agar file me 1 space ya character bhi badla, toh fingerprint badal jayega.
        """
        if not os.path.exists(filepath):
            return None

        hasher = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                # Chunk me read karte hain taaki file badi hone par memory crash na ho
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return None

    @classmethod
    def register_file_state(cls, filepath):
        """
        System Authorization: Kisi transaction ke baad jab data legally save hota hai, 
        toh yeh naye legal checksum ko approve (register) karta hai.
        """
        current_checksum = cls.calculate_file_checksum(filepath)
        if not current_checksum:
            return

        registry = {}
        if os.path.exists(SECURITY_DB):
            try:
                with open(SECURITY_DB, 'r') as f:
                    registry = json.load(f)
            except json.JSONDecodeError:
                pass

        registry[filepath] = current_checksum

        with open(SECURITY_DB, 'w') as f:
            json.dump(registry, f, indent=4)

    @classmethod
    def scan_system_integrity(cls, filepath):
        """
        [THE ANTIVIRUS SCANNER]
        Har boot up ya read operation se pehle yeh function check karega 
        ki file external modify toh nahi ki gayi.
        """
        if not os.path.exists(filepath):
            # File abhi bani hi nahi hai (Initial State), no alarm needed.
            return True

        if not os.path.exists(SECURITY_DB):
            print(f"{YELLOW}[IDS WARNING] Security registry missing. Registering current state as baseline.{RESET}")
            cls.register_file_state(filepath)
            return True

        with open(SECURITY_DB, 'r') as f:
            registry = json.load(f)

        expected_checksum = registry.get(filepath)
        actual_checksum = cls.calculate_file_checksum(filepath)

        if expected_checksum != actual_checksum:
            print(f"\n{RED}🚨 [CRITICAL BREACH DETECTED] 🚨")
            print(f"Unauthorized modification detected in: '{filepath}'")
            print(f"Expected Fingerprint: {expected_checksum}")
            print(f"Actual Fingerprint:   {actual_checksum}{RESET}")
            print(f"{RED}[SECURITY ACTION] Freezing node execution to prevent chain corruption!{RESET}\n")
            # Attacker ko false data process karne se rokne ke liye program exit kar do
            sys.exit(1)
            return False

        print(f"{GREEN}[IDS OK] Integrity verified for '{filepath}'. No signs of tampering.{RESET}")
        return True
