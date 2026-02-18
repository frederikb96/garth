from __future__ import annotations

from datetime import datetime, timezone


def _now_iso() -> str:
    now = datetime.now(timezone.utc)
    return (
        now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"
    )
