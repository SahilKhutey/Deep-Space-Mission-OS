"""
Base Generator — Common interface for all simulation generators.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List
from datetime import datetime


@dataclass
class SimulationConfig:
    """Base configuration for any simulation."""
    mission: str
    spacecraft_mass: float
    propulsion: str
    launch_date: str
    duration_days: float = 365.0
    fidelity: str = "L2"  # L1 / L2 / L3
    seed: int = 42
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulationResult:
    """Standardized output of any simulation."""
    config: SimulationConfig
    trajectory: List[List[float]] = field(default_factory=list)
    fuel_profile: List[float] = field(default_factory=list)
    power_profile: List[float] = field(default_factory=list)
    thermal_profile: List[float] = field(default_factory=list)
    timeline: List[Dict[str, Any]] = field(default_factory=list)
    states: List[Dict[str, Any]] = field(default_factory=list)
    validation_status: str = "PENDING"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class BaseGenerator(ABC):
    """Abstract base for all simulation generators."""

    @abstractmethod
    def validate_inputs(self, config: SimulationConfig) -> bool:
        """Validate input configuration."""

    @abstractmethod
    def generate(self, config: SimulationConfig) -> SimulationResult:
        """Run simulation and return result."""

    def run(self, config_dict: Dict[str, Any]) -> SimulationResult:
        """Run with dict input — convenience method."""
        # Extract default params if not present
        duration_days = config_dict.get("simulation_duration_days", config_dict.get("duration_days", 365.0))
        config = SimulationConfig(
            mission=config_dict["mission"],
            spacecraft_mass=float(config_dict["spacecraft_mass"]),
            propulsion=config_dict["propulsion"],
            launch_date=config_dict["launch_date"],
            duration_days=float(duration_days),
            fidelity=config_dict.get("fidelity", "L2"),
            seed=config_dict.get("seed", 42),
            metadata=config_dict.get("metadata", {})
        )
        if not self.validate_inputs(config):
            raise ValueError("Invalid input configuration")
        return self.generate(config)
