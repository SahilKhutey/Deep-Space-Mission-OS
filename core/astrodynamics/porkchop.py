"""
Porkchop Plot and Launch Window Analysis Generator
Computes C3 launch energy, arrival v_infinity, and total delta-V grids across departure/arrival date ranges.
"""

import numpy as np
import matplotlib.pyplot as plt
from core.constants import MU_SUN, MU_EARTH, MU_MARS, R_EARTH, R_MARS, DAY_S
from core.trajectories.earth_mars import get_planet_state
from core.astrodynamics.lambert import lambert_solve


def generate_porkchop_data(departure_jds, arrival_jds, destination="mars", prograde=True):
    """
    Calculate porkchop plot grid data.
    
    Parameters
    ----------
    departure_jds : array-like - Departure Julian dates
    arrival_jds   : array-like - Arrival Julian dates
    destination   : str        - Destination planet (currently "mars" supported)
    prograde      : bool       - Heliocentric orbit direction
    
    Returns
    -------
    dict with C3 grid, v_inf_arr grid, total_dv grid, and date ranges.
    """
    n_dep = len(departure_jds)
    n_arr = len(arrival_jds)
    
    c3_grid = np.zeros((n_dep, n_arr))
    v_inf_arr_grid = np.zeros((n_dep, n_arr))
    total_dv_grid = np.zeros((n_dep, n_arr))

    # Spacecraft parking orbit presets
    # Earth LEO: 300 km altitude
    r_leo = R_EARTH + 300.0
    v_leo = np.sqrt(MU_EARTH / r_leo)
    
    # Destination orbit insertions:
    if destination.lower() == "mars":
        mu_dest = MU_MARS
        r_dest_orbit = R_MARS + 300.0  # 300 km altitude
        v_dest_orbit = np.sqrt(MU_MARS / r_dest_orbit)
    else:
        # Generic fallback
        mu_dest = MU_MARS
        r_dest_orbit = R_MARS + 300.0
        v_dest_orbit = np.sqrt(MU_MARS / r_dest_orbit)

    for i, t_dep in enumerate(departure_jds):
        try:
            rE, vE = get_planet_state("earth", t_dep)
        except Exception:
            c3_grid[i, :] = np.nan
            v_inf_arr_grid[i, :] = np.nan
            total_dv_grid[i, :] = np.nan
            continue

        for j, t_arr in enumerate(arrival_jds):
            dt_days = t_arr - t_dep
            if dt_days <= 10.0:  # Require at least 10 days of flight time
                c3_grid[i, j] = np.nan
                v_inf_arr_grid[i, j] = np.nan
                total_dv_grid[i, j] = np.nan
                continue
                
            dt_s = dt_days * DAY_S
            
            try:
                rD, vD = get_planet_state(destination, t_arr)
                # Solve Lambert
                v_trans1, v_trans2 = lambert_solve(rE, rD, dt_s, MU_SUN, prograde=prograde)
                
                # Hyperbolic excess velocities
                v_inf_dep = v_trans1 - vE
                v_inf_arr = v_trans2 - vD
                
                v_inf_dep_norm = np.linalg.norm(v_inf_dep)
                v_inf_arr_norm = np.linalg.norm(v_inf_arr)
                
                # C3 launch energy (km^2/s^2)
                c3 = v_inf_dep_norm**2
                c3_grid[i, j] = c3
                v_inf_arr_grid[i, j] = v_inf_arr_norm
                
                # Trans-injection burn from circular LEO
                # v_esc^2 + v_inf^2 = v_burn_start^2
                # v_burn_start = sqrt(2*mu/r + v_inf^2)
                dv_dep = np.sqrt(2.0 * MU_EARTH / r_leo + c3) - v_leo
                
                # Capture burn into destination circular orbit
                dv_arr = np.sqrt(2.0 * mu_dest / r_dest_orbit + v_inf_arr_norm**2) - v_dest_orbit
                
                total_dv_grid[i, j] = dv_dep + dv_arr
            except Exception:
                c3_grid[i, j] = np.nan
                v_inf_arr_grid[i, j] = np.nan
                total_dv_grid[i, j] = np.nan

    return {
        "departure_jds": departure_jds,
        "arrival_jds": arrival_jds,
        "c3": c3_grid,
        "v_inf_arr": v_inf_arr_grid,
        "total_dv": total_dv_grid
    }


def plot_porkchop(data, save_path=None):
    """
    Generate and save a visual porkchop plot from data.
    """
    dep_dates = data["departure_jds"]
    arr_dates = data["arrival_jds"]
    total_dv = data["total_dv"]
    c3 = data["c3"]
    
    # Subtract starting JD for relative axis labels
    x = dep_dates - dep_dates[0]
    y = arr_dates - arr_dates[0]
    
    X, Y = np.meshgrid(x, y)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot total delta-V contours
    # Limit max dv to plot for better visibility
    dv_plot = total_dv.T
    dv_plot = np.clip(dv_plot, 0, 15.0)
    
    cp_dv = ax.contour(X, Y, dv_plot, levels=np.arange(3.0, 12.0, 0.5), colors='blue', alpha=0.7)
    ax.clabel(cp_dv, inline=True, fontsize=8, fmt='%.1f km/s')
    
    # Plot C3 contours
    c3_plot = c3.T
    c3_plot = np.clip(c3_plot, 0, 50.0)
    cp_c3 = ax.contour(X, Y, c3_plot, levels=[10, 15, 20, 25, 30, 40], colors='red', linestyles='dashed', alpha=0.7)
    ax.clabel(cp_c3, inline=True, fontsize=8, fmt='C3=%.0f')
    
    ax.set_xlabel(f"Days since Departure Start JD: {dep_dates[0]}")
    ax.set_ylabel(f"Days since Arrival Start JD: {arr_dates[0]}")
    ax.set_title("Earth → Mars Launch Window (Porkchop Plot)")
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        plt.close()
    return fig
