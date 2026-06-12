"""
Time Controller — Speed, pause, reverse, scrub.
"""

import numpy as np


class TimeController:
    """Manages simulation playback time with speed control."""

    SPEEDS = [0.1, 0.5, 1.0, 2.0, 10.0, 100.0, 1000.0]

    def __init__(self, total_duration_s: float):
        self.total_duration = total_duration_s
        self.current_time = 0.0
        self.speed_index = 2  # default = 1x (SPEEDS[2] == 1.0)
        self.is_playing = False
        self.direction = 1  # 1 = forward, -1 = reverse

    @property
    def speed(self):
        return self.SPEEDS[self.speed_index] * self.direction

    def play(self):
        self.is_playing = True

    def pause(self):
        self.is_playing = False

    def toggle_direction(self):
        self.direction *= -1

    def set_speed(self, index: int):
        if 0 <= index < len(self.SPEEDS):
            self.speed_index = index

    def step(self, dt_real: float = 0.016):
        """Advance simulation time by dt_real * speed."""
        if self.is_playing:
            self.current_time += dt_real * self.speed
            self.current_time = max(0.0, min(self.total_duration, self.current_time))

    def scrub(self, t: float):
        """Jump to specific time."""
        self.current_time = max(0.0, min(self.total_duration, t))

    @property
    def progress(self):
        if self.total_duration == 0.0:
            return 0.0
        return self.current_time / self.total_duration
