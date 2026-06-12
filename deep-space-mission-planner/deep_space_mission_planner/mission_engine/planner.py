"""
Mission planner engine.
"""

class MissionEngine:
    def plan(self, mission):
        destination = mission.get("destination", "Moon")
        
        if destination == "Moon":
            total_dv = 15.5
            timeline = [
                {"event": "Launch & LEO Insertion", "delta_v": 9.5},
                {"event": "Trans-Lunar Injection (TLI)", "delta_v": 3.15},
                {"event": "Lunar Orbit Insertion (LOI)", "delta_v": 0.85},
                {"event": "Lunar Landing", "delta_v": 2.0}
            ]
        elif destination == "Mars":
            total_dv = 16.0
            timeline = [
                {"event": "Launch & LEO Insertion", "delta_v": 9.5},
                {"event": "Trans-Mars Injection (TMI)", "delta_v": 3.6},
                {"event": "Mars Orbit Insertion (MOI)", "delta_v": 2.1},
                {"event": "Mars Landing", "delta_v": 0.8}
            ]
        else:
            total_dv = 12.0
            timeline = [
                {"event": "Launch", "delta_v": 9.0},
                {"event": "Transfer", "delta_v": 2.0},
                {"event": "Insertion", "delta_v": 1.0}
            ]
            
        return {
            "feasible": True,
            "total_delta_v_km_s": total_dv,
            "propellant_fraction": 0.75,
            "timeline": timeline
        }
