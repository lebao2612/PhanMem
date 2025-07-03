from datetime import datetime, timedelta, timezone

class TimeUtil:
    @staticmethod
    def now() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def time(
        hours: float = 0,
        minutes: float = 0,
        seconds: float = 0
    ) -> datetime:
        return datetime.now(timezone.utc) + timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        )

    @staticmethod
    def from_iso(iso_str: str) -> datetime | None:
        try:
            dt = datetime.fromisoformat(iso_str)
            return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return None

    @staticmethod
    def to_iso(dt: datetime) -> str | None:
        if not dt:
            return None
        return dt.astimezone(timezone.utc).isoformat()
