"""
Dynamic Evacuation Pathfinding Engine (A* / Dijkstra).
Calculates shortest safe egress routes for ambulances, rescue convoys,
and evacuating citizens while automatically detouring around active landslide
debris flows, road fissures, and hazard buffer zones.
"""

import heapq
import math
from typing import Dict, List, Any, Optional, Tuple

from road_network import RoadNetworkGraph, RoadNode, RoadEdge

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two GPS coordinates in kilometers."""
    r = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(r * c, 3)

def point_to_segment_distance_km(p_lat: float, p_lng: float,
                                 a_lat: float, a_lng: float,
                                 b_lat: float, b_lng: float) -> float:
    """Calculates perpendicular distance from point P to line segment AB."""
    # Convert lat/lon degrees to approximate local meter projection
    mid_lat = math.radians((a_lat + b_lat) / 2)
    kx = 111.320 * math.cos(mid_lat)
    ky = 110.574

    px, py = p_lng * kx, p_lat * ky
    ax, ay = a_lng * kx, a_lat * ky
    bx, by = b_lng * kx, b_lat * ky

    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)

    # Parametric projection t of point onto line
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    proj_x = ax + t * dx
    proj_y = ay + t * dy
    return round(math.hypot(px - proj_x, py - proj_y), 3)

class EvacuationRouter:
    """Pathfinding engine executing hazard-aware routing on the 8-state road network."""

    def __init__(self, network: Optional[RoadNetworkGraph] = None):
        self.network = network or RoadNetworkGraph()

    def find_nearest_node(self, lat: float, lng: float) -> RoadNode:
        """Snaps a raw GPS point to the closest road network node."""
        closest_node = None
        min_dist = float('inf')
        for node in self.network.nodes.values():
            dist = haversine_km(lat, lng, node.lat, node.lng)
            if dist < min_dist:
                min_dist = dist
                closest_node = node
        return closest_node

    def apply_active_hazards(self, hazards: List[Dict[str, Any]]):
        """
        Dynamically closes any road segment that intersects an active landslide hazard.
        hazards format: [ {'lat': 27.305, 'lng': 88.588, 'threat_radius_km': 1.8, 'label': 'Ranipool Mudflow'} ]
        """
        # First reset all edges to OPEN
        for edge in self.network.edges.values():
            edge.status = "OPEN"
            edge.hazard_reason = None

        for h in hazards:
            h_lat = h.get('lat', h.get('latitude', 0.0))
            h_lng = h.get('lng', h.get('longitude', 0.0))
            radius = float(h.get('threat_radius_km', h.get('radius_km', 1.5)))
            label = h.get('label', h.get('station_name', 'Active Landslide Threat'))

            for edge in self.network.edges.values():
                u_node = self.network.nodes[edge.u]
                v_node = self.network.nodes[edge.v]

                dist = point_to_segment_distance_km(h_lat, h_lng,
                                                    u_node.lat, u_node.lng,
                                                    v_node.lat, v_node.lng)
                if dist <= radius:
                    edge.status = "BLOCKED_LANDSLIDE"
                    edge.hazard_reason = f"Blocked by {label} (Distance: {dist:.2f} km <= {radius:.2f} km buffer)"

    def compute_safe_route(self, start_id: str,
                           target_shelter_id: Optional[str] = None,
                           hazards: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Calculates the shortest safe evacuation route using Dijkstra algorithm.
        If hazards are provided, compromised edges are dynamically avoided.
        """
        if hazards:
            self.apply_active_hazards(hazards)

        if start_id not in self.network.nodes:
            return {'success': False, 'error': f"Start node '{start_id}' not found in road network."}

        # If no target shelter specified, identify the closest accessible shelter node
        shelter_ids = [n.node_id for n in self.network.nodes.values() if n.is_shelter]
        if target_shelter_id:
            if target_shelter_id not in self.network.nodes:
                return {'success': False, 'error': f"Target shelter '{target_shelter_id}' not found."}
            target_set = {target_shelter_id}
        else:
            target_set = set(shelter_ids)

        # Dijkstra priority queue: (cumulative_cost_minutes, current_node_id, path_nodes, path_edges)
        pq = [(0.0, 0.0, start_id, [start_id], [])]
        visited_costs = {}

        best_route = None

        while pq:
            cost_mins, cost_km, curr_id, node_path, edge_path = heapq.heappop(pq)

            if curr_id in visited_costs and visited_costs[curr_id] <= cost_mins:
                continue
            visited_costs[curr_id] = cost_mins

            # Target reached
            if curr_id in target_set:
                best_route = (cost_mins, cost_km, node_path, edge_path)
                break

            for neighbor_id, edge in self.network.get_neighbors(curr_id):
                # Skip blocked roads
                if edge.status != "OPEN":
                    continue

                t_mins = edge.traversal_time_minutes()
                new_mins = cost_mins + t_mins
                new_km = cost_km + edge.distance_km

                if neighbor_id not in visited_costs or new_mins < visited_costs[neighbor_id]:
                    heapq.heappush(pq, (new_mins, new_km, neighbor_id,
                                       node_path + [neighbor_id],
                                       edge_path + [edge]))

        if not best_route:
            # Trapped: all egress corridors blocked by landslides
            return {
                'success': False,
                'status': 'TRAPPED_ALL_ROADS_BLOCKED',
                'message': 'CRITICAL WARNING: All outward corridors from this sector are blocked by active debris flows.',
                'start_node': self.network.nodes[start_id].to_dict(),
                'recommendation': 'DO NOT DRIVE. Move on foot to highest local elevation or sturdy concrete building.'
            }

        cost_mins, cost_km, node_path, edge_path = best_route
        destination_node = self.network.nodes[node_path[-1]]

        # Generate coordinates polyline and turn-by-turn navigation instructions
        polyline = []
        instructions = []
        avoided_hazards = []

        for i, nid in enumerate(node_path):
            n = self.network.nodes[nid]
            polyline.append([n.lat, n.lng])

        for edge in edge_path:
            inst = f"Take {edge.corridor_name} ({edge.road_type.replace('_', ' ').title()}) for {edge.distance_km:.1f} km at {edge.speed_limit_kmh:.0f} km/h"
            instructions.append(inst)

        # Check which blocked corridors were successfully bypassed
        for edge in self.network.edges.values():
            if edge.status == "BLOCKED_LANDSLIDE" and edge.hazard_reason:
                if edge.hazard_reason not in avoided_hazards:
                    avoided_hazards.append(edge.hazard_reason)

        has_bypass = any(e.road_type == "RIDGE_BYPASS" for e in edge_path)

        return {
            'success': True,
            'status': 'SAFE_BYPASS_VERIFIED' if has_bypass else 'CLEAR_DIRECT_CORRIDOR',
            'start_location': self.network.nodes[start_id].to_dict(),
            'destination_shelter': destination_node.to_dict(),
            'total_distance_km': round(cost_km, 2),
            'estimated_time_minutes': round(cost_mins, 1),
            'node_count': len(node_path),
            'node_sequence': node_path,
            'polyline_coordinates': polyline,
            'turn_by_turn_instructions': instructions,
            'avoided_hazards_count': len(avoided_hazards),
            'avoided_hazard_details': avoided_hazards
        }
