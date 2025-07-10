from datetime import datetime, timedelta, timezone

def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


def datetime_delta(
    hours: float = 0,
    minutes: float = 0,
    seconds: float = 0
) -> datetime:
    return datetime.now(timezone.utc) + timedelta(
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )


def datetime_from_iso(iso_str: str) -> datetime | None:
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def datetime_to_iso(dt: datetime) -> str | None:
    if not dt:
        return None
    return dt.astimezone(timezone.utc).isoformat()


def datetime_to_str(dt: datetime | None = None, format: str = r"%d-%m-%Y") -> str:
    if dt is None:
        dt = datetime_now()
    return dt.strftime(format)