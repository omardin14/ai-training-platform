"""Progress tracking and session management for the learning platform."""

import json
import os
from datetime import date, timedelta

_PROGRESS_FILE = ".learn-progress.json"


def _progress_path():
    """Return the absolute path to the progress file in the project root."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, _PROGRESS_FILE)


def load_progress():
    """Load progress from disk. Returns dict with 'courses' and 'streak' keys."""
    path = _progress_path()
    default = {"courses": {}, "last_active": None, "streak": 0}
    if not os.path.isfile(path):
        return default
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for key in default:
            data.setdefault(key, default[key])
        return data
    except (json.JSONDecodeError, OSError):
        return default


def save_progress(progress):
    """Write progress dict to disk."""
    path = _progress_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)


def update_streak(progress):
    """Update the daily streak counter. Returns the current streak number."""
    today = date.today().isoformat()
    last = progress.get("last_active")
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    if last == today:
        return progress.get("streak", 1)
    elif last == yesterday:
        progress["streak"] = progress.get("streak", 0) + 1
    else:
        progress["streak"] = 1
    progress["last_active"] = today
    return progress["streak"]


def mark_lesson(progress, course_id, module_id):
    """Mark a lesson as completed."""
    _ensure_module(progress, course_id, module_id)
    progress["courses"][course_id][module_id]["lesson"] = True


def mark_quiz(progress, course_id, module_id, score, total):
    """Record a quiz score."""
    _ensure_module(progress, course_id, module_id)
    progress["courses"][course_id][module_id]["quiz_score"] = f"{score}/{total}"


def mark_challenge(progress, course_id, module_id):
    """Mark a challenge as passed."""
    _ensure_module(progress, course_id, module_id)
    progress["courses"][course_id][module_id]["challenge"] = True


def get_module_progress(progress, course_id, module_id):
    """Get progress dict for a specific module. Returns {} if none."""
    return progress.get("courses", {}).get(course_id, {}).get(module_id, {})


def _ensure_module(progress, course_id, module_id):
    """Ensure nested dict structure exists."""
    progress["courses"].setdefault(course_id, {})
    progress["courses"][course_id].setdefault(module_id, {})
