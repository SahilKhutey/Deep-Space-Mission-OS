"""
Simulation Playback Engine.
Supports pause, play, speed control, reverse, scrubbing, bookmarks.
"""

import numpy as np
from platform.playback.time_controller import TimeController
from platform.playback.bookmarks import BookmarkManager


class PlaybackEngine:
    """Replays a simulation result with full control."""

    def __init__(self, simulation_result):
        self.result = simulation_result
        states = simulation_result.states
        # Extract time series
        if states and "t_s" in states[0]:
            self.times = np.array([s["t_s"] for s in states])
        else:
            self.times = np.arange(len(states), dtype=float)
        self.total_duration = float(self.times[-1] - self.times[0]) if len(self.times) > 0 else 0.0
        self.controller = TimeController(self.total_duration)
        self.bookmarks = BookmarkManager()
        self.bookmarks.auto_from_timeline(simulation_result.timeline)

    def current_state(self):
        """Interpolate state at current time."""
        if len(self.times) == 0:
            return None
        target_t = self.times[0] + self.controller.current_time
        idx = np.searchsorted(self.times, target_t)
        idx = min(idx, len(self.result.states) - 1)
        return self.result.states[idx]

    def step(self, dt=0.016):
        self.controller.step(dt)
        return self.current_state()

    def jump_to_bookmark(self, name: str):
        """Jump to named bookmark."""
        for bm in self.bookmarks.bookmarks:
            if bm.name == name:
                self.controller.scrub(bm.t_s)
                return True
        return False

    def export_bookmarks(self):
        return self.bookmarks.to_dict()
