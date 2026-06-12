# Aerospace-Grade Export Pipeline

Every simulation run in the Deep Space Simulation Platform follows a strict pipeline to ensure data integrity, traceability, and accessibility.

```
Simulation Results
   │
   ▼
Validation (ResultValidator enforces conservation of mass, energy, and physical boundaries)
   │
   ▼
Analytics (MissionAnalytics, PropulsionAnalytics, TwinAnalytics calculate metrics)
   │
   ▼
Visualization (2D plots, 3D orbits, dashboards, and XR scene graphs are rendered)
   │
   ▼
Export Manager (Routes data to the target exporter module)
   ├── Data: CSV, JSON, HDF5
   ├── Reports: PDF, DOCX, PPTX
   ├── Visuals: PNG, SVG, MP4, GIF
   ├── 3D Models: GLTF, GLB, OBJ
   └── XR Bundles: Unity package, OpenXR scene graphs
```

## Traceability & Versioning
Every exported artifact contains:
1.  **simulation_uuid**: A unique trace back to the exact code execution run.
2.  **config_hash**: A hash of the inputs (launch date, spacecraft mass, propulsion type).
3.  **validation_stamp**: Set to `VALID` or `FAILED` to prevent downstream pipelines from consuming corrupted data.
4.  **timestamp**: UTC ISO 8601 creation timestamp.
