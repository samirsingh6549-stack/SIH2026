import math
from typing import Dict, Any

class GeotechSensorSimulator:
    """
    Simulates in-situ geotechnical IoT instrumentation arrays deployed along
    vulnerable slope cut-sections, conforming to CSIR-CRRI and GSI field specs.
    """

    @staticmethod
    def read_telemetry(
        station: Dict[str, Any],
        rainfall_24h_mm: float,
        antecedent_72h_mm: float,
        soil_moisture_pct: float
    ) -> Dict[str, Any]:
        """
        Synthesizes coupled hydro-mechanical geotechnical telemetry:
        1. Subsurface pore water pressure (Piezometer, kPa)
        2. Biaxial slope tilt displacement (MEMS Inclinometer, degrees)
        3. Tension crack opening (Wire Extensometer, mm)
        4. Acoustic emission rate (Acoustic Waveguide Sensor, hits/min)
        """
        slope_deg = float(station.get("slope_angle_degrees", 35.0))
        soil_type = str(station.get("soil_type", "clay")).lower()

        # Hydro-mechanical coupling:
        # Clay/silt soils trap water with low hydraulic conductivity, causing pore pressure spikes.
        permeability_factors = {
            "clay": 1.45,
            "silt": 1.20,
            "loam": 0.95,
            "sand": 0.65,
            "gravel": 0.35
        }
        p_factor = permeability_factors.get(soil_type, 1.0)

        # 1. Pore Water Pressure (kPa)
        # Saturated hydrostatic pressure buildup along the shear slip plane (approx 1.8m depth)
        saturation_ratio = max(0.0, min(1.0, (soil_moisture_pct - 25.0) / 75.0))
        rainfall_contribution = (rainfall_24h_mm * 0.08) + (antecedent_72h_mm * 0.035)
        pore_pressure_kpa = round(
            max(0.5, (saturation_ratio * 12.5 * p_factor) + rainfall_contribution), 2
        )

        # 2. Biaxial Slope Tilt (degrees)
        # Baseline gravity tilt + micro-deflections when pore pressure reduces effective shear resistance
        creep_rate = 0.02
        if pore_pressure_kpa > 10.0:
            creep_rate += (pore_pressure_kpa - 10.0) * 0.06
        tilt_x = round(0.15 + (math.sin(math.radians(slope_deg)) * creep_rate), 3)
        tilt_y = round(0.08 + (math.cos(math.radians(slope_deg)) * 0.015), 3)

        # 3. Surface Tension Crack Displacement (mm)
        crack_displacement_mm = round(
            max(0.0, ((pore_pressure_kpa - 6.0) * 1.8) if pore_pressure_kpa > 6.0 else 0.2), 2
        )

        # 4. Acoustic Emission (Micro-fracturing in rock/regolith matrix)
        acoustic_hits = int(max(2, round(crack_displacement_mm * 14.0 + (rainfall_24h_mm * 0.15))))

        # 5. Geotechnical Hazard Flag
        sensor_alarm_status = "NORMAL"
        if pore_pressure_kpa >= 14.0 or tilt_x >= 0.85:
            sensor_alarm_status = "CRITICAL_DESTABILIZATION"
        elif pore_pressure_kpa >= 9.0 or tilt_x >= 0.45:
            sensor_alarm_status = "WARNING_CREEP_ACCELERATION"
        elif pore_pressure_kpa >= 5.5:
            sensor_alarm_status = "ELEVATED_PORE_PRESSURE"

        return {
            "station_id": station.get("station_id"),
            "station_name": station.get("station_name"),
            "piezometer": {
                "sensor_type": "Vibrating Wire Subsurface Piezometer",
                "pore_water_pressure_kpa": pore_pressure_kpa,
                "pressure_trend": "RISING" if rainfall_24h_mm > 40.0 else "STABLE",
                "unit": "kPa"
            },
            "tiltmeter": {
                "sensor_type": "Biaxial Digital MEMS Inclinometer",
                "tilt_axis_x_deg": tilt_x,
                "tilt_axis_y_deg": tilt_y,
                "vector_displacement_deg": round(math.sqrt(tilt_x**2 + tilt_y**2), 3),
                "unit": "degrees"
            },
            "extensometer": {
                "sensor_type": "Surface Tension Crack Extensometer",
                "crack_width_displacement_mm": crack_displacement_mm,
                "unit": "mm"
            },
            "acoustic_emission": {
                "sensor_type": "High-Frequency Acoustic Waveguide",
                "ring_down_count": acoustic_hits,
                "unit": "hits/min"
            },
            "sensor_alarm_status": sensor_alarm_status
        }
