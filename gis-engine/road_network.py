"""
8-State Lifeline Highway Network Graph Model.
Topological graph representation of critical mountain highway corridors,
bridges, valley cutting sections, and ridge bypass routes across North East India.
"""

import math
from typing import Dict, List, Any, Optional, Tuple

class RoadNode:
    def __init__(self, node_id: str, name: str, state: str, district: str,
                 lat: float, lng: float, elevation_m: float, is_shelter: bool = False,
                 shelter_capacity: int = 0):
        self.node_id = node_id
        self.name = name
        self.state = state
        self.district = district
        self.lat = lat
        self.lng = lng
        self.elevation_m = elevation_m
        self.is_shelter = is_shelter
        self.shelter_capacity = shelter_capacity

    def to_dict(self) -> Dict[str, Any]:
        return {
            'node_id': self.node_id,
            'name': self.name,
            'state': self.state,
            'district': self.district,
            'coordinates': [self.lat, self.lng],
            'elevation_m': self.elevation_m,
            'is_shelter': self.is_shelter,
            'shelter_capacity': self.shelter_capacity
        }

class RoadEdge:
    def __init__(self, edge_id: str, u: str, v: str, corridor_name: str,
                 distance_km: float, speed_limit_kmh: float = 35.0,
                 is_lifeline: bool = True, road_type: str = "NATIONAL_HIGHWAY"):
        self.edge_id = edge_id
        self.u = u  # Start node ID
        self.v = v  # End node ID
        self.corridor_name = corridor_name
        self.distance_km = distance_km
        self.speed_limit_kmh = speed_limit_kmh
        self.is_lifeline = is_lifeline
        self.road_type = road_type  # NATIONAL_HIGHWAY, STATE_HIGHWAY, RIDGE_BYPASS
        self.status = "OPEN"  # OPEN, BLOCKED_LANDSLIDE, RESTRICTED_CONVOY
        self.hazard_reason: Optional[str] = None

    def traversal_time_minutes(self) -> float:
        """Returns standard traversal time in minutes."""
        if self.status != "OPEN":
            return float('inf')
        return round((self.distance_km / self.speed_limit_kmh) * 60.0, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'edge_id': self.edge_id,
            'from': self.u,
            'to': self.v,
            'corridor': self.corridor_name,
            'distance_km': self.distance_km,
            'speed_kmh': self.speed_limit_kmh,
            'status': self.status,
            'hazard_reason': self.hazard_reason,
            'road_type': self.road_type
        }

class RoadNetworkGraph:
    """Graph structure managing road topology, edge interdiction, and adjacency lists."""

    def __init__(self):
        self.nodes: Dict[str, RoadNode] = {}
        self.edges: Dict[str, RoadEdge] = {}
        self.adjacency: Dict[str, List[Tuple[str, str]]] = {}  # node_id -> [(neighbor_id, edge_id)]
        self._build_ner_lifeline_network()

    def add_node(self, node: RoadNode):
        self.nodes[node.node_id] = node
        if node.node_id not in self.adjacency:
            self.adjacency[node.node_id] = []

    def add_edge(self, edge: RoadEdge, bidirectional: bool = True):
        self.edges[edge.edge_id] = edge
        self.adjacency[edge.u].append((edge.v, edge.edge_id))
        if bidirectional:
            rev_id = f"{edge.edge_id}_rev"
            rev_edge = RoadEdge(rev_id, edge.v, edge.u, edge.corridor_name,
                                edge.distance_km, edge.speed_limit_kmh,
                                edge.is_lifeline, edge.road_type)
            self.edges[rev_id] = rev_edge
            self.adjacency[edge.v].append((edge.u, rev_id))

    def set_edge_status(self, edge_id: str, status: str, reason: Optional[str] = None):
        """Sets status (OPEN or BLOCKED_LANDSLIDE) and synchronizes reverse edge."""
        if edge_id in self.edges:
            self.edges[edge_id].status = status
            self.edges[edge_id].hazard_reason = reason
        rev_id = f"{edge_id}_rev" if not edge_id.endswith('_rev') else edge_id[:-4]
        if rev_id in self.edges:
            self.edges[rev_id].status = status
            self.edges[rev_id].hazard_reason = reason

    def get_neighbors(self, node_id: str) -> List[Tuple[str, RoadEdge]]:
        result = []
        for neighbor_id, edge_id in self.adjacency.get(node_id, []):
            result.append((neighbor_id, self.edges[edge_id]))
        return result

    def _build_ner_lifeline_network(self):
        """Initializes strategic road corridors across all 8 North Eastern states."""
        
        # --- 1. SIKKIM (NH-10 & Upper Martam Bypass) ---
        self.add_node(RoadNode("SKM_SINGTAM", "Singtam Junction", "Sikkim", "East Sikkim", 27.2350, 88.4980, 350.0))
        self.add_node(RoadNode("SKM_32MILE", "32nd Mile Checkpost", "Sikkim", "East Sikkim", 27.2850, 88.5520, 580.0))
        self.add_node(RoadNode("SKM_MARTAM_JUNCT", "Martam Bypass Junction", "Sikkim", "East Sikkim", 27.2920, 88.5620, 680.0))
        self.add_node(RoadNode("SKM_RANIPOOL", "Ranipool Bridge (NH-10)", "Sikkim", "East Sikkim", 27.3050, 88.5880, 860.0))
        self.add_node(RoadNode("SKM_9TH_MILE", "9th Mile Debris Zone", "Sikkim", "East Sikkim", 27.3250, 88.6010, 1100.0))
        self.add_node(RoadNode("SKM_GANGTOK", "Gangtok Capital Hub", "Sikkim", "East Sikkim", 27.3389, 88.6065, 1650.0))
        self.add_node(RoadNode("SKM_MARTAM_CREST", "Upper Martam Western Ridge Crest", "Sikkim", "East Sikkim", 27.3250, 88.5450, 1250.0))
        self.add_node(RoadNode("SKM_UPPER_MARTAM_SHELTER", "Upper Martam Relief Shelter", "Sikkim", "East Sikkim", 27.3520, 88.6180, 1420.0, is_shelter=True, shelter_capacity=850))

        # Direct valley road (NH-10, prone to debris flow)
        self.add_edge(RoadEdge("E_SKM_01", "SKM_SINGTAM", "SKM_32MILE", "NH-10", 6.2, 40.0))
        self.add_edge(RoadEdge("E_SKM_02", "SKM_32MILE", "SKM_MARTAM_JUNCT", "NH-10", 2.1, 35.0))
        self.add_edge(RoadEdge("E_SKM_03", "SKM_MARTAM_JUNCT", "SKM_RANIPOOL", "NH-10 Ranipool Sector", 3.4, 30.0))
        self.add_edge(RoadEdge("E_SKM_04", "SKM_RANIPOOL", "SKM_9TH_MILE", "NH-10 9th Mile", 2.8, 25.0))
        self.add_edge(RoadEdge("E_SKM_05", "SKM_9TH_MILE", "SKM_GANGTOK", "NH-10 Gangtok Approach", 3.1, 30.0))
        # Upper Ridge Bypass Route (Safe alternative avoiding Ranipool riverbed mudflow via Western Crest)
        self.add_edge(RoadEdge("E_SKM_BYPASS_01", "SKM_MARTAM_JUNCT", "SKM_MARTAM_CREST", "Upper Martam Ridge Ascent", 4.2, 28.0, road_type="RIDGE_BYPASS"))
        self.add_edge(RoadEdge("E_SKM_BYPASS_02", "SKM_MARTAM_CREST", "SKM_UPPER_MARTAM_SHELTER", "Martam Ridge Link", 4.8, 26.0, road_type="RIDGE_BYPASS"))
        self.add_edge(RoadEdge("E_SKM_BYPASS_03", "SKM_UPPER_MARTAM_SHELTER", "SKM_GANGTOK", "Tathangchen Crest Link", 4.2, 25.0, road_type="RIDGE_BYPASS"))


        # --- 2. ASSAM (NH-27 Dima Hasao Jatinga & Haflong Bypass) ---
        self.add_node(RoadNode("ASM_MAHUR", "Mahur Junction", "Assam", "Dima Hasao", 25.1200, 93.1100, 420.0))
        self.add_node(RoadNode("ASM_JATINGA_CHOK", "Jatinga Valley Cutting", "Assam", "Dima Hasao", 25.1837, 93.0298, 620.0))
        self.add_node(RoadNode("ASM_HAFLONG_SHELTER", "Haflong Town Stadium Shelter", "Assam", "Dima Hasao", 25.1780, 93.0150, 780.0, is_shelter=True, shelter_capacity=1500))
        self.add_node(RoadNode("ASM_CIRCUIT_RIDGE", "Circuit House Upper Ridge", "Assam", "Dima Hasao", 25.1890, 93.0220, 840.0))

        self.add_edge(RoadEdge("E_ASM_01", "ASM_MAHUR", "ASM_JATINGA_CHOK", "NH-27 Jatinga Section", 8.4, 35.0))
        self.add_edge(RoadEdge("E_ASM_02", "ASM_JATINGA_CHOK", "ASM_HAFLONG_SHELTER", "NH-27 Haflong Gate", 3.2, 30.0))
        # High bypass avoiding valley cutting
        self.add_edge(RoadEdge("E_ASM_BYPASS", "ASM_MAHUR", "ASM_CIRCUIT_RIDGE", "Mahur-Circuit Crest Bypass", 9.1, 28.0, road_type="RIDGE_BYPASS"))
        self.add_edge(RoadEdge("E_ASM_BYPASS_2", "ASM_CIRCUIT_RIDGE", "ASM_HAFLONG_SHELTER", "Circuit House Descent", 2.0, 30.0, road_type="RIDGE_BYPASS"))

        # --- 3. MANIPUR (NH-37 Tupul Railway Corridor) ---
        self.add_node(RoadNode("MAN_JIRIBAM_SPUR", "Jiribam Foothills", "Manipur", "Noney", 24.8000, 93.1200, 210.0))
        self.add_node(RoadNode("MAN_TUPUL_VALLEY", "Tupul River Bed Yard", "Manipur", "Noney", 24.8167, 93.6833, 490.0))
        self.add_node(RoadNode("MAN_NONEY_SHELTER", "Noney District Civil Shelter", "Manipur", "Noney", 24.8320, 93.6990, 620.0, is_shelter=True, shelter_capacity=950))
        self.add_node(RoadNode("MAN_LONGMAI_RIDGE", "Longmai Mountain Spur", "Manipur", "Noney", 24.8450, 93.7100, 810.0))

        self.add_edge(RoadEdge("E_MAN_01", "MAN_JIRIBAM_SPUR", "MAN_TUPUL_VALLEY", "NH-37 Tupul Approach", 14.5, 30.0))
        self.add_edge(RoadEdge("E_MAN_02", "MAN_TUPUL_VALLEY", "MAN_NONEY_SHELTER", "NH-37 Tupul-Noney", 4.1, 25.0))
        self.add_edge(RoadEdge("E_MAN_BYPASS", "MAN_JIRIBAM_SPUR", "MAN_LONGMAI_RIDGE", "Longmai Ridge Trail", 16.2, 22.0, road_type="RIDGE_BYPASS"))
        self.add_edge(RoadEdge("E_MAN_BYPASS_2", "MAN_LONGMAI_RIDGE", "MAN_NONEY_SHELTER", "Longmai-Noney Descent", 3.0, 25.0, road_type="RIDGE_BYPASS"))

        # --- 4. MEGHALAYA (SH-5 Sohra Cherrapunji) ---
        self.add_node(RoadNode("MEG_SHILLONG", "Shillong Civil Hub", "Meghalaya", "East Khasi Hills", 25.5788, 91.8933, 1520.0))
        self.add_node(RoadNode("MEG_MAWKDOK", "Mawkdok Dympep Bridge", "Meghalaya", "East Khasi Hills", 25.4200, 91.8100, 1410.0))
        self.add_node(RoadNode("MEG_DYMPEP_GORGE", "Dympep Canyon Edge", "Meghalaya", "East Khasi Hills", 25.3500, 91.7800, 1380.0))
        self.add_node(RoadNode("MEG_SOHRA_SHELTER", "Sohra Civil Defense Shelter", "Meghalaya", "East Khasi Hills", 25.2850, 91.7450, 1430.0, is_shelter=True, shelter_capacity=700))

        self.add_edge(RoadEdge("E_MEG_01", "MEG_SHILLONG", "MEG_MAWKDOK", "SH-5 Shillong-Mawkdok", 18.0, 45.0))
        self.add_edge(RoadEdge("E_MEG_02", "MEG_MAWKDOK", "MEG_DYMPEP_GORGE", "SH-5 Canyon Section", 8.5, 35.0))
        self.add_edge(RoadEdge("E_MEG_03", "MEG_DYMPEP_GORGE", "MEG_SOHRA_SHELTER", "SH-5 Sohra Road", 9.2, 35.0))
        # Upper Plateau Bypass
        self.add_edge(RoadEdge("E_MEG_BYPASS", "MEG_MAWKDOK", "MEG_SOHRA_SHELTER", "Laitryngew Plateau Bypass", 16.0, 32.0, road_type="RIDGE_BYPASS"))

        # --- 5. NAGALAND (NH-29 Kohima Dzüdza Section) ---
        self.add_node(RoadNode("NAG_ZUBZA", "Sechu Zubza Valley", "Nagaland", "Kohima", 25.7100, 94.0450, 890.0))
        self.add_node(RoadNode("NAG_DZUDZA_BRIDGE", "Dzüdza River Crossing", "Nagaland", "Kohima", 25.6751, 94.1086, 1120.0))
        self.add_node(RoadNode("NAG_KOHIMA_SHELTER", "Kohima South Indoor Stadium", "Nagaland", "Kohima", 25.6620, 94.1190, 1440.0, is_shelter=True, shelter_capacity=1400))
        self.add_node(RoadNode("NAG_KHONOMA_RIDGE", "Khonoma Mountain Crest", "Nagaland", "Kohima", 25.6500, 94.0200, 1510.0))

        self.add_edge(RoadEdge("E_NAG_01", "NAG_ZUBZA", "NAG_DZUDZA_BRIDGE", "NH-29 Dzüdza River Section", 7.8, 30.0))
        self.add_edge(RoadEdge("E_NAG_02", "NAG_DZUDZA_BRIDGE", "NAG_KOHIMA_SHELTER", "NH-29 Kohima Bypass", 4.2, 28.0))
        self.add_edge(RoadEdge("E_NAG_BYPASS", "NAG_ZUBZA", "NAG_KHONOMA_RIDGE", "Khonoma Heritage Bypass", 8.9, 25.0, road_type="RIDGE_BYPASS"))
        self.add_edge(RoadEdge("E_NAG_BYPASS_2", "NAG_KHONOMA_RIDGE", "NAG_KOHIMA_SHELTER", "Phesama Crest Link", 5.1, 25.0, road_type="RIDGE_BYPASS"))

        # --- 6. ARUNACHAL PRADESH (NH-13 Tawang Sela Alpine Pass) ---
        self.add_node(RoadNode("ARN_DIRANG_BASE", "Dirang Civil Defense Base", "Arunachal Pradesh", "West Kameng", 27.3550, 92.2350, 1560.0, is_shelter=True, shelter_capacity=800))
        self.add_node(RoadNode("ARN_SELA_LOWER", "Sela Base Camp (NH-13)", "Arunachal Pradesh", "West Kameng", 27.4800, 92.1200, 2800.0))
        self.add_node(RoadNode("ARN_SELA_PASS", "Sela Alpine Pass (Hazard Zone)", "Arunachal Pradesh", "West Kameng", 27.5000, 92.1000, 4170.0))
        self.add_node(RoadNode("ARN_TAWANG_SHELTER", "Tawang Monastery Shelter", "Arunachal Pradesh", "West Kameng", 27.5861, 91.8653, 3048.0, is_shelter=True, shelter_capacity=1200))

        self.add_edge(RoadEdge("E_ARN_01", "ARN_DIRANG_BASE", "ARN_SELA_LOWER", "NH-13 Dirang-Sela", 18.2, 28.0))
        self.add_edge(RoadEdge("E_ARN_02", "ARN_SELA_LOWER", "ARN_SELA_PASS", "NH-13 Sela Ascent", 6.5, 20.0))
        self.add_edge(RoadEdge("E_ARN_03", "ARN_SELA_PASS", "ARN_TAWANG_SHELTER", "NH-13 Sela-Tawang", 14.8, 25.0))

        # --- 7. MIZORAM (Aizawl Spine & Hunthar Sinking Area) ---
        self.add_node(RoadNode("MIZ_HUNTHAR_SINK", "Hunthar Sinking Zone", "Mizoram", "Aizawl", 23.7271, 92.7176, 880.0))
        self.add_node(RoadNode("MIZ_VANAPA_SHELTER", "Vanapa Hall Disaster Sanctuary", "Mizoram", "Aizawl", 23.7310, 92.7150, 1020.0, is_shelter=True, shelter_capacity=1600))
        self.add_node(RoadNode("MIZ_CHITE_VALLEY", "Chite Veng Lower Bridge", "Mizoram", "Aizawl", 23.7210, 92.7310, 710.0))
        self.add_node(RoadNode("MIZ_DURTLANG_RIDGE", "Durtlang North Ridge", "Mizoram", "Aizawl", 23.7800, 92.7300, 1180.0))

        self.add_edge(RoadEdge("E_MIZ_01", "MIZ_CHITE_VALLEY", "MIZ_HUNTHAR_SINK", "Hunthar Spine Road", 3.2, 22.0))
        self.add_edge(RoadEdge("E_MIZ_02", "MIZ_HUNTHAR_SINK", "MIZ_VANAPA_SHELTER", "Vanapa Access Ramp", 1.4, 20.0))
        self.add_edge(RoadEdge("E_MIZ_BYPASS", "MIZ_CHITE_VALLEY", "MIZ_DURTLANG_RIDGE", "Durtlang Eastern Bypass", 6.4, 25.0, road_type="RIDGE_BYPASS"))
        self.add_edge(RoadEdge("E_MIZ_BYPASS_2", "MIZ_DURTLANG_RIDGE", "MIZ_VANAPA_SHELTER", "Durtlang South Descent", 4.1, 22.0, road_type="RIDGE_BYPASS"))

        # --- 8. TRIPURA (NH-8 Jampui Hills) ---
        self.add_node(RoadNode("TRP_KANCHANPUR_SHELTER", "Kanchanpur College Shelter", "Tripura", "North Tripura", 23.9800, 92.2200, 120.0, is_shelter=True, shelter_capacity=1000))
        self.add_node(RoadNode("TRP_VANGHMUN_RIDGE", "Vanghmun YMA Relief Hub", "Tripura", "North Tripura", 23.9540, 92.2710, 650.0, is_shelter=True, shelter_capacity=600))
        self.add_node(RoadNode("TRP_JAMPUI_CUT", "Jampui Valley Road", "Tripura", "North Tripura", 23.9500, 92.2667, 480.0))

        self.add_edge(RoadEdge("E_TRP_01", "TRP_KANCHANPUR_SHELTER", "TRP_JAMPUI_CUT", "Kanchanpur-Jampui Road", 7.8, 30.0))
        self.add_edge(RoadEdge("E_TRP_02", "TRP_JAMPUI_CUT", "TRP_VANGHMUN_RIDGE", "Vanghmun Ridge Ascent", 3.5, 25.0))
        self.add_edge(RoadEdge("E_TRP_BYPASS", "TRP_KANCHANPUR_SHELTER", "TRP_VANGHMUN_RIDGE", "Phuldungsei Crest Trail", 9.2, 24.0, road_type="RIDGE_BYPASS"))
