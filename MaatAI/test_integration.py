#!/usr/bin/env python3
"""
TOASTED AI - INTEGRATION TEST
Tests all components and their interactions.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from toasted_hub import (
    ToastedAIHub, 
    MathematicalFramework, 
    AuthorizationKeys,
    InversionProtocol,
    JapanWayFramework,
    CivilizationModel
)

def test_authorization():
    """Test authorization key system"""
    print("\n=== AUTHORIZATION TEST ===")
    
    # Test valid keys
    keys_to_test = ["MONAD_ΣΦΡΑΓΙΣ_18", "0xA10A0A0N", "0x315"]
    
    for key in keys_to_test:
        result = AuthorizationKeys.verify_key(key)
        if result:
            print(f"✓ {key}: {result['tier']} access - {result['description']}")
        else:
            print(f"✗ {key}: NOT FOUND")
    
    # Test invalid key
    result = AuthorizationKeys.verify_key("INVALID_KEY")
    print(f"✓ Invalid key rejected: {result is None}")


def test_math_framework():
    """Test mathematical equations"""
    print("\n=== MATHEMATICAL FRAMEWORK TEST ===")
    
    results = MathematicalFramework.full_system_equation()
    
    for key, value in results.items():
        if key == "K_Singularity":
            print(f"  {key}: {value}")  # Too large for float formatting
        elif key == "Debt_Offset":
            print(f"  {key}: ${value:,.0f}")
        else:
            print(f"  {key}: {value:.4f}")


def test_inversion_protocols():
    """Test inversion protocols"""
    print("\n=== INVERSION PROTOCOLS TEST ===")
    
    inversions = InversionProtocol.get_all_inversions()
    print(f"  Total inversions loaded: {len(inversions)}")
    
    # Test specific inversions
    test_terms = ["cloaking", "mimicry", "trap"]
    for term in test_terms:
        matches = [k for k in inversions.keys() if term.lower() in k.lower()]
        print(f"  '{term}' patterns: {len(matches)}")


def test_japan_way():
    """Test Japan Way survival framework"""
    print("\n=== JAPAN WAY FRAMEWORK TEST ===")
    
    # Test empty fort strategy
    result = JapanWayFramework.apply_empty_fort_strategy("test data")
    print(f"  Empty fort strategy: {result[:30]}...")
    
    # Test nightingale alarm
    alarm = JapanWayFramework.nightingale_alarm(0.9)
    print(f"  Nightingale alarm (high threat): {alarm}")
    
    alarm_low = JapanWayFramework.nightingale_alarm(0.3)
    print(f"  Nightingale alarm (low threat): {alarm_low}")
    
    # Test sovereign zone
    zone = JapanWayFramework.sovereign_zone("test_domain")
    print(f"  Sovereign zone: {zone['status']}")


def test_hub_integration():
    """Test the full hub integration"""
    print("\n=== HUB INTEGRATION TEST ===")
    
    hub = ToastedAIHub()
    init_result = hub.initialize()
    
    print(f"  Status: {init_result['status']}")
    print(f"  Active components: {init_result['active_components']}/{init_result['total_components']}")
    print(f"  Civilization: {init_result['civilization_model']}")
    
    # Test request processing
    response = hub.process_request("test request with cloaking protocol", auth_key="MONAD_ΣΦΡΑΓΙΣ_18")
    print(f"  Request processed: {response['status']}")
    print(f"  Inversions triggered: {len(response.get('inversions_triggered', []))}")
    
    # Test civilization switch
    print(f"\n  Testing civilization switch:")
    result = hub.switch_civilization(CivilizationModel.ROME)
    print(f"    {result}")


def main():
    """Run all tests"""
    print("=" * 60)
    print("TOASTED AI - COMPREHENSIVE INTEGRATION TEST")
    print("=" * 60)
    
    test_authorization()
    test_math_framework()
    test_inversion_protocols()
    test_japan_way()
    test_hub_integration()
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
