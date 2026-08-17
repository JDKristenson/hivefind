from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SurfaceResult:
    ok: bool
    text: str = ""
    model: str | None = None
    tokens_in: int | None = None
    tokens_out: int | None = None
    cost_usd: float | None = None          # None == unmetered by vendor; never 0.0 unless the vendor said 0.0
    target_ref: str | None = None
    raw: dict = field(default_factory=dict)
    error: str | None = None


class SurfaceError(RuntimeError):
    pass
