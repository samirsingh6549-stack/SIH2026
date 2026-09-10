import math
from typing import List, Dict, Any

# Geological Survey of India (GSI) Bhukosh Historical Landslide Records for NER
GSI_HISTORICAL_INVENTORY = [
    {
        "event_id": "GSI_NER_2022_001",
        "location_name": "Tupul Railway Yard / Noney",
        "district": "Noney",
        "state": "Manipur",
        "latitude": 24.8217,
        "longitude": 93.6389,
        "date_occurred": "2022-06-30",
        "landslide_type": "Debris Flow & Translational Cut-Slope Failure",
        "trigger_mechanism": "Continuous 72h antecedent rainfall (242 mm) on unreinforced railway cut slopes",
        "lithology": "Weathered Disang Shales & Interbedded Sandstones",
        "fatalities": 58,
        "infrastructure_damage": "Complete devastation of Tupul railway station platform & Ijei river blockage",
        "gsi_bhukosh_code": "BHU-NER-MN-2022-04"
    },
    {
        "event_id": "GSI_NER_2022_002",
        "location_name": "Haflong Hill Station - New Haflong Railway",
        "district": "Dima Hasao",
        "state": "Assam",
        "latitude": 25.1833,
        "longitude": 93.0167,
        "date_occurred": "2022-05-15",
        "landslide_type": "Rotational Slump & Soil Liquefaction",
        "trigger_mechanism": "Pre-monsoon extreme cloudburst (310 mm in 48h)",
        "lithology": "Barail Group unconsolidated sandstones & plastic silts",
        "fatalities": 14,
        "infrastructure_damage": "Lumding-Badarpur railway tracks washed away; Haflong town cut off for 3 weeks",
        "gsi_bhukosh_code": "BHU-NER-AS-2022-12"
    },
    {
        "event_id": "GSI_NER_2023_003",
        "location_name": "NH-10 Teesta Valley - Dikchu Sector",
        "district": "East & North Sikkim",
        "state": "Sikkim",
        "latitude": 27.3820,
        "longitude": 88.5190,
        "date_occurred": "2023-10-04",
        "landslide_type": "Catastrophic Rock Avalanche & Toe Erosion",
        "trigger_mechanism": "South Lhonak GLOF flash flood surge combined with heavy mountain precipitation",
        "lithology": "Daling Group high-grade phyllites and fractured schists",
        "fatalities": 42,
        "infrastructure_damage": "NH-10 lifeline highway breached at 14 locations; Chungthang dam collapse",
        "gsi_bhukosh_code": "BHU-NER-SK-2023-01"
    },
    {
        "event_id": "GSI_NER_2024_004",
        "location_name": "Aizawl Hunthar & Melthum Sinking Zone",
        "district": "Aizawl",
        "state": "Mizoram",
        "latitude": 23.7307,
        "longitude": 92.7173,
        "date_occurred": "2024-05-28",
        "landslide_type": "Deep-Seated Multi-Tier Rotational Slide",
        "trigger_mechanism": "Cyclone Remal tropical downpour (190 mm in 24h)",
        "lithology": "Surma Group brittle siltstone and clayey shale",
        "fatalities": 34,
        "infrastructure_damage": "Stone quarry collapse and 150+ residential buildings displaced along NH-54",
        "gsi_bhukosh_code": "BHU-NER-MZ-2024-08"
    },
    {
        "event_id": "GSI_NER_2024_005",
        "location_name": "NH-29 Dzüdza River Sector / Kohima",
        "district": "Kohima",
        "state": "Nagaland",
        "latitude": 25.6890,
        "longitude": 94.0410,
        "date_occurred": "2024-08-19",
        "landslide_type": "Debris Avalanche & Road Subsidence",
        "trigger_mechanism": "Monsoon saturated regolith sliding into Dzüdza gorge",
        "lithology": "Disang flysch with fractured clay gouge zones",
        "fatalities": 6,
        "infrastructure_damage": "NH-29 commercial artery severed, cutting off supply lines between Dimapur and Manipur",
        "gsi_bhukosh_code": "BHU-NER-NL-2024-03"
    },
    {
        "event_id": "GSI_NER_2022_006",
        "location_name": "Sohra-Shella Escarpment",
        "district": "East Khasi Hills",
        "state": "Meghalaya",
        "latitude": 25.2702,
        "longitude": 91.7323,
        "date_occurred": "2022-06-18",
        "landslide_type": "Planar Rockfall & Cascading Mudflows",
        "trigger_mechanism": "World-record precipitation event (972 mm in 72h)",
        "lithology": "Shella Formation massive bedded limestone & sandstone cliffs",
        "fatalities": 18,
        "infrastructure_damage": "Multiple village access roads severed across Southern Khasi Hills",
        "gsi_bhukosh_code": "BHU-NER-ML-2022-19"
    },
    {
        "event_id": "GSI_NER_2023_007",
        "location_name": "Sela Tunnel Approach Road",
        "district": "West Kameng & Tawang",
        "state": "Arunachal Pradesh",
        "latitude": 27.5012,
        "longitude": 92.1034,
        "date_occurred": "2023-07-22",
        "landslide_type": "High-Altitude Glacial Moraine & Scree Slide",
        "trigger_mechanism": "Rapid snowmelt combined with cloudburst runoff",
        "lithology": "Granite gneiss and fractured quartzites",
        "fatalities": 2,
        "infrastructure_damage": "Strategic defense highway to LAC blocked for 48 hours",
        "gsi_bhukosh_code": "BHU-NER-AR-2023-05"
    },
    {
        "event_id": "GSI_NER_2023_008",
        "location_name": "Vanghmun - Jampui Ridge",
        "district": "North Tripura",
        "state": "Tripura",
        "latitude": 23.9500,
        "longitude": 92.2833,
        "date_occurred": "2023-08-11",
        "landslide_type": "Shallow Soil Slip & Orchard Slope Slump",
        "trigger_mechanism": "Sustained monsoon rains (140 mm in 24h) on cleared orange orchards",
        "lithology": "Tipam Sandstones with soft clay binding",
        "fatalities": 0,
        "infrastructure_damage": "Kanchanpur-Vanghmun road connectivity disrupted",
        "gsi_bhukosh_code": "BHU-NER-TR-2023-02"
    }
]

def get_all_historical_landslides() -> List[Dict[str, Any]]:
    return GSI_HISTORICAL_INVENTORY

def get_landslides_by_state(state: str) -> List[Dict[str, Any]]:
    s_norm = state.strip().lower()
    return [e for e in GSI_HISTORICAL_INVENTORY if e["state"].strip().lower() == s_norm]

def find_nearest_historical_landslide(lat: float, lon: float) -> Dict[str, Any]:
    """
    Computes great-circle distance (Haversine formula) to locate the closest historical landslide event.
    """
    closest = None
    min_dist_km = float('inf')

    for event in GSI_HISTORICAL_INVENTORY:
        e_lat = event['latitude']
        e_lon = event['longitude']

        # Haversine distance
        d_lat = math.radians(e_lat - lat)
        d_lon = math.radians(e_lon - lon)
        a = (math.sin(d_lat / 2) ** 2 +
             math.cos(math.radians(lat)) * math.cos(math.radians(e_lat)) * math.sin(d_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist_km = 6371.0 * c

        if dist_km < min_dist_km:
            min_dist_km = dist_km
            closest = event

    return {
        "nearest_event": closest,
        "distance_km": round(min_dist_km, 2)
    }
