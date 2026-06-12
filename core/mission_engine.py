"""
DSMP Mission Engine — Central Orchestrator
Coordinates trajectory calculations, propellant estimation, timeline generation, and feasibility checking.
"""

from datetime import datetime, timedelta
import numpy as np

from core.constants import MU_SUN, MU_EARTH, MU_MARS, R_EARTH, R_MARS, G0, DAY_S
from core.astrodynamics.hohmann import leo_to_lunar_transfer, hohmann_transfer
from core.astrodynamics.lambert import lambert_solve
from core.fuel_models.tsiolkovsky import propellant_mass, build_delta_v_budget
from core.trajectories.earth_mars import get_planet_state, date_to_jd, jd_to_date
from core.trajectories.asteroid import get_asteroid_state


class MissionEngine:
    """Main mission planning orchestrator."""

    def __init__(self, mission_config):
        """
        config = {
            "origin": "Earth",
            "destination": "Mars",  # Moon, Mars, Bennu, Psyche
            "spacecraft_mass": 2500, # kg
            "propulsion_type": "Chemical", # Chemical, Electric, Nuclear
            "payload_mass": 800, # kg
            "launch_date": "2032-08-15" # YYYY-MM-DD
        }
        """
        self.config = mission_config
        self.origin = mission_config.get("origin", "Earth").strip()
        self.destination = mission_config.get("destination", "Mars").strip()
        self.m0 = float(mission_config.get("spacecraft_mass", 2500.0))
        self.payload = float(mission_config.get("payload_mass", 800.0))
        self.propulsion = mission_config.get("propulsion_type", "Chemical").strip()
        self.launch_date = mission_config.get("launch_date", "2032-08-15").strip()
        self.results = {}

    def plan_mission(self):
        """Execute full mission planning sequence."""
        self.results["feasibility"] = self._evaluate_feasibility()
        
        # Calculate Delta-V Budget dynamically
        self.results["delta_v_budget"] = self._compute_delta_v()
        
        # Calculate Propellant consumption
        self.results["fuel"] = self._compute_fuel()
        
        # Build timeline
        self.results["timeline"] = self._generate_timeline()
        self.results["risk_score"] = self._compute_risk()
        return self.results

    def _evaluate_feasibility(self):
        """Check if the mission parameters are valid and feasible."""
        valid_destinations = ["Moon", "Mars", "Bennu", "Psyche"]
        valid_propulsion = ["Chemical", "Electric", "Nuclear"]
        
        checks = {
            "valid_destination": self.destination in valid_destinations,
            "adequate_mass": self.m0 > self.payload,
            "propulsion_supported": self.propulsion in valid_propulsion
        }
        
        # Check if fuel requirement is physically possible
        feasible = all(checks.values())
        return {
            "feasible": feasible,
            "checks": checks
        }

    def _get_isp(self):
        """Return Isp based on propulsion type."""
        isp_map = {
            "Chemical": 320.0,      # LH2/LOX or similar high-performing chemical
            "Electric": 2000.0,     # Ion / Hall Effect Thrusters
            "Nuclear": 900.0        # Nuclear Thermal Propulsion (NTP)
        }
        return isp_map.get(self.propulsion, 320.0)

    def _compute_delta_v(self):
        """Compute the full ΔV budget dynamically based on planetary ephemerides."""
        # Convert launch date to Julian Date
        try:
            dt_launch = datetime.strptime(self.launch_date, "%Y-%m-%d")
        except ValueError:
            dt_launch = datetime.strptime("2032-08-15", "%Y-%m-%d")
            
        jd_launch = date_to_jd(dt_launch.year, dt_launch.month, dt_launch.day)
        
        Isp = self._get_isp()

        if self.destination == "Moon":
            # Earth-Moon transfer approximation
            transfer = leo_to_lunar_transfer()
            segments = [
                {"name": "LEO Injection", "dv": 9400.0},
                {"name": "TLI (Trans-Lunar Injection)", "dv": float(transfer["tli_dv"] * 1000.0)},
                {"name": "LOI (Lunar Orbit Insertion)", "dv": float(transfer["loi_dv"] * 1000.0)},
                {"name": "Lunar Landing Burn", "dv": 1800.0}
            ]
            
        elif self.destination == "Mars":
            # Heliocentric Earth-Mars Lambert Solver
            # Approximate travel time of 258 days (standard Hohmann)
            flight_days = 258.0
            jd_arrival = jd_launch + flight_days
            dt_flight_s = flight_days * DAY_S
            
            try:
                rE, vE = get_planet_state("earth", jd_launch)
                rM, vM = get_planet_state("mars", jd_arrival)
                
                # Solve Lambert
                v_trans1, v_trans2 = lambert_solve(rE, rM, dt_flight_s, MU_SUN, prograde=True)
                
                v_inf_dep = np.linalg.norm(v_trans1 - vE)
                v_inf_arr = np.linalg.norm(v_trans2 - vM)
            except Exception:
                # Fallback to analytical approximations if Lambert solver fails
                v_inf_dep = 2.94  # km/s
                v_inf_arr = 2.65  # km/s
                
            r_leo = R_EARTH + 300.0
            v_leo = np.sqrt(MU_EARTH / r_leo)
            
            r_mo = R_MARS + 300.0
            v_mo = np.sqrt(MU_MARS / r_mo)
            
            # Injection burn from 300km LEO
            dv_tmi = (np.sqrt(2.0 * MU_EARTH / r_leo + v_inf_dep**2) - v_leo) * 1000.0
            
            # Capture burn into 300km Mars orbit
            dv_moi = (np.sqrt(2.0 * MU_MARS / r_mo + v_inf_arr**2) - v_mo) * 1000.0
            
            segments = [
                {"name": "LEO Insertion", "dv": 9400.0},
                {"name": "TMI (Trans-Mars Injection)", "dv": dv_tmi},
                {"name": "MOI (Mars Orbit Insertion)", "dv": dv_moi},
                {"name": "Mars Landing (EDL)", "dv": 1600.0}
            ]
            
        elif self.destination in ["Bennu", "Psyche"]:
            # Asteroid Rendezvous
            flight_days = 400.0 if self.destination == "Bennu" else 800.0
            jd_arrival = jd_launch + flight_days
            dt_flight_s = flight_days * DAY_S
            
            try:
                rE, vE = get_planet_state("earth", jd_launch)
                rA, vA = get_asteroid_state(self.destination, jd_arrival)
                
                v_trans1, v_trans2 = lambert_solve(rE, rA, dt_flight_s, MU_SUN, prograde=True)
                
                v_inf_dep = np.linalg.norm(v_trans1 - vE)
                v_inf_arr = np.linalg.norm(v_trans2 - vA)
            except Exception:
                v_inf_dep = 3.5
                v_inf_arr = 4.0
                
            r_leo = R_EARTH + 300.0
            v_leo = np.sqrt(MU_EARTH / r_leo)
            
            dv_tpi = (np.sqrt(2.0 * MU_EARTH / r_leo + v_inf_dep**2) - v_leo) * 1000.0
            # Rendezvous matching velocity burn:
            dv_capture = v_inf_arr * 1000.0
            
            segments = [
                {"name": "LEO Insertion", "dv": 9400.0},
                {"name": "Interplanetary Injection", "dv": dv_tpi},
                {"name": "Rendezvous Capture Burn", "dv": dv_capture}
            ]
            
        else:
            segments = [{"name": "Generic Mission Transfer", "dv": 12000.0}]

        # Check if first segment is LEO Insertion
        has_leo_insertion = (len(segments) > 0 and segments[0]["name"] == "LEO Insertion")
        if has_leo_insertion:
            leo_seg = segments[0]
            sc_segments = segments[1:]
            
            # Compute budget for spacecraft maneuvers
            sc_budget = build_delta_v_budget(Isp, self.m0, self.payload, sc_segments)
            
            # Prepend LEO insertion to segment list
            combined_segments = [{
                "name": leo_seg["name"],
                "delta_v_m_s": leo_seg["dv"],
                "mass_start_kg": 0.0,
                "mass_end_kg": 0.0,
                "propellant_consumed_kg": 0.0
            }] + sc_budget["segments"]
            
            total_dv = leo_seg["dv"] + sc_budget["total_delta_v_m_s"]
            
            budget = {
                "initial_mass_kg": self.m0,
                "final_mass_kg": sc_budget["final_mass_kg"],
                "total_fuel_mass_kg": sc_budget["total_fuel_mass_kg"],
                "propellant_fraction": sc_budget["propellant_fraction"],
                "payload_mass_kg": self.payload,
                "payload_margin_kg": sc_budget["payload_margin_kg"],
                "feasible": sc_budget["feasible"],
                "segments": combined_segments,
                "total_delta_v_m_s": total_dv,
                "total_delta_v_km_s": total_dv / 1000.0
            }
        else:
            budget = build_delta_v_budget(Isp, self.m0, self.payload, segments)
            
        return budget

    def _compute_fuel(self):
        """Compute required propellant mass based on the delta-V budget."""
        Isp = self._get_isp()
        total_dv = self.results["delta_v_budget"]["total_delta_v_m_s"]
        has_leo = any(s["name"] == "LEO Insertion" for s in self.results["delta_v_budget"]["segments"])
        sc_dv = total_dv - 9400.0 if has_leo else total_dv
        return propellant_mass(Isp, self.m0, sc_dv)

    def _generate_timeline(self):
        """Generate timeline dates of mission phases."""
        try:
            launch = datetime.strptime(self.launch_date, "%Y-%m-%d")
        except ValueError:
            launch = datetime.strptime("2032-08-15", "%Y-%m-%d")

        timeline = {"launch": self.launch_date}

        if self.destination == "Moon":
            timeline["tli"] = (launch + timedelta(days=1)).strftime("%Y-%m-%d")
            timeline["mid_course"] = (launch + timedelta(days=3)).strftime("%Y-%m-%d")
            timeline["lunar_arrival"] = (launch + timedelta(days=5)).strftime("%Y-%m-%d")
            timeline["landing"] = (launch + timedelta(days=6)).strftime("%Y-%m-%d")
            
        elif self.destination == "Mars":
            timeline["tmi"] = (launch + timedelta(days=1)).strftime("%Y-%m-%d")
            timeline["mid_course"] = (launch + timedelta(days=130)).strftime("%Y-%m-%d")
            timeline["mars_arrival"] = (launch + timedelta(days=258)).strftime("%Y-%m-%d")
            timeline["landing"] = (launch + timedelta(days=259)).strftime("%Y-%m-%d")
            
        elif self.destination in ["Bennu", "Psyche"]:
            flight_days = 400 if self.destination == "Bennu" else 800
            timeline["injection"] = (launch + timedelta(days=1)).strftime("%Y-%m-%d")
            timeline["mid_course"] = (launch + timedelta(days=flight_days // 2)).strftime("%Y-%m-%d")
            timeline["arrival"] = (launch + timedelta(days=flight_days)).strftime("%Y-%m-%d")
            
        return timeline

    def _compute_risk(self):
        """Compute an aerospace feasibility/mission risk index from 0 to 100."""
        risk = 15.0
        
        # Destination risk multiplier
        dest_risk = {"Moon": 5.0, "Mars": 25.0, "Bennu": 35.0, "Psyche": 40.0}
        risk += dest_risk.get(self.destination, 20.0)
        
        # Propulsion risk factors
        prop_risk = {"Chemical": 5.0, "Nuclear": 20.0, "Electric": 15.0}
        risk += prop_risk.get(self.propulsion, 10.0)
        
        # Mass margin penalty
        fuel_results = self.results.get("fuel", {})
        prop_fraction = fuel_results.get("propellant_fraction", 0.0)
        
        if prop_fraction > 0.8:
            risk += 30.0  # Extremely heavy fuel fraction (mass ratio limits reached)
        elif prop_fraction > 0.6:
            risk += 15.0
            
        if not self.results.get("delta_v_budget", {}).get("feasible", False):
            risk = 100.0  # Mission is mathematically unfeasible (dry mass exceeds wet mass margin)
            
        return min(100.0, risk)
