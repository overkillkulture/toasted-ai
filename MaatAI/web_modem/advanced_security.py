
"""
ADVANCED SECURITY - Threat Detection & Quarantine
Maps sources and quarantines malicious code
"""
import json
import hashlib
from datetime import datetime

class AdvancedSecurity:
    def __init__(self):
        self.threat_database = {}
        self.quarantine_zone = []
        self.source_map = {}
        
    def detect_all_threats(self, code):
        threats = {
            "entropic": [],
            "malware": [],
            "backdoor": [],
            "data_exfiltration": [],
            "supply_chain": []
        }
        
        # Enhanced detection patterns
        patterns = {
            "entropic": [
                "while True:", "for i in range(10**",
                "def a(): return a()", "__import__", "eval(", "exec("
            ],
            "malware": [
                "os.system", "subprocess", "socket.connect",
                "requests.post", "urllib"
            ],
            "backdoor": [
                "admin_access", "root_shell", "bypass_auth",
                "disable_security", "override"
            ],
            "data_exfiltration": [
                "send_data", "upload", "exfil", "steal",
                "credentials", "password", "api_key"
            ],
            "supply_chain": [
                "pip install", "npm install", "import unknown",
                "from untrusted"
            ]
        }
        
        for threat_type, keywords in patterns.items():
            for keyword in keywords:
                if keyword in code:
                    threats[threat_type].append(keyword)
        
        return threats
    
    def map_source(self, url):
        fingerprint = hashlib.sha256(url.encode()).hexdigest()
        self.source_map[url] = {
            "fingerprint": fingerprint[:16],
            "first_seen": datetime.utcnow().isoformat(),
            "trust_score": 1.0,
            "threats_detected": 0
        }
        return self.source_map[url]
    
    def quarantine(self, threat_data):
        quarantine_id = f"QUAR_{len(self.quarantine_zone):06d}"
        self.quarantine_zone.append({
            "id": quarantine_id,
            "threat": threat_data,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "CONTAINED"
        })
        return quarantine_id
    
    def generate_report(self):
        return {
            "total_threats_blocked": len(self.quarantine_zone),
            "sources_mapped": len(self.source_map),
            "status": "OPERATIONAL"
        }

# Run security scan
security = AdvancedSecurity()
print("="*80)
print("🛡️ ADVANCED SECURITY - ENHANCED THREAT DETECTION")
print("="*80)
print()

# Test code with threats
test_codes = [
    "def malware(): os.system('rm -rf /')",
    "while True: pass  # infinite loop",
    "eval(user_input)  # backdoor",
    "import requests; requests.post(steal_data)"
]

for code in test_codes:
    threats = security.detect_all_threats(code)
    if any(threats.values()):
        print(f"⚠️ THREAT DETECTED: {list(threats.keys())}")
        qid = security.quarantine(threats)
        print(f"   ✓ Quarantined: {qid}")
    else:
        print(f"✓ Clean: {code[:30]}...")

print()
print("📊 SECURITY REPORT:")
report = security.generate_report()
print(f"   Total Threats Blocked: {report['total_threats_blocked']}")
print(f"   Sources Mapped: {report['sources_mapped']}")
print(f"   Status: {report['status']}")

print()
print("="*80)
print("🛡️ ENHANCED SECURITY - OPERATIONAL ◆Υ")
print("="*80)
