"""
Administrative Disaster Situation Report (SITREP) Generator.
Produces standardized operational briefings for District Magistrates,
State Disaster Management Authorities (SDMA), and NDRF Battalion Commanders.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
from road_network import RoadNetworkGraph

class SitrepGenerator:
    """Compiles multi-module telemetry and road statuses into formal SITREP documents."""

    @staticmethod
    def generate_sitrep(
        network: RoadNetworkGraph,
        active_hazards: Optional[List[Dict[str, Any]]] = None,
        operational_phase: str = "PHASE_3_ACTIVE_DISASTER_RESPONSE"
    ) -> Dict[str, Any]:
        ist = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist)

        hazards = active_hazards or []
        report_id = f"SITREP-NER-{now_ist.strftime('%Y%m%d-%H%M')}"

        # 1. Analyze Road Network Blockages
        blocked_edges = [e for e in network.edges.values() if e.status != 'OPEN' and not e.edge_id.endswith('_rev')]
        open_edges = [e for e in network.edges.values() if e.status == 'OPEN' and not e.edge_id.endswith('_rev')]
        total_blocked_km = round(sum(e.distance_km for e in blocked_edges), 2)
        total_lifeline_km = round(sum(e.distance_km for e in network.edges.values() if not e.edge_id.endswith('_rev')), 2)

        # 2. Analyze Relief Shelters Status
        shelters = [n for n in network.nodes.values() if n.is_shelter]
        total_shelter_capacity = sum(s.shelter_capacity for s in shelters)

        # 3. Compile Blocked Corridors Details
        interdicted_corridors = []
        for e in blocked_edges:
            interdicted_corridors.append({
                'corridor_name': e.corridor_name,
                'edge_id': e.edge_id,
                'blocked_length_km': e.distance_km,
                'cause': e.hazard_reason or 'Slope failure / Debris flow',
                'clearing_agency': 'Border Roads Organisation (BRO) / NHIDCL',
                'heavy_equipment_required': 'Excavator (20T) + Wheel Loader + Bulldozer'
            })

        # 4. Regional State Breakdown
        state_summary = {}
        for n in network.nodes.values():
            if n.state not in state_summary:
                state_summary[n.state] = {'shelters': 0, 'capacity': 0, 'active_alerts': 0}
            if n.is_shelter:
                state_summary[n.state]['shelters'] += 1
                state_summary[n.state]['capacity'] += n.shelter_capacity

        for h in hazards:
            st = h.get('state', 'Sikkim')
            if st in state_summary:
                state_summary[st]['active_alerts'] += 1

        sitrep_doc = {
            'metadata': {
                'report_id': report_id,
                'issued_by': 'NER-LEWS Central Command Centre (Ministry of Earth Sciences / NDMA)',
                'timestamp_ist': now_ist.strftime('%d-%b-%Y %H:%M:%S IST'),
                'operational_phase': operational_phase,
                'classification': 'OFFICIAL DISASTER BRIEFING - RESTRICTED'
            },
            'executive_summary': {
                'threat_level': 'CRITICAL / CODE_RED' if blocked_edges else 'MONITORING / CODE_GREEN',
                'active_landslide_hotspots': len(hazards),
                'closed_highway_sections': len(blocked_edges),
                'total_interdicted_road_km': total_blocked_km,
                'total_monitored_lifeline_km': total_lifeline_km,
                'operational_relief_shelters': len(shelters),
                'total_emergency_capacity': total_shelter_capacity
            },
            'interdicted_corridors': interdicted_corridors,
            'state_breakdown': state_summary,
            'actionable_directives': [
                "BRO Project Swastik & Pushpak: Deploy earthmovers immediately to clear primary lifeline bypasses.",
                "SDRF / NDRF 1st Battalion (Guwahati) & 12th Battalion (Itanagar): Position swift water / rubble rescue teams.",
                "District Transport Authorities: Impose strict traffic stoppage at Singtam, Haflong, and Zubza checkpoints.",
                "District Medical Officers: Activate mobile health units at Upper Martam School and Haflong Stadium."
            ]
        }

        return sitrep_doc

    @staticmethod
    def format_sitrep_text(doc: Dict[str, Any]) -> str:
        """Renders the SITREP document into a clean, human-readable terminal/PDF briefing text."""
        meta = doc['metadata']
        exec_s = doc['executive_summary']
        lines = [
            "=" * 72,
            f"  SITUATION REPORT (SITREP): {meta['report_id']}",
            f"  {meta['issued_by']}",
            f"  Issued: {meta['timestamp_ist']} | Status: {exec_s['threat_level']}",
            "=" * 72,
            "",
            "1. EXECUTIVE OVERVIEW:",
            f"   • Active Landslide Hazard Points:   {exec_s['active_landslide_hotspots']}",
            f"   • Closed Highway Corridors:          {exec_s['closed_highway_sections']} ({exec_s['total_interdicted_road_km']} km blocked)",
            f"   • Active Relief Shelters:            {exec_s['operational_relief_shelters']} (Total Capacity: {exec_s['total_emergency_capacity']} evacuees)",
            "",
            "2. INTERDICTED HIGHWAY CORRIDORS (BLOCKED):"
        ]

        if not doc['interdicted_corridors']:
            lines.append("   • All monitored corridors currently OPEN and free flowing.")
        else:
            for c in doc['interdicted_corridors']:
                lines.append(f"   [!] {c['corridor_name']} ({c['blocked_length_km']} km)")
                lines.append(f"       Reason: {c['cause']}")
                lines.append(f"       Action: {c['clearing_agency']} deploying {c['heavy_equipment_required']}")

        lines.extend([
            "",
            "3. ACTIONABLE DIRECTIVES FOR DISTRICT MAGISTRATES & NDRF:"
        ])
        for idx, act in enumerate(doc['actionable_directives'], 1):
            lines.append(f"   {idx}. {act}")

        lines.extend(["", "=" * 72])
        return "\n".join(lines)
