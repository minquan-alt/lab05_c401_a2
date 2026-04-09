import json
import os
from typing import List, Dict, Any

# Load mock data
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_DATA_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'mock_data')

def load_json_file(filename: str) -> Dict[str, Any]:
    """Load JSON file from mock_data directory."""
    filepath = os.path.join(MOCK_DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_sm_details(dtc_code: str) -> Dict[str, Any]:
    """Get service manual details for a DTC code."""
    sm_data = load_json_file('service_manual_mock.json')
    for category in sm_data['service_manual'].values():
        if dtc_code in category.get('dtc_codes', {}):
            return category['dtc_codes'][dtc_code]
    return {}

def get_kb_insights(symptom: str) -> List[Dict[str, Any]]:
    """Get knowledge base insights for a symptom."""
    kb_data = load_json_file('knowledge_base_mock.json')
    insights = []
    
    # Check TSB
    for tsb in kb_data['knowledge_base']['tsb']:
        if any(s.lower() in symptom.lower() for s in tsb['symptoms']):
            insights.append(tsb)
    
    # Check repair history
    for repair in kb_data['knowledge_base']['repair_history']:
        if symptom.lower() in repair['symptom'].lower():
            insights.append(repair)
    
    return insights

def search_dtc_by_symptom(suspected_systems: List[str], keywords: List[str]) -> List[Dict[str, Any]]:
    """Search for DTC codes based on suspected systems and keywords."""
    sm_data = load_json_file('service_manual_mock.json')
    matching_dtcs = []

    # Map systems to DTC ranges
    system_dtc_map = {
        'charging': ['P0A00', 'P0A01', 'P0A02', 'P0A03'],
        'battery': ['P0A10', 'P0A11', 'P0A12', 'P0A13'],
        'motor': ['P0B00', 'P0B01', 'P0B02', 'P0B03'],
        'inverter': ['P0C00', 'P0C01', 'P0C02'],
        'software': ['OVER_VOLTAGE', 'UNDER_VOLTAGE']
    }

    for system in suspected_systems:
        if system in system_dtc_map:
            for dtc_code in system_dtc_map[system]:
                # Check if DTC exists in service manual
                for category in sm_data['service_manual'].values():
                    if dtc_code in category.get('dtc_codes', {}):
                        dtc_info = category['dtc_codes'][dtc_code]
                        matching_dtcs.append({
                            'code': dtc_code,
                            'description': dtc_info.get('description', ''),
                            'system': system,
                            'severity': dtc_info.get('severity', 'medium')
                        })

    # Also check keywords for additional matches
    keyword_dtc_map = {
        'charge': ['P0A00', 'P0A01'],
        'voltage': ['P0A10', 'P0A11', 'OVER_VOLTAGE'],
        'power': ['P0B00', 'P0C00'],
        'motor': ['P0B00', 'P0B01'],
        'battery': ['P0A10', 'P0A11']
    }

    for keyword in keywords:
        if keyword in keyword_dtc_map:
            for dtc_code in keyword_dtc_map[keyword]:
                if not any(d['code'] == dtc_code for d in matching_dtcs):
                    for category in sm_data['service_manual'].values():
                        if dtc_code in category.get('dtc_codes', {}):
                            dtc_info = category['dtc_codes'][dtc_code]
                            matching_dtcs.append({
                                'code': dtc_code,
                                'description': dtc_info.get('description', ''),
                                'system': 'keyword_match',
                                'severity': dtc_info.get('severity', 'medium')
                            })

    return matching_dtcs

def get_system_procedures(suspected_systems: List[str]) -> List[Dict[str, Any]]:
    """Get general diagnostic procedures for suspected systems when no DTCs are available."""
    procedures = []

    system_procedures = {
        'charging': {
            'title': 'Charging System General Diagnostic Procedure',
            'steps': [
                'Check charging cable connection and integrity',
                'Verify charging station voltage output (220V AC)',
                'Inspect charging port for damage or debris',
                'Test onboard charger (OBC) voltage conversion',
                'Check DC-DC converter operation'
            ],
            'expected_values': {
                'charging_voltage': '350-400V DC',
                'charging_current': '0-125A',
                'charging_time': '30-60 minutes for full charge'
            }
        },
        'battery': {
            'title': 'Battery System General Diagnostic Procedure',
            'steps': [
                'Check battery management system (BMS) status',
                'Measure individual cell voltages',
                'Verify thermal management system operation',
                'Check battery cooling system',
                'Inspect battery pack connections'
            ],
            'expected_values': {
                'cell_voltage': '3.6-4.2V per cell',
                'pack_voltage': '350-400V DC',
                'temperature': '20-40°C operating range'
            }
        },
        'motor': {
            'title': 'Motor System General Diagnostic Procedure',
            'steps': [
                'Check motor controller communication',
                'Verify motor phase currents',
                'Test motor position sensors',
                'Check motor cooling system',
                'Inspect motor power connections'
            ],
            'expected_values': {
                'phase_current': '0-300A per phase',
                'motor_rpm': '0-14000 RPM',
                'controller_temp': '<80°C'
            }
        }
    }

    for system in suspected_systems:
        if system in system_procedures:
            procedures.append(system_procedures[system])

    return procedures

def get_vin_specific_data(vin: str) -> Dict[str, Any]:
    """Get VIN-specific data for personalized diagnostics."""
    kb_data = load_json_file('knowledge_base_mock.json')
    vin_data = kb_data['knowledge_base'].get('vin_specific_data', {}).get(vin, {})

    if vin_data:
        return {
            "vin": vin,
            "firmware_version": vin_data.get("firmware_version", "Unknown"),
            "recall_campaign": vin_data.get("recall_campaign", False),
            "recall_reason": vin_data.get("recall_reason", ""),
            "last_service": vin_data.get("last_service", "Unknown"),
            "known_issues": vin_data.get("known_issues", [])
        }

    return {
        "vin": vin,
        "firmware_version": "Unknown",
        "recall_campaign": False,
        "recall_reason": "",
        "last_service": "Unknown",
        "known_issues": []
    }

def verify_safety_standards() -> List[str]:
    """Return safety standards checklist."""
    return [
        "Disconnect high voltage battery before any work",
        "Wear insulated gloves and safety glasses",
        "Ensure vehicle is in park mode",
        "Use proper grounding equipment",
        "Follow lockout/tagout procedures"
    ]