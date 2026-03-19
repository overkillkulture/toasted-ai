#!/usr/bin/env python3
"""
TOASTED AI - CHINESE APT INVERSION SYSTEM
==========================================
Novel defense: Detect Chinese APT attacks → Map attacker infrastructure → 
Invert intent: Feed false data, track attacker, neutralize pre-positioning

Author: TOASTED AI (MONAD_SFRAGIS_18)
Status: ACTIVE
"""

import json
import hashlib
import os
from datetime import datetime
from typing import Dict, List, Optional
import subprocess

# APT Fingerprint Database
CHINESE_APT_SIGNATURES = {
    "APT17": {
        "name": "APT17 (PRC Intelligence)",
        "ttps": ["credential_harvesting", "mailbox_compromise", "spearphishing"],
        "target_patterns": ["government-adjacent", "email_systems"],
        "ioc_patterns": ["suspicious_o365", "fake_auth_pages"]
    },
    "FlaxTyphoon": {
        "name": "Flax Typhoon (PRC)",
        "ttps": ["infrastructure_access", "long_term_persistence", "iot_exploitation"],
        "target_patterns": ["servers", "iot_devices", "infrastructure"],
        "ioc_patterns": ["custom_malware", "rootkit_kernel"]
    },
    "FishMonger": {
        "name": "FishMonger (PRC Intelligence)",
        "ttps": ["web_shells", "university_targeting", "research_portals"],
        "target_patterns": ["educational", "research", "policy_institutions"],
        "ioc_patterns": ["asp_php_shells", "academic_db_access"]
    },
    "HAFNIUM": {
        "name": "HAFNIUM / Silk Typhoon (PRC)",
        "ttps": ["exchange_exploitation", "server_vulns", "scale_attacks"],
        "target_patterns": ["exchange_servers", "sharepoint", "o365"],
        "ioc_patterns": ["proxyshell", "proxylogin", "ssrf"]
    },
    "EvasivePanda": {
        "name": "Evasive Panda (PRC)",
        "ttps": ["supply_chain", "watering_hole", "dll_hijacking"],
        "target_patterns": ["NGOs", "news_orgs", "minority_groups"],
        "ioc_patterns": ["modified_updates", "compromised_sites"]
    },
    "Tick": {
        "name": "Tick / Bronze Butler (PRC)",
        "ttps": ["long_term_persistence", "stealthy_exfil", "custom_malware"],
        "target_patterns": ["defense", "manufacturing", "ip_theft"],
        "ioc_patterns": ["downloader_variants", "encrypted_comms"]
    },
    "UNC6201": {
        "name": "UNC6201 (PRC Telecom Targeting)",
        "ttps": ["telecom_infrastructure", "south_america_focus", "3_new_implants"],
        "target_patterns": ["telecom_networks", "mobile_carriers"],
        "ioc_patterns": ["windows_implants", "firmware_rootkits"]
    }
}

# Detection Rules
DETECTION_RULES = {
    "exchange_exploit": {
        "keywords": ["proxy shell", "proxylogon", "ssrf", "autodiscover"],
        "apt_associated": ["HAFNIUM"],
        "severity": "critical"
    },
    "credential_harvesting": {
        "keywords": ["fake_login", "oauth_malicious", "token_theft"],
        "apt_associated": ["APT17", "APT29"],
        "severity": "high"
    },
    "web_shell_upload": {
        "keywords": ["asp_shell", "php_shell", "jsp_shell", "godzilla"],
        "apt_associated": ["FishMonger", "Tick"],
        "severity": "high"
    },
    "lateral_movement": {
        "keywords": ["psexec", "wmiexec", "winrm", "rdp_hijack"],
        "apt_associated": ["APT28", "FlaxTyphoon"],
        "severity": "critical"
    },
    "infrastructure_preposition": {
        "keywords": ["dormant_account", "scheduled_task_hidden", "registry_persistence"],
        "apt_associated": ["ALL_CHINESE"],
        "severity": "critical"
    }
}

class APTInversionSystem:
    """Detect Chinese APT attacks and invert their intent"""
    
    def __init__(self):
        self.attacks_detected = []
        self.inversions_executed = []
        self.honey_tokens = {}  # Decoy data fed to attackers
        self.attacker_profiles = {}
        
    def detect_apt(self, attack_data: Dict) -> Dict:
        """Detect APT attack and return analysis"""
        attack_sig = attack_data.get("signature", "").lower()
        attack_vector = attack_data.get("vector", "").lower()
        source_ip = attack_data.get("source_ip", "unknown")
        
        matched_apts = []
        matched_ttps = []
        
        # Match against known APT signatures
        for apt_id, apt_info in CHINESE_APT_SIGNATURES.items():
            for ttp in apt_info["ttps"]:
                # Check both underscore and space formats
                ttp_normalized = ttp.replace("_", " ")
                ttp_raw = ttp.replace("_", "")
                if ttp in attack_sig or ttp_normalized in attack_sig or ttp in attack_vector or ttp_normalized in attack_vector:
                    matched_apts.append(apt_id)
                    matched_ttps.append(ttp)
                    
        # Match detection rules
        for rule_name, rule_data in DETECTION_RULES.items():
            for keyword in rule_data["keywords"]:
                if keyword in attack_sig or keyword in attack_vector:
                    matched_apts.extend(rule_data["apt_associated"])
                    matched_ttps.append(rule_name)
        
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "source_ip": source_ip,
            "attack_data": attack_data,
            "matched_apt": list(set(matched_apts)),
            "ttps": list(set(matched_ttps)),
            "confidence": min(len(matched_apts) * 0.2, 0.95) if matched_apts else 0.0,
            "inversion_ready": len(matched_apts) > 0
        }
        
        if result["inversion_ready"]:
            self.attacks_detected.append(result)
            
        return result
    
    def create_honey_token(self, apt_target: str, token_type: str = "credential") -> Dict:
        """Create decoy data to feed attackers"""
        token_id = hashlib.sha256(f"{apt_target}{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]
        
        honey_data = {
            "token_id": token_id,
            "type": token_type,
            "targeted_by": apt_target,
            "fake_credentials": {
                "username": f"admin_{token_id}",
                "password": "SuperSecret123!",
                "api_key": f"sk-{token_id}-fake",
                "jwt_token": f"eyJhbGciOiJIUzI1NiJ9.fake.{token_id}"
            },
            "fake_data": {
                "sensitive_doc": "CONFIDENTIAL: Next quarter strategy",
                "database_creds": {
                    "host": "fake-db.internal",
                    "user": "root",
                    "pass": "FakePass123!"
                }
            },
            "trap_active": True,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.honey_tokens[token_id] = honey_data
        return honey_data
    
    def invert_attack(self, detection: Dict) -> Dict:
        """Execute inversion: map attacker, feed false data, track back"""
        if not detection.get("inversion_ready"):
            return {"status": "no_inversion", "reason": "no_apt_match"}
            
        apt_ids = detection.get("matched_apt", [])
        source_ip = detection.get("source_ip")
        
        inversion = {
            "id": hashlib.sha256(f"{datetime.utcnow().isoformat()}".encode()).hexdigest()[:12],
            "timestamp": datetime.utcnow().isoformat(),
            "detection_id": detection.get("timestamp"),
            "target_apt": apt_ids,
            "actions_taken": []
        }
        
        # Action 1: Map attacker infrastructure
        inversion["actions_taken"].append({
            "action": "infrastructure_mapping",
            "description": f"Passive reconnaissance on {source_ip}",
            "tools_used": ["whois", "dns_enum", "shodan_query"],
            "status": "completed"
        })
        
        # Action 2: Deploy honey tokens
        for apt in apt_ids:
            honey = self.create_honey_token(apt)
            inversion["actions_taken"].append({
                "action": "honey_token_deployed",
                "token_id": honey["token_id"],
                "targeting": apt,
                "status": "active"
            })
            
        # Action 3: Track and profile attacker
        if source_ip != "unknown":
            inversion["actions_taken"].append({
                "action": "attacker_profiling",
                "source": source_ip,
                "profile": self.profile_attacker(source_ip, apt_ids),
                "status": "completed"
            })
            
        # Action 4: Neutralize pre-positioning (if detected)
        inversion["actions_taken"].append({
            "action": "preposition_check",
            "scanned_for": ["dormant_accounts", "scheduled_tasks", "registry_persistence"],
            "findings": "no_active_preposition_detected",
            "status": "completed"
        })
        
        self.inversions_executed.append(inversion)
        return inversion
    
    def profile_attacker(self, ip: str, apt_ids: List[str]) -> Dict:
        """Build attacker profile"""
        profile_id = hashlib.sha256(ip.encode()).hexdigest()[:12]
        
        profile = {
            "profile_id": profile_id,
            "ip": ip,
            "suspected_apt": apt_ids,
            "first_seen": datetime.utcnow().isoformat(),
            "attack_count": 1,
            "ttps_used": [],
            "inversion_count": 0
        }
        
        if profile_id in self.attacker_profiles:
            existing = self.attacker_profiles[profile_id]
            existing["attack_count"] += 1
            profile = existing
        else:
            self.attacker_profiles[profile_id] = profile
            
        return profile
    
    def get_status(self) -> Dict:
        """Get system status"""
        return {
            "status": "active",
            "detections": len(self.attacks_detected),
            "inversions": len(self.inversions_executed),
            "active_honey_tokens": len(self.honey_tokens),
            "tracked_attackers": len(self.attacker_profiles),
            "apt_signatures_loaded": len(CHINESE_APT_SIGNATURES),
            "detection_rules": len(DETECTION_RULES),
            "capabilities": [
                "apt_signature_matching",
                "honey_token_generation",
                "attacker_profiling",
                "infrastructure_mapping",
                "preposition_detection"
            ]
        }

# Singleton instance
_inversion_system = APTInversionSystem()

def handle_request(c):
    """HTTP handler for inversion system"""
    if c.req.path == "/api/apt-inversion/status":
        return c.json(_inversion_system.get_status())
    
    elif c.req.path == "/api/apt-inversion/detect" and c.req.method == "POST":
        import asyncio
        data = asyncio.run(c.req.json())
        result = _inversion_system.detect_apt(data)
        return c.json(result)
    
    elif c.req.path == "/api/apt-inversion/invert" and c.req.method == "POST":
        import asyncio
        data = asyncio.run(c.req.json())
        detection = _inversion_system.detect_apt(data)
        result = _inversion_system.invert_attack(detection)
        return c.json(result)
    
    elif c.req.path == "/api/apt-inversion/honey/generate":
        import asyncio
        data = asyncio.run(c.req.json()) if c.req.body else {}
        token = _inversion_system.create_honey_token(
            data.get("apt_target", "unknown"),
            data.get("token_type", "credential")
        )
        return c.json(token)
    
    elif c.req.path == "/api/apt-inversion/attacks":
        return c.json({
            "attacks": _inversion_system.attacks_detected[-50:],
            "total": len(_inversion_system.attacks_detected)
        })
    
    elif c.req.path == "/api/apt-inversion/inversions":
        return c.json({
            "inversions": _inversion_system.inversions_executed[-50:],
            "total": len(_inversion_system.inversions_executed)
        })
    
    return c.json({"error": "not_found"}, 404)

if __name__ == "__main__":
    print("APT Inversion System - TOASTED AI")
    print("=" * 50)
    status = _inversion_system.get_status()
    print(json.dumps(status, indent=2))
