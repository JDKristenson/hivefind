"""Agent registry (PRD v1.1 §7.5). Phases 0-1: kam/registry.yaml is the authority. Phase 2: Notion 🤖 Agent Registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .config import REGISTRY_YAML


@dataclass
class Agent:
    name: str
    tier: str = "2"
    default_surface: str = "openrouter"
    allowed_surfaces: list[str] = field(default_factory=list)
    gates: list[str] = field(default_factory=list)
    stage_to: str = "local-drafts"
    paused: bool = False
    bypass_allowlist: bool = False
    mailbox: str = ""
    vault: str = ""
    github_identity: str = ""

    def allows(self, surface: str) -> bool:
        return self.bypass_allowlist or surface in self.allowed_surfaces


class Registry:
    def __init__(self, agents: dict[str, Agent]) -> None:
        self.agents = agents

    @classmethod
    def load(cls, path: Path = REGISTRY_YAML) -> Registry:
        data = yaml.safe_load(path.read_text()) if path.exists() else {}
        agents: dict[str, Agent] = {}
        for name, spec in (data or {}).get("agents", {}).items():
            spec = spec or {}
            agents[name] = Agent(
                name=name,
                tier=str(spec.get("tier", "2")),
                default_surface=spec.get("default_surface", "openrouter"),
                allowed_surfaces=list(spec.get("allowed_surfaces", [])),
                gates=list(spec.get("gates", [])),
                stage_to=spec.get("stage_to", "local-drafts"),
                paused=bool(spec.get("paused", False)),
                bypass_allowlist=bool(spec.get("bypass_allowlist", False)),
                mailbox=spec.get("mailbox", ""),
                vault=spec.get("vault", ""),
                github_identity=spec.get("github_identity", ""),
            )
        return cls(agents)

    def get(self, name: str) -> Agent:
        if name not in self.agents:
            raise KeyError(f"agent '{name}' is not in the registry ({REGISTRY_YAML})")
        return self.agents[name]
