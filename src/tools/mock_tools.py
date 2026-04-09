import json
import os
from typing import List, Dict, Any

# Load mock data into memory once to reduce disk I/O.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_DATA_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'mock_data')
_DATA_CACHE: Dict[str, Any] = {}
_SM_DTC_INDEX: Dict[str, Dict[str, Any]] = {}

_SYSTEM_DTC_MAP = {
    'charging': ['P0A00', 'P0A01', 'P0A02', 'P0A03'],
    'battery': ['P0A10', 'P0A11', 'P0A12', 'P0A13'],
    'motor': ['P0B00', 'P0B01', 'P0B02', 'P0B03'],
    'inverter': ['P0C00', 'P0C01', 'P0C02'],
    'software': ['OVER_VOLTAGE', 'UNDER_VOLTAGE']
}

_KEYWORD_DTC_MAP = {
    'charge': ['P0A00', 'P0A01', 'P0A02'],
    'voltage': ['P0A10', 'P0A11', 'OVER_VOLTAGE'],
    'power': ['P0B00', 'P0C00'],
    'motor': ['P0B00', 'P0B01'],
    'battery': ['P0A10', 'P0A11']
}


def _load_json_file(filename: str) -> Dict[str, Any]:
    if filename in _DATA_CACHE:
        return _DATA_CACHE[filename]

    filepath = os.path.join(MOCK_DATA_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    _DATA_CACHE[filename] = data
    return data


def _get_service_manual() -> Dict[str, Any]:
    service_manual_data = _load_json_file('service_manual_mock.json')
    return service_manual_data.get('service_manual', {})


def _get_knowledge_base() -> Dict[str, Any]:
    kb_data = _load_json_file('knowledge_base_mock.json')
    return kb_data.get('knowledge_base', {})


def _build_sm_dtc_index() -> None:
    global _SM_DTC_INDEX
    if _SM_DTC_INDEX:
        return

    service_manual = _get_service_manual()
    for category in service_manual.values():
        for code, info in category.get('dtc_codes', {}).items():
            _SM_DTC_INDEX[code] = info


def _find_dtc_info(dtc_code: str) -> Dict[str, Any]:
    _build_sm_dtc_index()
    return _SM_DTC_INDEX.get(dtc_code, {})

def get_sm_details(dtc_code: str) -> Dict[str, Any]:
    """Get service manual details for a DTC code."""
    return _find_dtc_info(dtc_code)


def get_kb_insights(symptom: str) -> List[Dict[str, Any]]:
    """Get knowledge base insights for a symptom."""
    kb_data = _get_knowledge_base()
    insights: List[Dict[str, Any]] = []
    symptom_lower = symptom.lower()

    for tsb in kb_data.get('tsb', []):
        if any(s.lower() in symptom_lower for s in tsb.get('symptoms', [])):
            insights.append(tsb)

    for repair in kb_data.get('repair_history', []):
        if repair.get('symptom') and repair['symptom'].lower() in symptom_lower:
            insights.append(repair)

    return insights


def search_dtc_by_symptom(suspected_systems: List[str], keywords: List[str]) -> List[Dict[str, Any]]:
    """Search for DTC codes based on suspected systems and keywords."""
    _build_sm_dtc_index()
    matching_dtcs: List[Dict[str, Any]] = []
    seen_codes = set()

    for system in suspected_systems:
        for dtc_code in _SYSTEM_DTC_MAP.get(system, []):
            dtc_info = _find_dtc_info(dtc_code)
            if dtc_info and dtc_code not in seen_codes:
                matching_dtcs.append({
                    'code': dtc_code,
                    'description': dtc_info.get('description', ''),
                    'system': system,
                    'severity': dtc_info.get('severity', 'medium')
                })
                seen_codes.add(dtc_code)

    symptom_keywords = {keyword.lower() for keyword in keywords}

    for keyword in symptom_keywords:
        for dtc_code in _KEYWORD_DTC_MAP.get(keyword, []):
            if dtc_code not in seen_codes:
                dtc_info = _find_dtc_info(dtc_code)
                if dtc_info:
                    matching_dtcs.append({
                        'code': dtc_code,
                        'description': dtc_info.get('description', ''),
                        'system': 'keyword_match',
                        'severity': dtc_info.get('severity', 'medium')
                    })
                    seen_codes.add(dtc_code)

    if symptom_keywords:
        for code, dtc_info in _SM_DTC_INDEX.items():
            description = dtc_info.get('description', '').lower()
            if any(keyword in description for keyword in symptom_keywords) and code not in seen_codes:
                matching_dtcs.append({
                    'code': code,
                    'description': dtc_info.get('description', ''),
                    'system': 'description_match',
                    'severity': dtc_info.get('severity', 'medium')
                })
                seen_codes.add(code)

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
    kb_data = _get_knowledge_base()
    vin_data = kb_data.get('vin_specific_data', {}).get(vin, {})

    if vin_data:
        return {
            'vin': vin,
            'firmware_version': vin_data.get('firmware_version', 'Unknown'),
            'recall_campaign': vin_data.get('recall_campaign', False),
            'recall_reason': vin_data.get('recall_reason', ''),
            'last_service': vin_data.get('last_service', 'Unknown'),
            'known_issues': vin_data.get('known_issues', [])
        }

    return {
        'vin': vin,
        'firmware_version': 'Unknown',
        'recall_campaign': False,
        'recall_reason': '',
        'last_service': 'Unknown',
        'known_issues': []
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