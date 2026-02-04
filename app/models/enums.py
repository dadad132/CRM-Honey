from enum import Enum


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    blocked = "blocked"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class MeetingPlatform(str, Enum):
    zoom = "zoom"
    teams = "teams"
    discord = "discord"
    in_person = "in_person"
    google_meet = "google_meet"
    phone = "phone"
    other = "other"
