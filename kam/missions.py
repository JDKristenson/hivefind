"""Mission sensitivity fence (PRD v1.1 §6.2 step 3). Reads 00 CIC/2 PROJECTS.yaml; fails closed."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from .config import LOCAL_SURFACES, PROJECTS_YAML


@dataclass(frozen=True)
class Mission:
    id: str
    sensitivity: str  # cloud-ok | local-only | UNSET | (missing)
    path: str = ""
    status: str = ""

    @property
    def cloud_ok(self) -> bool:
        return self.sensitivity == "cloud-ok"


def load_missions(path: Path = PROJECTS_YAML) -> dict[str, Mission]:
    """Parse the manifest. Entries are flow-style dicts under a top-level list; tolerate comments and odd keys."""
    if not path.exists():
        return {}
    text = path.read_text()
    out: dict[str, Mission] = {}
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        data = None
    items: list = []
    if isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                items.extend(v)
    elif isinstance(data, list):
        items = data
    for it in items:
        if isinstance(it, dict) and "id" in it:
            out[str(it["id"])] = Mission(
                id=str(it["id"]), sensitivity=str(it.get("sensitivity", "UNSET")),
                path=str(it.get("path", "")), status=str(it.get("status", "")),
            )
    if not out:  # fallback: regex over flow-style lines
        for m in re.finditer(r"id:\s*([A-Za-z0-9_.-]+).*?sensitivity:\s*([A-Za-z-]+)", text):
            out[m.group(1)] = Mission(id=m.group(1), sensitivity=m.group(2))
    return out


def resolve(mission_id: str, missions: dict[str, Mission] | None = None) -> Mission:
    missions = missions if missions is not None else load_missions()
    return missions.get(mission_id, Mission(id=mission_id, sensitivity="MISSING"))


def surface_allowed_for(mission: Mission, surface: str) -> tuple[bool, str]:
    """Local surfaces are always allowed. External surfaces need an explicit cloud-ok mission."""
    if surface in LOCAL_SURFACES:
        return True, "local surface"
    if mission.cloud_ok:
        return True, "mission cloud-ok"
    return False, f"mission {mission.id} sensitivity={mission.sensitivity}; external surface {surface} refused (fail closed)"
