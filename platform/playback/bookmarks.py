"""
Bookmarks — Save and navigate to key simulation events.
"""

from datetime import datetime


class Bookmark:
    def __init__(self, name: str, t_s: float, label: str = ""):
        self.name = name
        self.t_s = t_s
        self.label = label or name

    def __repr__(self):
        return f"Bookmark({self.name}, t={self.t_s}s, '{self.label}')"


class BookmarkManager:
    """Manage a collection of bookmarks."""

    def __init__(self):
        self.bookmarks = []

    def add(self, name: str, t_s: float, label: str = ""):
        bm = Bookmark(name, t_s, label)
        self.bookmarks.append(bm)
        return bm

    def auto_from_timeline(self, timeline):
        """Generate bookmarks from mission timeline events."""
        for event in timeline:
            phase = event.get("phase", "Event")
            t_s = event.get("t_s", 0.0)
            if t_s == 0.0 and "timestamp" in event:
                t_s = self._timestamp_to_seconds(event["timestamp"], timeline[0].get("timestamp", ""))
            self.add(phase, t_s, label=phase)

    def _timestamp_to_seconds(self, ts, start_ts):
        try:
            dt = datetime.fromisoformat(ts)
            dt_start = datetime.fromisoformat(start_ts)
            return (dt - dt_start).total_seconds()
        except Exception:
            return 0.0

    def to_dict(self):
        return [{"name": b.name, "t_s": b.t_s, "label": b.label}
                for b in self.bookmarks]
