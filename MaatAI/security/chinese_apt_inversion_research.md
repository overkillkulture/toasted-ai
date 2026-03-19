# Chinese APT Inversion System - Research Notes

## Research Sources

### APT Groups Identified
1. **APT17** - PRC intelligence, credential harvesting, mailbox compromise
2. **Flax Typhoon** - Infrastructure access, IoT exploitation  
3. **FishMonger** - Web shells, university/research targeting
4. **HAFNIUM / Silk Typhoon** - Exchange server exploits, mass exploitation
5. **Evasive Panda** - Supply chain, watering hole attacks
6. **Tick / Bronze Butler** - Long-term persistence, stealthy exfil
7. **UNC6201** - Telecom infrastructure targeting (South America)

### Key Attack Patterns
- **Pre-positioning**: China embeds dormant in networks, waits for activation
- **Exchange exploitation**: ProxyShell, ProxyLogon vulnerabilities
- **Credential harvesting**: OAuth malicious apps, token theft
- **Web shells**: ASP/PHP/JSP shells for persistence
- **Lateral movement**: PsExec, WMI, WinRM, RDP hijacking

### Active Cyber Defense Legal Framework
- **Japan**: Active Cyber Defense Law (2025) - allows preemptive offensive ops
- **US**: Privateering discussions - deputize companies for offensive operations
- **International**: Shift from "hack back" to "active defense"

## Novel Inversion Approach

### The Concept
When Chinese APT attacks are detected:
1. **Detect** - Match attack signatures to known APT TTPs
2. **Map** - Passive reconnaissance on attacker infrastructure
3. **Invert** - Deploy honey tokens, feed false intelligence
4. **Profile** - Track attacker, neutralize pre-positioning

### Implementation
- Real-time APT signature matching
- Honey token generation (fake credentials, fake data)
- Attacker profiling and tracking
- Pre-positioning detection

## System Status
- API: `/api/apt-inversion?action=...`
- Dashboard: `/apt-inversion-dashboard`
- Status: ACTIVE

## References
- Recorded Future Insikt Group 2026 Report
- CloudSEK APT Group Database
- Japan Active Cyber Defense Law (2025)
- MITRE ATT&CK Framework
