import math
from typing import Dict, Any, List

def evaluate_caine_threshold(rainfall_intensity_mmh: float, duration_hours: float = 24.0) -> Dict[str, Any]:
    """
    Evaluates Caine's (1980) Empirical Rainfall Intensity-Duration Threshold:
        I_c = 14.82 * D^(-0.39)
    Where:
        I_c: Critical threshold intensity in mm/hour
        D: Duration in hours (default 24h)
    If observed intensity exceeds I_c, empirical landslide triggering conditions are met.
    """
    duration = max(1.0, float(duration_hours))
    critical_intensity = 14.82 * (duration ** (-0.39))
    observed_intensity = float(rainfall_intensity_mmh)
    exceeded = observed_intensity >= critical_intensity

    margin_ratio = round(observed_intensity / critical_intensity, 2) if critical_intensity > 0 else 0.0

    return {
        'breached': bool(exceeded),
        'critical_threshold_mmh': round(critical_intensity, 2),
        'observed_intensity_mmh': round(observed_intensity, 2),
        'duration_hours': duration,
        'intensity_ratio': margin_ratio
    }

def calculate_factor_of_safety(
    slope_angle_deg: float,
    pore_pressure_kpa: float,
    soil_type: str = 'clay',
    soil_depth_m: float = 1.8
) -> Dict[str, Any]:
    """
    Calculates the Geotechnical Factor of Safety (FoS) using the Infinite Slope Model:
        FoS = [ c' + (gamma * z - u) * cos^2(beta) * tan(phi') ] / [ gamma * z * sin(beta) * cos(beta) ]

    Parameters:
        beta: Slope inclination in radians
        gamma: Soil unit weight (~18.5 kN/m^3)
        z: Soil regolith thickness (m)
        u: Pore water pressure at slip surface (kPa)
        c': Effective soil cohesion (kPa)
        phi': Effective internal friction angle (degrees)

    Interpretation:
        FoS > 1.3  : Stable slope
        1.0 <= FoS <= 1.3 : Marginally stable / Alert
        FoS < 1.0  : Active failure / High imminent collapse
    """
    # Geotechnical parameters calibrated for Himalayan residual soils and GSI field benchmarks
    soil_params = {
        'sand': {'cohesion': 2.5, 'friction_angle': 32.0, 'unit_weight': 18.0},
        'loam': {'cohesion': 6.5, 'friction_angle': 26.0, 'unit_weight': 18.2},
        'clay': {'cohesion': 8.0, 'friction_angle': 20.0, 'unit_weight': 18.5},
        'silt': {'cohesion': 5.0, 'friction_angle': 24.0, 'unit_weight': 18.0},
        'gravel': {'cohesion': 1.5, 'friction_angle': 36.0, 'unit_weight': 19.5}
    }

    params = soil_params.get(str(soil_type).lower(), soil_params['clay'])
    c_prime = params['cohesion']
    phi_prime = math.radians(params['friction_angle'])
    gamma = params['unit_weight']
    z = max(0.5, float(soil_depth_m))
    u = max(0.0, float(pore_pressure_kpa))

    beta = math.radians(max(1.0, min(89.0, float(slope_angle_deg))))

    # Normal and shear stress components
    total_normal_stress = gamma * z
    effective_stress_normal = max(0.1, total_normal_stress - u)

    cos_beta = math.cos(beta)
    sin_beta = math.sin(beta)
    tan_phi = math.tan(phi_prime)

    # Resisting shear strength (Coulomb criterion)
    resisting_force = c_prime + (effective_stress_normal * (cos_beta ** 2) * tan_phi)

    # Driving gravitational shear stress
    driving_force = total_normal_stress * sin_beta * cos_beta

    if driving_force <= 0.001:
        fos = 9.99
    else:
        fos = max(0.05, min(9.99, round(resisting_force / driving_force, 2)))

    stability_status = "STABLE" if fos > 1.3 else ("MARGINAL" if fos >= 1.0 else "UNSTABLE")

    return {
        'factor_of_safety': fos,
        'stability_status': stability_status,
        'resisting_stress_kpa': round(resisting_force, 2),
        'driving_stress_kpa': round(driving_force, 2),
        'pore_pressure_kpa': round(u, 2)
    }

def extract_contributing_risk_factors(features: Dict[str, Any]) -> List[str]:
    """
    Synthesizes explainable domain-specific key risk factors.
    """
    factors = []
    rainfall = float(features.get('rainfall_mm', 0))
    slope = float(features.get('slope_angle_degrees', 0))
    moisture = float(features.get('soil_moisture_percent', 0))
    antecedent = float(features.get('antecedent_rainfall_72h_mm', 0))
    pore_press = float(features.get('pore_water_pressure_kpa', 0))
    vegetation = float(features.get('vegetation_density_ndvi', 0.5))

    if rainfall >= 100.0:
        factors.append(f"Torrential 24h precipitation ({rainfall:.1f} mm) exceeding regional flash runoff threshold")
    elif rainfall >= 60.0:
        factors.append(f"Heavy sustained rainfall ({rainfall:.1f} mm)")

    if antecedent >= 180.0:
        factors.append(f"Severe 72h antecedent rainfall accumulation ({antecedent:.1f} mm) saturating deep regolith")

    if slope >= 38.0:
        factors.append(f"Extremely steep topographical slope angle ({slope:.1f}°) with high gravitational shear")
    elif slope >= 28.0:
        factors.append(f"Moderate to steep slope gradient ({slope:.1f}°)")

    if moisture >= 80.0:
        factors.append(f"Near-complete soil saturation ({moisture:.1f}%) reducing inter-particle cohesion")

    if pore_press >= 8.0:
        factors.append(f"High subsurface pore water pressure ({pore_press:.1f} kPa) causing effective stress dissipation")

    if vegetation <= 0.25:
        factors.append(f"Sparse vegetation cover (NDVI: {vegetation:.2f}) lacking root tensile reinforcement")

    if not factors:
        factors.append("Sub-critical environmental and geotechnical metrics within baseline safety thresholds")

    return factors
