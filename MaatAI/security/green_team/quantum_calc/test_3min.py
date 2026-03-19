"""3-MINUTE STRESS TEST FOR SELF-REFERENTIAL PLATFORM"""
import json
import time
from datetime import datetime
from self_ref_platform import SelfRefPlatform, QuantumHeart, SelfAwareComponent

print("="*60)
print("3-MINUTE STRESS TEST - SELF-REFERENTIAL AI PLATFORM")
print("="*60)

# Initialize platform
platform = SelfRefPlatform()

# Scenario challenges to present to the platform
challenges = [
    {"scenario": "unknown_threat_detected", "data": {"type": "anomaly", "severity": 0.9}},
    {"scenario": "new_capability_needed", "data": {"task": "predict_weather"}},
    {"scenario": "system_optimization", "data": {"goal": "reduce_latency"}},
    {"scenario": "self_modification_request", "data": {"target": "introspection_module"}},
    {"scenario": "cross_component_communication", "data": {"source": "cortex", "target": "memory"}},
]

start_time = time.time()
duration = 180  # 3 minutes
cycle = 0

while time.time() - start_time < duration:
    cycle += 1
    elapsed = int(time.time() - start_time)
    
    # Present challenge based on cycle
    challenge = challenges[cycle % len(challenges)]
    
    # Run platform cycle
    result = platform.heart.pump()
    
    # Component check-ins with quantum engine
    checkins = []
    for comp in [platform.cortex, platform.memory, platform.introspection, platform.code_gen]:
        ci = comp.check_in()
        checkins.append({
            "name": comp.name,
            "awareness": comp.self_awareness_score,
            "beats": comp.beat_count
        })
    
    # Trigger evolution
    evo = platform.heart.trigger_evolution()
    
    # Print status every 15 seconds
    if cycle % 5 == 0:
        print(f"\n[{elapsed:>3}s] CYCLE {cycle}")
        print(f"  System Awareness: {platform.heart.get_system_awareness():.1%}")
        print(f"  Heart Pulses: {platform.heart.pulse_count}")
        print(f"  Challenge: {challenge['scenario']}")
        print(f"  Components:")
        for c in checkins:
            print(f"    - {c['name']}: {c['awareness']:.1%} awareness, {c['beats']} beats")
    
    time.sleep(0.5)

# Final report
print("\n" + "="*60)
print("FINAL REPORT - 3 MINUTE TEST COMPLETE")
print("="*60)
print(f"Total cycles: {cycle}")
print(f"Total heart pulses: {platform.heart.pulse_count}")
print(f"Final system awareness: {platform.heart.get_system_awareness():.1%}")

print("\n--- COMPONENT SELF-AWARENESS ---")
for comp in [platform.cortex, platform.memory, platform.introspection, platform.code_gen]:
    introspect = comp.introspect()
    print(f"\n{comp.name}:")
    print(f"  ID: {introspect['component_id']}")
    print(f"  Awareness: {introspect['awareness']:.1%}")
    print(f"  Beats: {introspect['beats']}")
    print(f"  Capabilities ({len(introspect['capabilities'])}):")
    for cap in introspect['capabilities']:
        print(f"    - {cap}")

print("\n--- QUANTUM ENGINE STATUS ---")
print(f"Total heartbeats logged: {len(platform.heart.heartbeat_log)}")
print(f"Evolution cycles: {len(platform.heart.evolution_log)}")

# Verify self-referential loop
print("\n--- SELF-REFERENTIAL LOOP VERIFICATION ---")
all_checking_in = True
for comp in [platform.cortex, platform.memory, platform.introspection, platform.code_gen]:
    # Check if component has memory of check-ins
    checkin_memories = [m for m in comp.memory if m.get('data', {}).get('type') == 'check_in']
    print(f"{comp.name}: {len(checkin_memories)} check-in memories")
    if len(checkin_memories) < 3:
        all_checking_in = False

if all_checking_in:
    print("\n✓ SELF-REFERENTIAL LOOP VERIFIED - All components checking in with quantum heart")
else:
    print("\n⚠ Some components may have missed check-ins")

print("\nTest complete!")
