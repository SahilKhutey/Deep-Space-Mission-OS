"""
Analytical 3D Geometry operations for orbits and collision checks.
"""

import numpy as np

def distance_3d(p1, p2):
    """Calculates Euclidean distance in 3D space."""
    return np.linalg.norm(np.array(p1) - np.array(p2))

def line_plane_intersection(line_pt, line_dir, plane_pt, plane_norm):
    """
    Finds the intersection of a line and a 3D plane.
    Returns intersection point, or None if parallel.
    """
    line_dir = np.array(line_dir) / np.linalg.norm(line_dir)
    plane_norm = np.array(plane_norm) / np.linalg.norm(plane_norm)
    
    denominator = np.dot(plane_norm, line_dir)
    if abs(denominator) < 1e-12:
        return None  # Parallel
        
    t = np.dot(plane_norm, np.array(plane_pt) - np.array(line_pt)) / denominator
    return np.array(line_pt) + t * line_dir

def sphere_line_intersection(line_pt, line_dir, sphere_center, radius):
    """
    Finds intersections between a unit line and a sphere.
    Returns list of 0, 1, or 2 intersection points.
    """
    line_pt = np.array(line_pt)
    line_dir = np.array(line_dir) / np.linalg.norm(line_dir)
    sphere_center = np.array(sphere_center)
    
    oc = line_pt - sphere_center
    b = 2 * np.dot(oc, line_dir)
    c = np.dot(oc, oc) - radius**2
    discriminant = b**2 - 4*c
    
    if discriminant < 0:
        return []
    elif discriminant == 0:
        t = -b / 2
        return [line_pt + t * line_dir]
    else:
        t1 = (-b + np.sqrt(discriminant)) / 2
        t2 = (-b - np.sqrt(discriminant)) / 2
        return [line_pt + t1 * line_dir, line_pt + t2 * line_dir]
