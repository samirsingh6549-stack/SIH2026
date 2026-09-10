"""
Geographical & Geotechnical Metadata for Landslide Monitoring Stations
Covering all 8 North Eastern Region (NER) States.
"""

NER_STATIONS = [
    {
        "station_id": "SKM_GNT_01",
        "station_name": "Gangtok - 9th Mile (NH-10)",
        "district": "East Sikkim",
        "state": "Sikkim",
        "latitude": 27.3314,
        "longitude": 88.6138,
        "elevation_m": 1650.0,
        "slope_angle_degrees": 41.5,
        "soil_type": "clay",
        "soil_texture": "fine",
        "lithology": "metamorphic",  # Daling Group phyllites & schists
        "vegetation_density_ndvi": 0.32,
        "lifeline_corridor": "NH-10 (Siliguri - Gangtok Lifeline)",
        "sensor_installed": True
    },
    {
        "station_id": "SKM_MNG_02",
        "station_name": "Mangan - Dikchu Sector",
        "district": "North Sikkim",
        "state": "Sikkim",
        "latitude": 27.5082,
        "longitude": 88.5327,
        "elevation_m": 1280.0,
        "slope_angle_degrees": 44.0,
        "soil_type": "clay",
        "soil_texture": "fine",
        "lithology": "metamorphic",
        "vegetation_density_ndvi": 0.28,
        "lifeline_corridor": "North Sikkim Highway",
        "sensor_installed": True
    },
    {
        "station_id": "ASM_HFL_01",
        "station_name": "Haflong - Jatinga Valley",
        "district": "Dima Hasao",
        "state": "Assam",
        "latitude": 25.1833,
        "longitude": 93.0167,
        "elevation_m": 680.0,
        "slope_angle_degrees": 34.0,
        "soil_type": "loam",
        "soil_texture": "medium",
        "lithology": "sedimentary",  # Disang shales & Barail sandstones
        "vegetation_density_ndvi": 0.45,
        "lifeline_corridor": "NH-27 / Lumding-Badarpur Railway",
        "sensor_installed": True
    },
    {
        "station_id": "ASM_GHY_02",
        "station_name": "Guwahati - Khanapara Slopes",
        "district": "Kamrup Metropolitan",
        "state": "Assam",
        "latitude": 26.1158,
        "longitude": 91.8150,
        "elevation_m": 180.0,
        "slope_angle_degrees": 26.5,
        "soil_type": "loam",
        "soil_texture": "medium",
        "lithology": "igneous",  # Granite gneiss hills
        "vegetation_density_ndvi": 0.55,
        "lifeline_corridor": "Guwahati Bypass (GS Road)",
        "sensor_installed": False
    },
    {
        "station_id": "MEG_SHR_01",
        "station_name": "Cherrapunji - Sohra Escarpment",
        "district": "East Khasi Hills",
        "state": "Meghalaya",
        "latitude": 25.2702,
        "longitude": 91.7323,
        "elevation_m": 1430.0,
        "slope_angle_degrees": 43.5,
        "soil_type": "silt",
        "soil_texture": "fine",
        "lithology": "sedimentary",  # Limestone & sandstone cliff bands
        "vegetation_density_ndvi": 0.38,
        "lifeline_corridor": "SH-5 (Sohra-Shella Corridor)",
        "sensor_installed": True
    },
    {
        "station_id": "MEG_SHL_02",
        "station_name": "Shillong - Umiam Bypass",
        "district": "Ri-Bhoi",
        "state": "Meghalaya",
        "latitude": 25.6580,
        "longitude": 91.9050,
        "elevation_m": 1020.0,
        "slope_angle_degrees": 31.0,
        "soil_type": "clay",
        "soil_texture": "medium",
        "lithology": "metamorphic",
        "vegetation_density_ndvi": 0.62,
        "lifeline_corridor": "NH-6 (Guwahati - Shillong - Silchar)",
        "sensor_installed": True
    },
    {
        "station_id": "ARN_TWG_01",
        "station_name": "Tawang - Sela Pass Passway",
        "district": "Tawang",
        "state": "Arunachal Pradesh",
        "latitude": 27.5861,
        "longitude": 91.8653,
        "elevation_m": 2980.0,
        "slope_angle_degrees": 45.0,
        "soil_type": "gravel",
        "soil_texture": "coarse",
        "lithology": "igneous",  # High-grade crystalline complex
        "vegetation_density_ndvi": 0.22,
        "lifeline_corridor": "NH-13 (Trans-Arunachal Highway)",
        "sensor_installed": True
    },
    {
        "station_id": "ARN_ITN_02",
        "station_name": "Itanagar - Banderdewa Pass",
        "district": "Papum Pare",
        "state": "Arunachal Pradesh",
        "latitude": 27.0844,
        "longitude": 93.6053,
        "elevation_m": 530.0,
        "slope_angle_degrees": 33.5,
        "soil_type": "sand",
        "soil_texture": "coarse",
        "lithology": "sedimentary",  # Siwalik sandstone & gravel
        "vegetation_density_ndvi": 0.48,
        "lifeline_corridor": "NH-415 (Capital Complex Corridor)",
        "sensor_installed": False
    },
    {
        "station_id": "NAG_KHM_01",
        "station_name": "Kohima - Dzüdza River Sector",
        "district": "Kohima",
        "state": "Nagaland",
        "latitude": 25.6751,
        "longitude": 94.1086,
        "elevation_m": 1440.0,
        "slope_angle_degrees": 39.0,
        "soil_type": "clay",
        "soil_texture": "fine",
        "lithology": "sedimentary",  # Highly weathered Disang Flysch
        "vegetation_density_ndvi": 0.35,
        "lifeline_corridor": "NH-29 (Dimapur - Kohima - Imphal)",
        "sensor_installed": True
    },
    {
        "station_id": "MAN_TPL_01",
        "station_name": "Noney - Tupul Railway Yard",
        "district": "Noney",
        "state": "Manipur",
        "latitude": 24.8217,
        "longitude": 93.6389,
        "elevation_m": 720.0,
        "slope_angle_degrees": 42.0,
        "soil_type": "clay",
        "soil_texture": "fine",
        "lithology": "sedimentary",  # Weathered shale cut-slopes
        "vegetation_density_ndvi": 0.26,
        "lifeline_corridor": "NH-37 (Jiribam - Imphal Highway)",
        "sensor_installed": True
    },
    {
        "station_id": "MIZ_AZL_01",
        "station_name": "Aizawl - Hunthar Sinking Zone",
        "district": "Aizawl",
        "state": "Mizoram",
        "latitude": 23.7307,
        "longitude": 92.7173,
        "elevation_m": 1130.0,
        "slope_angle_degrees": 38.5,
        "soil_type": "silt",
        "soil_texture": "fine",
        "lithology": "sedimentary",  # Tertiary Surma Group sandstones
        "vegetation_density_ndvi": 0.40,
        "lifeline_corridor": "NH-54 (Silchar - Aizawl Arterial Road)",
        "sensor_installed": True
    },
    {
        "station_id": "TRP_JMP_01",
        "station_name": "Jampui Hills - Vanghmun",
        "district": "North Tripura",
        "state": "Tripura",
        "latitude": 23.9500,
        "longitude": 92.2833,
        "elevation_m": 880.0,
        "slope_angle_degrees": 29.5,
        "soil_type": "loam",
        "soil_texture": "medium",
        "lithology": "sedimentary",
        "vegetation_density_ndvi": 0.58,
        "lifeline_corridor": "Dharmanagar - Kanchanpur Road",
        "sensor_installed": False
    }
]

def get_station_by_id(station_id: str):
    for s in NER_STATIONS:
        if s["station_id"] == station_id:
            return s
    return None

def get_stations_by_state(state_name: str):
    state_lower = state_name.strip().lower()
    return [s for s in NER_STATIONS if s["state"].strip().lower() == state_lower]
