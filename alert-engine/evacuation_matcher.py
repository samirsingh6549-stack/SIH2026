"""
Evacuation & Downstream Habitation Target Matcher.
Identifies threatened villages, habitations, and infrastructure assets
within the dynamic runout danger buffer of a landslide epicenter,
and routes citizens to designated disaster relief shelters.
"""

import math
from typing import Dict, List, Any

# Regional Habitation & Relief Shelter Inventory across the 8 NER States
NER_SHELTER_INVENTORY = [
    {
        'state': 'Sikkim',
        'district': 'East Sikkim',
        'corridor': 'NH-10 Ranipool - 9th Mile Corridor',
        'epicenter': {'lat': 27.3389, 'lng': 88.6065},
        'primary_shelter': {
            'name': 'Upper Martam Government Senior Secondary School',
            'type': 'Educational Institution / Cyclone & Landslide Shelter',
            'capacity': 850,
            'lat': 27.3520, 'lng': 88.6180,
            'amenities': ['Solar Power', 'Emergency Water Storage', 'SDRF Medical Camp', 'Helipad Access']
        },
        'secondary_shelter': {
            'name': 'Singtam Community Hall & Ground',
            'type': 'Civic Infrastructure',
            'capacity': 1200,
            'lat': 27.2350, 'lng': 88.4980
        },
        'safe_evacuation_route': 'NH-10 Upper Ridge Bypass towards Martam (Avoid Teesta riverbank lower road)',
        'threatened_villages': [
            {'name': 'Ranipool Bazaar', 'population': 2400, 'distance_km': 0.8},
            {'name': 'Martam Lower Ward', 'population': 1100, 'distance_km': 1.6},
            {'name': 'Namli Busty', 'population': 850, 'distance_km': 2.3}
        ]
    },
    {
        'state': 'Assam',
        'district': 'Dima Hasao',
        'corridor': 'NH-27 Dima Hasao Jatinga Section',
        'epicenter': {'lat': 25.1837, 'lng': 93.0298},
        'primary_shelter': {
            'name': 'Haflong Town Stadium Indoor Hall',
            'type': 'Sports Complex Shelter',
            'capacity': 1500,
            'lat': 25.1780, 'lng': 93.0150,
            'amenities': ['Backup Generator', 'Red Cross First Aid', 'Dry Ration Storage']
        },
        'secondary_shelter': {
            'name': 'Fiangpui Church Relief Center',
            'type': 'Community Hall',
            'capacity': 600,
            'lat': 25.1920, 'lng': 93.0380
        },
        'safe_evacuation_route': 'Haflong Hill Road towards Circuit House (Avoid Railway Cutting zone)',
        'threatened_villages': [
            {'name': 'Lower Jatinga Village', 'population': 1600, 'distance_km': 0.9},
            {'name': 'Bagetar Ward 4', 'population': 950, 'distance_km': 1.8},
            {'name': 'Mahur Gate Basti', 'population': 1300, 'distance_km': 2.5}
        ]
    },
    {
        'state': 'Meghalaya',
        'district': 'East Khasi Hills',
        'corridor': 'SH-5 Sohra Cherrapunji Escarpment',
        'epicenter': {'lat': 25.2702, 'lng': 91.7323},
        'primary_shelter': {
            'name': 'Sohra Civil Defense Community Complex',
            'type': 'Government Relief Base',
            'capacity': 700,
            'lat': 25.2850, 'lng': 91.7450,
            'amenities': ['Radio Base', 'Water Filtration', 'Ambulance Station']
        },
        'secondary_shelter': {
            'name': 'Ramakrishna Mission Higher Secondary School Hall',
            'type': 'Institutional Shelter',
            'capacity': 1100,
            'lat': 25.2920, 'lng': 91.7280
        },
        'safe_evacuation_route': 'Plateau Ridge Highway towards Mawdok Bridge (Avoid canyon gorges)',
        'threatened_villages': [
            {'name': 'Mawkdok Village', 'population': 1200, 'distance_km': 1.1},
            {'name': 'Laitryngew Ward', 'population': 800, 'distance_km': 2.0},
            {'name': 'Dympep Settlement', 'population': 650, 'distance_km': 2.7}
        ]
    },
    {
        'state': 'Manipur',
        'district': 'Noney',
        'corridor': 'NH-37 / Tupul Railway Valley Corridor',
        'epicenter': {'lat': 24.8167, 'lng': 93.6833},
        'primary_shelter': {
            'name': 'Noney District Headquarters Civil Center',
            'type': 'District Administrative Shelter',
            'capacity': 950,
            'lat': 24.8320, 'lng': 93.6990,
            'amenities': ['Satellite Comms', 'Army Medical Unit', 'Water Tankers']
        },
        'secondary_shelter': {
            'name': 'Tupul Railway High School Complex',
            'type': 'School Shelter',
            'capacity': 500,
            'lat': 24.8100, 'lng': 93.6650
        },
        'safe_evacuation_route': 'NH-37 Upper Spur towards Longmai Town (Avoid Ijei Riverbanks)',
        'threatened_villages': [
            {'name': 'Tupul Railway Colony', 'population': 850, 'distance_km': 0.7},
            {'name': 'Makhuam Village', 'population': 1400, 'distance_km': 1.4},
            {'name': 'Awangkhul Basti', 'population': 720, 'distance_km': 2.8}
        ]
    },
    {
        'state': 'Nagaland',
        'district': 'Kohima',
        'corridor': 'NH-29 Kohima South Bypass (Dzüdza Section)',
        'epicenter': {'lat': 25.6751, 'lng': 94.1086},
        'primary_shelter': {
            'name': 'Kohima South Indoor Badminton Stadium',
            'type': 'Disaster Relief Shelter',
            'capacity': 1400,
            'lat': 25.6620, 'lng': 94.1190,
            'amenities': ['Solar Inverter', 'SDRF Staging Base', 'Emergency Kitchen']
        },
        'secondary_shelter': {
            'name': 'Zubza Community Town Hall',
            'type': 'Civic Hall',
            'capacity': 650,
            'lat': 25.7100, 'lng': 94.0450
        },
        'safe_evacuation_route': 'Bypass Crest Road towards Phesama Ridge',
        'threatened_villages': [
            {'name': 'Sechu Zubza Ward', 'population': 1800, 'distance_km': 1.2},
            {'name': 'Phesama Valley Lower', 'population': 950, 'distance_km': 2.1},
            {'name': 'Mezoma Outskirts', 'population': 620, 'distance_km': 3.0}
        ]
    },
    {
        'state': 'Arunachal Pradesh',
        'district': 'West Kameng',
        'corridor': 'NH-13 Bhalukpong - Tawang Highway',
        'epicenter': {'lat': 27.5861, 'lng': 91.8653},
        'primary_shelter': {
            'name': 'Dirang Civil Defense Base Camp',
            'type': 'Paramilitary / Disaster Camp',
            'capacity': 800,
            'lat': 27.3550, 'lng': 92.2350,
            'amenities': ['Snow/Rain Cleared Helipad', 'BRO Heavy Machinery', 'Army Hospital']
        },
        'secondary_shelter': {
            'name': 'Tawang Monastery Guest Complex',
            'type': 'Community Shelter',
            'capacity': 1200,
            'lat': 27.5890, 'lng': 91.8610
        },
        'safe_evacuation_route': 'High Alpine Military Spur Route away from Sela Lake pass',
        'threatened_villages': [
            {'name': 'Sela Pass Transit Basti', 'population': 350, 'distance_km': 1.5},
            {'name': 'Jaswant Garh Post', 'population': 280, 'distance_km': 2.4},
            {'name': 'Jung Waterfall Valley', 'population': 620, 'distance_km': 3.2}
        ]
    },
    {
        'state': 'Mizoram',
        'district': 'Aizawl',
        'corridor': 'Aizawl Chite Veng & Hunthar Sinking Area',
        'epicenter': {'lat': 23.7271, 'lng': 92.7176},
        'primary_shelter': {
            'name': 'Vanapa Hall & Aizawl Indoor Stadium',
            'type': 'Civic Disaster Sanctuary',
            'capacity': 1600,
            'lat': 23.7310, 'lng': 92.7150,
            'amenities': ['Water Storage', 'Red Cross Unit', 'Telecom Mesh Base']
        },
        'secondary_shelter': {
            'name': 'Chite Veng YMA Hall',
            'type': 'Community Hall',
            'capacity': 500,
            'lat': 23.7210, 'lng': 92.7310
        },
        'safe_evacuation_route': 'Ridge Crest Road towards Durtlang Heights (Avoid eastern steep scree)',
        'threatened_villages': [
            {'name': 'Hunthar Sinking Sector', 'population': 1500, 'distance_km': 0.8},
            {'name': 'Chite River Basin', 'population': 1100, 'distance_km': 1.7},
            {'name': 'Bawngkawn Lower Ward', 'population': 1350, 'distance_km': 2.4}
        ]
    },
    {
        'state': 'Tripura',
        'district': 'North Tripura',
        'corridor': 'NH-8 Jampui Hills Vanghmun Ridge',
        'epicenter': {'lat': 23.9500, 'lng': 92.2667},
        'primary_shelter': {
            'name': 'Vanghmun YMA Community Relief Hub',
            'type': 'Community Shelter',
            'capacity': 600,
            'lat': 23.9540, 'lng': 92.2710,
            'amenities': ['First Aid Station', 'Rainwater Tank', 'Emergency Power']
        },
        'secondary_shelter': {
            'name': 'Kanchanpur Government Degree College',
            'type': 'College Campus Shelter',
            'capacity': 1000,
            'lat': 23.9800, 'lng': 92.2200
        },
        'safe_evacuation_route': 'Ridge Top Highway towards Kanchanpur Sub-Division',
        'threatened_villages': [
            {'name': 'Vanghmun Village', 'population': 850, 'distance_km': 0.6},
            {'name': 'Phuldungsei Ward', 'population': 620, 'distance_km': 1.9},
            {'name': 'Tlangsang Settlement', 'population': 450, 'distance_km': 2.6}
        ]
    }
]

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Computes great-circle distance between two GPS coordinates in kilometers."""
    r = 6371.0  # Earth's radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(r * c, 3)

def calculate_threat_radius_km(slope_deg: float, pore_pressure_kpa: float, rainfall_mm: float) -> float:
    """
    Computes dynamic debris flow / landslide runout threat radius.
    Steeper slopes, high pore pressures, and intense cloudbursts increase the runout distance.
    """
    base_radius = 1.0  # minimum 1 km buffer
    # Steeper slopes (>35 deg) extend runout speed
    slope_factor = max(0.0, (slope_deg - 25.0) / 20.0) * 0.8
    # High pore pressure indicates fluidized debris flow
    pore_factor = max(0.0, (pore_pressure_kpa - 30.0) / 30.0) * 1.0
    # Torrential rainfall increases fluid runout
    rain_factor = max(0.0, (rainfall_mm - 50.0) / 100.0) * 0.7

    threat_radius = base_radius + slope_factor + pore_factor + rain_factor
    return round(min(5.0, max(1.2, threat_radius)), 2)

def match_evacuation_targets(latitude: float, longitude: float,
                             risk_tier: str = "EVACUATION",
                             slope_deg: float = 40.0,
                             pore_pressure_kpa: float = 45.0,
                             rainfall_mm: float = 75.0) -> Dict[str, Any]:
    """
    Finds the closest hazard corridor, computes the dynamic threat buffer,
    matches endangered villages within that radius, and pairs them with safe relief shelters.
    """
    closest_corridor = None
    min_dist = float('inf')

    for corridor in NER_SHELTER_INVENTORY:
        epi = corridor['epicenter']
        dist = haversine_distance_km(latitude, longitude, epi['lat'], epi['lng'])
        if dist < min_dist:
            min_dist = dist
            closest_corridor = corridor

    # Default to first corridor if none found
    selected = closest_corridor or NER_SHELTER_INVENTORY[0]
    threat_radius = calculate_threat_radius_km(slope_deg, pore_pressure_kpa, rainfall_mm)

    # Filter villages within threat radius or pick top vulnerable
    villages = selected['threatened_villages']
    threatened = [v for v in villages if v['distance_km'] <= threat_radius]
    if not threatened:
        threatened = [villages[0]]

    total_pop_at_risk = sum(v['population'] for v in threatened)

    return {
        'matched_corridor': selected['corridor'],
        'state': selected['state'],
        'district': selected['district'],
        'threat_radius_km': threat_radius,
        'threatened_villages': [v['name'] for v in threatened],
        'total_population_at_risk': total_pop_at_risk,
        'primary_shelter': selected['primary_shelter'],
        'secondary_shelter': selected['secondary_shelter'],
        'safe_evacuation_route': selected['safe_evacuation_route'],
        'distance_to_epicenter_km': min_dist if min_dist != float('inf') else 0.0
    }
