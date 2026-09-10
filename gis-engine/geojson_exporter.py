"""
GeoJSON Serialization Engine for GIS Spatial Mapping.
Converts road networks, dynamic evacuation polylines, hazard buffer circles,
and designated relief shelters into standardized GeoJSON FeatureCollections.
"""

import math
from typing import Dict, List, Any
from road_network import RoadNetworkGraph

def create_circle_polygon(lat: float, lng: float, radius_km: float, num_points: int = 32) -> List[List[float]]:
    """Generates a closed polygon ring approximating a circular threat buffer."""
    points = []
    # 1 deg latitude ~ 110.574 km, longitude varies by cos(lat)
    r_lat = radius_km / 110.574
    r_lng = radius_km / (111.320 * math.cos(math.radians(lat)))

    for i in range(num_points):
        theta = (2 * math.pi * i) / num_points
        pt_lat = lat + r_lat * math.sin(theta)
        pt_lng = lng + r_lng * math.cos(theta)
        points.append([round(pt_lng, 5), round(pt_lat, 5)])

    # Close the polygon ring
    points.append(points[0])
    return points

class GeoJsonExporter:
    """Exports network state, routes, and hazards to standard GeoJSON."""

    @staticmethod
    def export_road_network(network: RoadNetworkGraph) -> Dict[str, Any]:
        features = []

        # Export Road Edges as LineStrings
        for edge_id, edge in network.edges.items():
            if edge_id.endswith('_rev'):
                continue  # Skip reverse duplicates for cleaner display

            u_node = network.nodes[edge.u]
            v_node = network.nodes[edge.v]

            color = '#ef4444' if edge.status != 'OPEN' else ('#38bdf8' if edge.road_type == 'RIDGE_BYPASS' else '#10b981')
            weight = 4 if edge.is_lifeline else 2

            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': [
                        [u_node.lng, u_node.lat],
                        [v_node.lng, v_node.lat]
                    ]
                },
                'properties': {
                    'edge_id': edge.edge_id,
                    'corridor': edge.corridor_name,
                    'status': edge.status,
                    'road_type': edge.road_type,
                    'distance_km': edge.distance_km,
                    'speed_kmh': edge.speed_limit_kmh,
                    'hazard_reason': edge.hazard_reason,
                    'stroke': color,
                    'stroke_width': weight
                }
            })

        # Export Nodes as Points
        for node in network.nodes.values():
            icon_color = '#3b82f6' if node.is_shelter else '#94a3b8'
            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [node.lng, node.lat]
                },
                'properties': {
                    'node_id': node.node_id,
                    'name': node.name,
                    'state': node.state,
                    'district': node.district,
                    'elevation_m': node.elevation_m,
                    'is_shelter': node.is_shelter,
                    'shelter_capacity': node.shelter_capacity,
                    'marker_color': icon_color
                }
            })

        return {
            'type': 'FeatureCollection',
            'features': features
        }

    @staticmethod
    def export_evacuation_route(route_res: Dict[str, Any]) -> Dict[str, Any]:
        """Converts a computed evacuation route result into a high-visibility GeoJSON route."""
        if not route_res.get('success'):
            return {'type': 'FeatureCollection', 'features': []}

        coords = [[pt[1], pt[0]] for pt in route_res['polyline_coordinates']]

        route_feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': coords
            },
            'properties': {
                'status': route_res['status'],
                'total_distance_km': route_res['total_distance_km'],
                'estimated_time_minutes': route_res['estimated_time_minutes'],
                'destination_shelter': route_res['destination_shelter']['name'],
                'stroke': '#2563eb',
                'stroke_width': 6,
                'stroke_opacity': 0.95
            }
        }

        # Start and Destination markers
        start_pt = coords[0]
        end_pt = coords[-1]

        start_feature = {
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': start_pt},
            'properties': {
                'role': 'EVACUATION_ORIGIN',
                'name': route_res['start_location']['name'],
                'marker_color': '#f59e0b'
            }
        }

        end_feature = {
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': end_pt},
            'properties': {
                'role': 'DESIGNATED_RELIEF_SHELTER',
                'name': route_res['destination_shelter']['name'],
                'capacity': route_res['destination_shelter']['shelter_capacity'],
                'marker_color': '#10b981'
            }
        }

        return {
            'type': 'FeatureCollection',
            'features': [route_feature, start_feature, end_feature]
        }

    @staticmethod
    def export_hazard_buffers(hazards: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Exports circular hazard threat buffers as GeoJSON polygon features."""
        features = []
        for h in hazards:
            lat = h.get('lat', h.get('latitude', 0.0))
            lng = h.get('lng', h.get('longitude', 0.0))
            r_km = float(h.get('threat_radius_km', h.get('radius_km', 1.5)))
            label = h.get('label', h.get('station_name', 'Landslide Threat'))

            poly = create_circle_polygon(lat, lng, r_km)
            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [poly]
                },
                'properties': {
                    'label': label,
                    'radius_km': r_km,
                    'fill': '#ef4444',
                    'fill_opacity': 0.25,
                    'stroke': '#b91c1c',
                    'stroke_width': 2
                }
            })

        return {
            'type': 'FeatureCollection',
            'features': features
        }
